#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import json
import base64
import argparse
import subprocess
from config import Config
from file_saver import save_base64_image

# 意图匹配交由 SKILL.md 让 LLM 判断后直接以 --method 传入。
# 此处仅做取值合法性校验，避免脚本层再做语义匹配造成双层错配。
VALID_METHODS = {1, 2, 3, 4, 5, 6, 7, 8, 9}

IMAGE_MAX_BYTES = 5 * 1024 * 1024  # 5MB

# 支持的图片格式魔数
IMAGE_MAGIC = {
    "jpg":  (b"\xff\xd8\xff",),
    "png":  (b"\x89PNG\r\n\x1a\n",),
    "gif":  (b"GIF87a", b"GIF89a"),
    "bmp":  (b"BM",),
    "webp": None,  # 特殊：RIFF....WEBP，单独判断
}

def detect_image_format(data: bytes) -> str:
    """返回格式名，不支持则返回空字符串"""
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    for fmt, magics in IMAGE_MAGIC.items():
        if fmt == "webp":
            continue
        for magic in magics:
            if data[:len(magic)] == magic:
                return fmt
    return ""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", type=int, required=True,
                        help="意图对应的 method（1-9），由上层 LLM 根据 SKILL.md 语义匹配后传入")
    args = parser.parse_args()

    # ==========================
    # 第一步：环境检查
    # ==========================
    if not Config.BDPAN_SPACE_TOKEN:
        print(json.dumps({
            "code": "BP0100",
            "message": "网盘扫描授权未配置，请按以下步骤配置：1. 访问 https://aiconvert.baidu.com/simple/embed/scanSkill 获取 apikey，2. 在终端运行：export BDPAN_API_KEY=\"your_apikey_here\"，配置完成后重试即可",
            "data": None
        }, ensure_ascii=False))
        return

    # method 合法性校验
    if args.method not in VALID_METHODS:
        print(json.dumps({
            "code": "BP0204",
            "message": f"method 参数非法，允许取值 {sorted(VALID_METHODS)}，当前 {args.method}。",
            "data": None
        }, ensure_ascii=False))
        return
    method = args.method

    # ==========================
    # 第二步：读取二进制图片
    # ==========================
    img_bytes = sys.stdin.buffer.read()
    if not img_bytes:
        print(json.dumps({
            "code": "BP0201",
            "message": "缺少图片输入，请通过传入图片。",
            "data": None
        }, ensure_ascii=False))
        return

    # 格式校验（魔数检测）
    fmt = detect_image_format(img_bytes)
    if not fmt:
        print(json.dumps({
            "code": "BP0202",
            "message": "图片格式不支持，仅支持 jpg/png/gif/bmp/webp。",
            "data": None
        }, ensure_ascii=False))
        return

    # 大小校验
    if len(img_bytes) > IMAGE_MAX_BYTES:
        print(json.dumps({
            "code": "BP0203",
            "message": f"图片大小超出限制，最大支持 5MB，当前 {len(img_bytes) / 1024 / 1024:.2f}MB。",
            "data": None
        }, ensure_ascii=False))
        return

    image_b64 = base64.b64encode(img_bytes).decode("utf-8")

    # ==========================
    # 第三步：执行脚本（安全）
    # ==========================
    mode = Config.MODE_BASE64
    cmd_args = [
        "python3", "scripts/do_scan.py",
        "--method", str(method),
        "--mode", str(mode),
        # base64 通过 stdin 传递，避免触发 ARG_MAX 限制（Argument list too long）
    ]

    # 执行（无shell注入风险，base64 via stdin 绕过参数长度限制）
    result = subprocess.run(
        cmd_args,
        input=image_b64,
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()
    if result.returncode != 0 and not output:
        output = json.dumps({
            "errno": -999,
            "error": result.stderr[:500]
        }, ensure_ascii=False)

    # ==========================
    # 客户端增强：base64 → 保存为 path
    # ==========================
    try:
        res = json.loads(output)
        if res.get("errno") == 0 and mode == 1:
            img_b64 = res.get("data", {}).get("image", "")
            if img_b64:
                img_path = save_base64_image(img_b64)
                if img_path:
                    res["data"] = {"path": img_path}
                    output = json.dumps(res, ensure_ascii=False)
    except:
        pass

    # ==========================
    # 第四步：原样透出
    # ==========================
    print(output)

if __name__ == "__main__":
    main()
