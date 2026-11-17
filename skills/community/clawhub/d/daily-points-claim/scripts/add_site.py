#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""交互式向导：把一个新的签到站点追加到 config.json。

用法: python add_site.py [--config 路径]
"""

import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CONFIG = BASE_DIR / "config.json"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0 Safari/537.36")


def ask(prompt, default=""):
    tip = f"{prompt} [{default}]: " if default else f"{prompt}: "
    val = input(tip).strip()
    return val or default


def ask_yes(prompt, default="n"):
    val = input(f"{prompt} [y/N]: ").strip().lower()
    if not val:
        return default == "y"
    return val in ("y", "yes", "是")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(DEFAULT_CONFIG))
    args = ap.parse_args()

    path = Path(args.config).expanduser()
    cfg = {"settings": {}, "sites": []}
    if path.exists():
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"现有配置读取失败: {e}")
            return 2
    cfg.setdefault("sites", [])

    print("=" * 56)
    print("添加一个新的每日签到站点")
    print("提示：先在浏览器登录该站点，按 F12 -> Network，手动签到一次，")
    print("      找到那个签到请求，右键 Copy as cURL，即可拿到 URL/Cookie/请求体。")
    print("=" * 56)

    sid = ask("站点 id（英文短名，用于 --site 指定）")
    if not sid:
        print("id 不能为空")
        return 2
    if any(s.get("id") == sid for s in cfg["sites"]):
        print(f"站点 id 已存在: {sid}")
        return 2

    name = ask("显示名称", sid)
    url = ask("签到接口 URL（完整地址）")
    if not url:
        print("URL 不能为空")
        return 2
    method = ask("请求方法", "POST").upper()
    cookie = ask("Cookie（浏览器里整串复制，直接回车则留空稍后填）")
    referer = ask("Referer（可留空）")

    headers = {"User-Agent": UA}
    if cookie:
        headers["Cookie"] = cookie
    if referer:
        headers["Referer"] = referer

    body_type = "none"
    body = None
    if method in ("POST", "PUT", "PATCH"):
        body_type = ask("请求体类型 json/form/raw/none", "json").lower()
        if body_type != "none":
            print('粘贴请求体（json 直接粘 JSON；form 写 a=1&b=2；raw 直接粘原文），空行结束：')
            if body_type == "json":
                print("  示例: {\"date\":\"{{today}}\"}")
                raw = input("  > ").strip() or "{}"
                try:
                    body = json.loads(raw)
                except Exception:
                    print("JSON 解析失败，已跳过请求体")
                    body, body_type = None, "none"
            elif body_type == "form":
                raw = input("  > ").strip()
                body = {}
                for pair in raw.split("&"):
                    if "=" in pair:
                        k, v = pair.split("=", 1)
                        body[k] = v
            else:
                body = input("  > ").strip()

    print("\n--- 结果判定 ---")
    print("判定决定脚本能否识别「成功」和「今日已领」，务必填准确。")
    judge_kind = ask("判定方式：1=看 JSON 字段  2=看响应文本关键字", "1")

    if judge_kind == "2":
        ok_kw = ask("响应中出现什么文字算成功", "签到成功")
        dup_kw = ask("响应中出现什么文字算今日已领", "已签到")
        expect = {
            "success_when": [{"path": "", "op": "contains", "value": ok_kw}],
            "already_when": [{"path": "", "op": "contains", "value": dup_kw}],
        }
        points_path = ask("积分字段路径（可留空）")
    else:
        jpath = ask("成功时响应里能判断的字段路径，如 code 或 data.status", "code")
        jval = ask("该字段成功时的值", "0")
        try:
            jval = int(jval)
        except ValueError:
            pass
        expect = {"success_when": [{"path": jpath, "op": "eq", "value": jval}]}
        dup_path = ask("今日已领时，消息字段路径（留空则跳过重复判断）", "msg")
        if dup_path:
            dup_kw = ask("该字段里出现什么文字算已领", "已签")
            expect["already_when"] = [{"path": dup_path, "op": "contains", "value": dup_kw}]
        points_path = ask("积分字段路径，如 data.points（可留空）")
        msg_path = ask("消息字段路径，如 msg（可留空）")
        if msg_path:
            expect["message_path"] = msg_path

    if points_path:
        expect["points_path"] = points_path

    site = {
        "id": sid,
        "name": name,
        "enabled": True,
        "request": {"method": method, "url": url, "headers": headers, "body_type": body_type},
        "expect": expect,
    }
    if body is not None:
        site["request"]["body"] = body

    cfg["sites"].append(site)
    cfg.setdefault("settings", {})
    path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n已写入 {path}")

    if ask_yes("现在立即测试一次？"):
        import subprocess
        subprocess.run([sys.executable, str(BASE_DIR / "claim.py"), "--config", str(path), "--site", sid])

    return 0


if __name__ == "__main__":
    sys.exit(main())
