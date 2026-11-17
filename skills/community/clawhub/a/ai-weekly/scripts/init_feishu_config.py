#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""飞书连接器配置向导：交互式生成连接器推送目标 delivery/feishu_target.json，免去手动建文件。

仅支持飞书连接器直推（密钥由连接器托管、绝不落配置文件）：
  - delivery/feishu_target.json  {"chat_id": "oc_xxx"} 或 {"user_id": "ou_xxx"}

该文件被 .gitignore 忽略，不入库。

用法：
  1) 交互式（默认）：   python scripts/init_feishu_config.py
  2) 一键（CI / 脚本）： python scripts/init_feishu_config.py --chat-id oc_xxxx
                      python scripts/init_feishu_config.py --user-id ou_xxxx --as user

校验：仅做 JSON 合法 + ID 格式基础检查，不实际发请求（连通性在推送时用 --dry-run 验证）。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DELIVERY = REPO_ROOT / "delivery"
TARGET_JSON = DELIVERY / "feishu_target.json"


def _ask(prompt: str, default: str = "") -> str:
    try:
        val = input(prompt).strip()
    except EOFError:
        val = ""
    return val or default


def validate_target_id(flag: str, vid: str) -> tuple[bool, str]:
    if not vid:
        return False, f"{flag} 不能为空"
    if flag == "--chat-id" and not vid.startswith("oc_"):
        return False, "chat_id 应以 oc_ 开头（飞书群设置→群机器人/群信息里获取）"
    if flag == "--user-id" and not vid.startswith("ou_"):
        return False, "user_id 应以 ou_ 开头（飞书用户 open_id）"
    return True, ""


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)  # 原子替换，避免写到一半被读


def do_connector(chat_id: str, user_id: str, identity: str) -> int:
    if chat_id and user_id:
        print("❌ 只能填其一：--chat-id（群）或 --user-id（私聊），不要同时给")
        return 1
    if chat_id:
        flag, vid = "--chat-id", chat_id
    elif user_id:
        flag, vid = "--user-id", user_id
    else:
        print("❌ 连接器模式需填 --chat-id 或 --user-id")
        return 1
    ok, msg = validate_target_id(flag, vid)
    if not ok:
        print(f"❌ {msg}")
        return 1
    write_json(TARGET_JSON, {flag.lstrip("-").replace("-", "_"): vid})
    print(f"✅ 已写入 {TARGET_JSON}（{flag} = {vid}）")
    print("\n下一步（连接器直推，密钥不落盘）：")
    print(f"  python delivery/feishu_connector.py --report report.json {flag} {vid} --as {identity}")
    print(f"  python delivery/feishu_connector.py --report report.json {flag} {vid} --dry-run   # 仅预览不发送")
    return 0


def interactive() -> int:
    print("=== 飞书连接器配置向导 ===")
    print("目标类型：")
    print("  a) 群（chat_id，机器人需已入群）")
    print("  b) 私聊（user_id，以你本人身份发，首次测试最省心）")
    t = _ask("输入 a 或 b：", "a")
    if t == "b":
        vid = _ask("粘贴你的 user_id（ou_ 开头）：\n> ")
        return do_connector("", vid, "user")
    elif t == "a":
        vid = _ask("粘贴群 chat_id（oc_ 开头）：\n> ")
        return do_connector(vid, "", "bot")
    else:
        print("❌ 无效选择")
        return 1


def main() -> int:
    ap = argparse.ArgumentParser(description="飞书连接器配置向导：交互式生成 feishu_target.json")
    ap.add_argument("--chat-id", help="目标群 chat_id（oc_xxx）")
    ap.add_argument("--user-id", help="目标用户 open_id（ou_xxx），用于私聊")
    ap.add_argument("--as", dest="identity", default="bot", choices=["bot", "user"], help="连接器发送身份（默认 bot）")
    args = ap.parse_args()

    # 非交互模式
    if args.chat_id or args.user_id:
        return do_connector(args.chat_id or "", args.user_id or "", args.identity)

    # 交互模式
    return interactive()


if __name__ == "__main__":
    sys.exit(main())
