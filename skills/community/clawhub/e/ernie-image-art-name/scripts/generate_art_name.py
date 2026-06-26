#!/usr/bin/env python3
"""
名字转艺术字生成脚本
使用百度星河社区 ERNIE-Image API 生成艺术字图片

用法:
    python3 generate_art_name.py --name "李赞" --style 中国风
    python3 generate_art_name.py --name "Alice" --style 单线卡通
    python3 generate_art_name.py --name "Alice" --style 彩铅卡通 --output ./output
    python3 generate_art_name.py --name "李赞" --token YOUR_ACCESS_TOKEN

配置优先级:
    1. 命令行参数 --token
    2. 环境变量 AISTUDIO_ACCESS_TOKEN
    3. 配置文件 config.json（skill 安装目录下）
"""

import argparse
import base64
import json
import os
import random
import sys
import time
from pathlib import Path

# ──────────────────────────────────────────────────────────────────────────────
# 配置
# ──────────────────────────────────────────────────────────────────────────────

CONFIG_FILE = Path(__file__).parent.parent / "config.json"
DEFAULT_CONFIG = {
    "access_token": "",
    "model": "ERNIE-Image-Turbo",
    "output_dir": "./art_names"
}

API_BASE_URL = "https://aistudio.baidu.com/llm/lmapi/v3"

# ──────────────────────────────────────────────────────────────────────────────
# 风格预设库
# ──────────────────────────────────────────────────────────────────────────────

# 普通风格：单条 prompt 模板（{name} 将被替换为实际名字）
STYLE_PRESETS = {
    "中国风": "中国传统书法艺术字，毛笔字体，水墨风格，金色或红色文字，古典纹样背景，大气磅礴",
    "烫金": "豪华烫金艺术字，金属质感，深色背景，立体浮雕效果，精致华丽",
    "霓虹": "霓虹灯管艺术字，发光效果，赛博朋克风格，深夜城市背景，色彩鲜艳",
    "卡通": "可爱卡通字体，圆润边角，彩虹渐变色，白色背景，活泼有趣",
    "石刻": "古代石刻篆刻艺术字，浮雕质感，古朴沧桑，青铜或石灰岩质感",
    "玫瑰": "玫瑰花卉装饰艺术字，浪漫粉色，花瓣环绕，优雅精致",
    "极简": "现代简约艺术字，黑白灰色调，几何字体，高端设计感",
    "火焰": "火焰燃烧效果艺术字，橙红色火焰，动感强烈，深色背景",
    "冰晶": "冰晶霜冻艺术字，蓝白色调，晶莹剔透，雪花冰花装饰",
    "自定义": ""  # 用户自行输入 prompt
}

# 多模板风格：每次从模板列表随机选取一条，{name} 替换为名字
MULTI_TEMPLATE_STYLES = {
    "单线卡通": [
        '极简黑色单线手绘，ins风可爱简笔画，无填充轮廓线稿，主体为手写花体英文签名"{name}"，与一个软萌卡通元素自然融合，线条流畅干净，搭配少量小星星装饰，纯白背景，无多余元素，构图简洁，适合作为签名图案，高清线稿，无杂色，干净利落',
        '极简黑色单线条手绘，ins风简笔画，无填充，花体英文签名"{name}"与星星、月亮元素融合，线条飘逸流畅，搭配细碎星光装饰，纯白背景，干净极简，可爱温柔，高清线稿，适合签名设计',
        '极简黑色单线手绘，可爱简笔画，无填充，花体英文签名"{name}"与软萌兔子形象融合，兔子抱着星星，线条圆润流畅，搭配小星星装饰，纯白背景，治愈可爱，高清线稿，签名设计',
        '极简黑色单线条手绘，ins风可爱简笔画，无填充，花体英文签名"{name}"与带笑脸的星球融合，星球上趴着一只软萌小熊，线条干净，搭配星光装饰，纯白背景，温柔治愈，高清线稿',
        '极简黑色单线手绘，可爱简笔画，无填充，花体英文签名"{name}"与软萌小刺猬形象融合，线条流畅圆润，搭配星星月亮装饰，纯白背景，治愈风，高清线稿，适合签名/纹身设计',
        '极简黑色单线条手绘，ins风简笔画，无填充，花体英文签名"{name}"与蝴蝶元素融合，蝴蝶线条轻盈，搭配小太阳和星光装饰，纯白背景，清新温柔，高清线稿，签名设计',
        '极简黑色单线手绘，可爱简笔画，无填充，花体英文签名"{name}"与软萌云朵融合，云朵带着笑脸，搭配星星装饰，线条圆润，纯白背景，治愈可爱，高清线稿',
    ],
    "彩铅卡通": [
        '软萌彩铅手绘风，可爱卡通艺术签名设计，主体为流畅的黑色手写花体字"{name}"，搭配同画风的迷你卡通小元素（如小动物脸、小花、云朵、星星），元素融入签名笔画中，点缀低饱和度马卡龙色（粉色、黄色、蓝色），线条圆润软乎乎，带轻微彩铅质感，纯白背景，干净无多余装饰，治愈系ins风，高清线稿，色彩柔和，构图简洁可爱',
        '软萌彩铅手绘，可爱卡通签名，黑色流畅花体字"{name}"，笔画中融入一只迷你的Q版猫咪/小猪/兔子脸，脸颊带粉粉腮红，线条圆润软萌，点缀低饱和粉/黄/蓝马卡龙色小装饰，纯白背景，治愈ins风，色彩柔和，高清干净，适合签名设计',
        '软萌彩铅手绘风，可爱艺术签名，黑色手写花体字"{name}"，搭配简约手绘小花/郁金香/星星元素，自然融入签名笔画中，点缀低饱和粉/黄/蓝色彩，线条圆润柔和，带轻微彩铅肌理，纯白背景，清新治愈，高清干净，无多余元素',
        '软萌彩铅手绘，治愈风签名设计，黑色流畅花体字"{name}"，搭配迷你手绘云朵/爱心/月亮元素，融入签名笔画中，点缀低饱和蓝/粉色，线条软乎乎带轻微彩铅质感，纯白背景，ins可爱风，高清线稿，色彩柔和，构图简洁',
    ],
}


