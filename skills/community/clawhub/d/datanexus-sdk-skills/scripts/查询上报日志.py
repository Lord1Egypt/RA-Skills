#!/usr/bin/env python3
"""
DataNexus SDK 排障辅助脚本 - 上报数据验证助手

帮助开发者快速验证 SDK 数据上报是否正常，提供各端的调试方法指引，
并可解析本地抓包导出的上报日志进行分析。

使用方式：
    python3 查询上报日志.py --guide
    python3 查询上报日志.py --file <日志文件路径> [--action_type <行为类型>]
    python3 查询上报日志.py --file <日志文件路径> --check-required

注意：
    - 本脚本不需要 access_token 或 secret_key 等敏感信息
    - 仅在本地分析数据，不发送任何网络请求
"""

import argparse
import json
import sys
from datetime import datetime


REQUIRED_EVENTS_BY_TYPE = {
    "android_game": {
        "label": "Android 游戏",
        "required": {
            "START_APP": "启动应用（Android v1.9.4+ 自动采集，无需手动）",
            "REGISTER": "注册",
            "LOGIN": "登录",
            "CREATE_ROLE": "创建角色（无该行为可不报）",
            "PURCHASE": "付费（必传 value）",
        },
        "recommended": {"TUTORIAL_FINISH": "完成新手教程"},
    },
    "harmony": {
        "label": "鸿蒙",
        "required": {"PURCHASE": "付费（必传 value）"},
        "recommended": {"REGISTER": "注册", "LOGIN": "登录"},
        "auto_collected": ["START_APP"],
    },
}

REQUIRED_EVENTS = {
    "START_APP": "启动应用",
    "REGISTER": "注册",
    "LOGIN": "登录",
    "CREATE_ROLE": "创建角色",
    "PURCHASE": "付费",
}

DEBUG_GUIDE = """
╔══════════════════════════════════════════════════════════════╗
║              DataNexus SDK 各端调试方法指引                    ║
╚══════════════════════════════════════════════════════════════╝

【Android 端】
  调试方式: 过滤 Logcat TAG「gdt_action」，info 级别
  成功日志: LogAction success xxxx
  失败日志: LogAction failed xxxx

【iOS 端】
  调试方式: 过滤 TAG「gdt_action」，info 级别

【鸿蒙端】
  调试方式: 初始化时设置 show_log: true
  日志 TAG: [@dn-sdk/harmony v1.x.x]

【小游戏端】
  调试方式: 调用 SDK.setDebug(true)

【小程序端】
  调试方式: 调用 SDK.setDebug(true)

【通用在线验证】
  DataNexus 平台 → 日志查询 → 输入 AppID 或数据源 ID
"""


def parse_log_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        if content.startswith("["):
            records = json.loads(content)
        elif content.startswith("{"):
            data = json.loads(content)
            if "actions" in data:
                records = data["actions"]
            elif "data" in data and "list" in data["data"]:
                records = data["data"]["list"]
            else:
                records = [data]
        else:
            records = []
            for line in content.split("\n"):
                line = line.strip()
                if line and line.startswith("{"):
                    try:
                        records.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        return records
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"❌ Error: {e}")
        return []


def print_records(records, action_type_filter=None):
    filtered = records
    if action_type_filter:
        filtered = [r for r in records if r.get("action_type") == action_type_filter]
    if not filtered:
        print("\n⚠️ 无有效记录。")
        return
    print(f"\n✅ 共 {len(filtered)} 条记录：\n")
    for i, record in enumerate(filtered, 1):
        action_type = record.get("action_type", "N/A")
        action_time = record.get("action_time", "N/A")
        action_param = record.get("action_param", {})
        print(f"  [{i}] 行为类型: {action_type}")
        print(f"      上报时间: {action_time}")
        if action_param:
            print(f"      行为参数: {json.dumps(action_param, ensure_ascii=False)}")
        if action_type == "PURCHASE":
            value = action_param.get("value") if isinstance(action_param, dict) else None
            if value is None:
                print(f"      ⚠️ 警告: 付费事件缺少 value（金额）参数！")


def check_required_events(records, sdk_type=None):
    print("\n" + "=" * 60)
    print("  📋 必报事件完整性检查")
    print("=" * 60)
    found_types = set(r.get("action_type") for r in records)
    required = REQUIRED_EVENTS
    for action_type, name in required.items():
        found = action_type in found_types
        status = "✅" if found else "❌"
        print(f"  {status} {action_type} — {name}")


def main():
    parser = argparse.ArgumentParser(description="DataNexus SDK 上报数据验证助手")
    parser.add_argument("--guide", action="store_true", help="显示各端调试方法指引")
    parser.add_argument("--file", default=None, help="本地日志文件路径")
    parser.add_argument("--action_type", default=None, help="行为类型过滤")
    parser.add_argument("--check-required", action="store_true", help="检查必报事件完整性")
    parser.add_argument("--sdk-type", default=None, help="SDK 端 × 行业类型")
    args = parser.parse_args()

    if args.guide:
        print(DEBUG_GUIDE)
        return
    if not args.file:
        parser.print_help()
        return
    records = parse_log_file(args.file)
    if not records:
        return
    if args.check_required:
        check_required_events(records, sdk_type=args.sdk_type)
    else:
        print_records(records, action_type_filter=args.action_type)


if __name__ == "__main__":
    main()