# ──────────────────────────────────────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────────────────────────────────────

def load_config() -> dict:
    """加载配置文件，若不存在则创建默认配置"""
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            return {**DEFAULT_CONFIG, **cfg}
        except (json.JSONDecodeError, IOError):
            pass
    return DEFAULT_CONFIG.copy()


def save_config(cfg: dict):
    """保存配置到文件"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"✅ 配置已保存到 {CONFIG_FILE}")


def get_access_token(args_token: str, config: dict) -> str:
    """按优先级获取 Access Token"""
    # 1. 命令行参数
    if args_token:
        return args_token
    # 2. 环境变量
    env_token = os.environ.get("AISTUDIO_ACCESS_TOKEN", "")
    if env_token:
        return env_token
    # 3. 配置文件
    cfg_token = config.get("access_token", "")
    if cfg_token:
        return cfg_token
    return ""


def build_prompt(name: str, style: str, custom_prompt: str = "") -> str:
    """构建生成艺术字的 Prompt"""
    # 自定义风格
    if style == "自定义" and custom_prompt:
        return f'文字"{name}"，{custom_prompt}'

    # 多模板风格（随机选取一条）
    if style in MULTI_TEMPLATE_STYLES:
        template = random.choice(MULTI_TEMPLATE_STYLES[style])
        return template.replace("{name}", name)

    # 普通预设风格
    style_desc = STYLE_PRESETS.get(style, STYLE_PRESETS["中国风"])
    prompt = (
        f'将文字"{name}"设计成艺术字，{style_desc}，'
        f'文字清晰可辨，高分辨率，精细质感，专业设计感，正方形构图'
    )
    return prompt


def generate_image(prompt: str, access_token: str, model: str) -> bytes:
    """调用 ERNIE-Image API 生成图片，返回图片二进制数据"""
    import urllib.request

    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "response_format": "b64_json",
        "n": 1
    }).encode("utf-8")

    req = urllib.request.Request(
        url=f"{API_BASE_URL}/images/generations",
        data=payload,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        raise RuntimeError(f"API 请求失败 HTTP {e.code}: {body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络连接失败: {e.reason}")

    if "error" in result:
        raise RuntimeError(f"API 返回错误: {result['error']}")

    b64_data = result["data"][0]["b64_json"]
    return base64.b64decode(b64_data)


def save_image(img_bytes: bytes, output_dir: str, name: str, style: str) -> str:
    """保存图片到指定目录，返回保存路径"""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    timestamp = int(time.time())
    safe_name = name.replace("/", "_").replace("\\", "_")
    filename = f"{safe_name}_{style}_{timestamp}.png"
    filepath = out_path / filename
    with open(filepath, "wb") as f:
        f.write(img_bytes)
    return str(filepath)


# ──────────────────────────────────────────────────────────────────────────────
# 主入口
# ──────────────────────────────────────────────────────────────────────────────

def main():
    all_styles = list(STYLE_PRESETS.keys()) + list(MULTI_TEMPLATE_STYLES.keys())

    parser = argparse.ArgumentParser(
        description="名字转艺术字 - 使用百度 ERNIE-Image API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 generate_art_name.py --name "李赞" --style 中国风
  python3 generate_art_name.py --name "Alice" --style 单线卡通
  python3 generate_art_name.py --name "Alice" --style 彩铅卡通 --output ./签名
  python3 generate_art_name.py --name "李赞" --style 自定义 --prompt "蒸汽朋克风格，齿轮装饰"
  python3 generate_art_name.py --set-token YOUR_TOKEN   # 保存 Token 到配置文件
  python3 generate_art_name.py --list-styles             # 查看所有风格

可用风格:
  """ + "  ".join(all_styles)
    )

    parser.add_argument("--name", "-n", type=str, help="要转换为艺术字的名字或文字")
    parser.add_argument(
        "--style", "-s", type=str, default="中国风",
        choices=all_styles,
        help="艺术字风格，默认：中国风"
    )
    parser.add_argument("--prompt", "-p", type=str, default="",
                        help="自定义风格描述（--style 自定义 时生效）")
    parser.add_argument("--output", "-o", type=str, default="",
                        help="图片保存目录，默认使用配置文件中的 output_dir")
    parser.add_argument("--token", "-t", type=str, default="",
                        help="星河社区 Access Token（优先于配置文件）")
    parser.add_argument("--model", "-m", type=str, default="",
                        choices=["ERNIE-Image", "ERNIE-Image-Turbo", "Stable-Diffusion-XL"],
                        help="使用的模型，默认：ERNIE-Image-Turbo")
    parser.add_argument("--set-token", type=str, metavar="TOKEN",
                        help="将 Access Token 保存到配置文件")
    parser.add_argument("--list-styles", action="store_true",
                        help="列出所有可用风格")
    parser.add_argument("--show-config", action="store_true",
                        help="显示当前配置")

    args = parser.parse_args()

    config = load_config()

    # ── 特殊命令 ──────────────────────────────────────────────
    if args.list_styles:
        print("\n📋 可用艺术字风格：\n")
        print("【经典风格】")
        for style, desc in STYLE_PRESETS.items():
            if desc:
                print(f"  {style:8s}  {desc[:40]}...")
            else:
                print(f"  {style:8s}  （用 --prompt 自定义描述）")
        print("\n【卡通签名风格（每次随机选模板）】")
        for style, templates in MULTI_TEMPLATE_STYLES.items():
            print(f"  {style:8s}  {len(templates)} 种模板，随机生成")
            print(f"           示例：{templates[0][:50]}...")
        print()
        return

    if args.show_config:
        print(f"\n⚙️  当前配置（{CONFIG_FILE}）：\n")
        display_cfg = dict(config)
        if display_cfg.get("access_token"):
            display_cfg["access_token"] = display_cfg["access_token"][:8] + "****"
        print(json.dumps(display_cfg, ensure_ascii=False, indent=2))
        print()
        return

    if args.set_token:
        config["access_token"] = args.set_token
        save_config(config)
        print(f"✅ Access Token 已保存！前8位：{args.set_token[:8]}****")
        return

    # ── 参数校验 ──────────────────────────────────────────────
    if not args.name:
        parser.print_help()
        print("\n❌ 请使用 --name 指定要转换的名字")
        sys.exit(1)

    access_token = get_access_token(args.token, config)
    if not access_token:
        print("❌ 未找到 Access Token！请通过以下方式之一提供：")
        print("   1. 命令行：--token YOUR_TOKEN")
        print("   2. 环境变量：export AISTUDIO_ACCESS_TOKEN=YOUR_TOKEN")
        print("   3. 配置文件：python3 generate_art_name.py --set-token YOUR_TOKEN")
        print("\n   获取 Token：https://aistudio.baidu.com/account/accessToken")
        sys.exit(1)

    model = args.model or config.get("model", DEFAULT_CONFIG["model"])
    output_dir = args.output or config.get("output_dir", DEFAULT_CONFIG["output_dir"])

    # ── 生成艺术字 ───────────────────────────────────────────
    prompt = build_prompt(args.name, args.style, args.prompt)

    print(f"\n🎨 正在生成艺术字...")
    print(f"   名字：{args.name}")
    print(f"   风格：{args.style}")
    print(f"   模型：{model}")
    print(f"   Prompt：{prompt[:80]}{'...' if len(prompt) > 80 else ''}\n")

    try:
        img_bytes = generate_image(prompt, access_token, model)
        saved_path = save_image(img_bytes, output_dir, args.name, args.style)
        print(f"✅ 艺术字生成成功！")
        print(f"   保存路径：{saved_path}")
        print(f"   文件大小：{len(img_bytes) / 1024:.1f} KB\n")
    except RuntimeError as e:
        print(f"❌ 生成失败：{e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
