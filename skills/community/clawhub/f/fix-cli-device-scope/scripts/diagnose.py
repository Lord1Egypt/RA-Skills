#!/usr/bin/env python3
"""
诊断 CLI 设备 scope 问题
用法: python3 diagnose.py
"""
import json
import os
import sys
import subprocess

HOME = os.path.expanduser("~")
BASE = f"{HOME}/.openclaw"
PAIRED = f"{BASE}/devices/paired.json"
PENDING = f"{BASE}/devices/pending.json"
AUTH = f"{BASE}/identity/device-auth.json"
DEVICE_AUTH = f"{BASE}/identity/device.json"

def green(msg): print(f"\033[92m✓ {msg}\033[0m")
def red(msg): print(f"\033[91m✗ {msg}\033[0m")
def yellow(msg): print(f"\033[93m! {msg}\033[0m")
def info(msg): print(f"  {msg}")

def check_gateway():
    info("检查 Gateway 状态...")
    r = subprocess.run(["openclaw", "gateway", "status"], capture_output=True, text=True)
    if "running" in r.stdout:
        green("Gateway 正在运行")
    else:
        red(f"Gateway 可能未运行: {r.stdout[:200]}")
    return "running" in r.stdout

def check_devices():
    info("检查设备列表...")
    r = subprocess.run(["openclaw", "devices", "list"], capture_output=True, text=True)
    lines = r.stdout.strip().split("\n")
    # Find CLI devices
    cli_devices = []
    for line in lines:
        if "cli" in line.lower() or "linux" in line.lower():
            cli_devices.append(line)
    if cli_devices:
        for d in cli_devices:
            info(d)
            if "operator.read" in d and "operator.admin" not in d:
                yellow("  → 只有 read scope，缺少 admin！这是问题所在。")
                green("  → 找到了需要修复的设备")
    else:
        info("未找到 CLI 设备")
    return cli_devices

def check_pending():
    if not os.path.exists(PENDING):
        info("无 pending 请求")
        return []
    with open(PENDING) as f:
        pending = json.load(f)
    if not pending:
        info("pending.json 为空")
        return []
    repair_reqs = [(k, v) for k, v in pending.items() if v.get("isRepair")]
    if repair_reqs:
        green(f"找到 {len(repair_reqs)} 个 repair pending 请求")
        for k, v in repair_reqs:
            info(f"  Request: {k}")
            info(f"  Device: {v.get('deviceId', 'N/A')}")
            info(f"  Scopes: {v.get('scopes', [])}")
        return repair_reqs
    else:
        info("无 repair pending 请求")

    # Show all pending
    for k, v in pending.items():
        info(f"  {k}: device={v.get('deviceId')} scopes={v.get('scopes')}")
    return []

def check_auth():
    if not os.path.exists(AUTH):
        red(f"device-auth.json 不存在: {AUTH}")
        return
    if not os.path.exists(DEVICE_AUTH):
        info(f"device.json 不存在")
        return
    with open(AUTH) as f:
        auth = json.load(f)
    with open(DEVICE_AUTH) as f:
        device = json.load(f)
    scopes = auth.get("tokens", {}).get("operator", {}).get("scopes", [])
    device_id = device.get("deviceId", "N/A")
    info(f"当前设备 ID: {device_id}")
    info(f"当前 token scopes: {scopes}")
    if "operator.admin" not in scopes:
        red(f"没有 admin scope！需要修复。")
    else:
        green("已有 admin scope")
    return device_id, scopes

def print_summary(device_id, scopes, pending_reqs, needs_fix):
    """打印紧凑诊断摘要"""
    print("\n" + "="*50)
    print("诊断摘要")
    print("="*50 + "\n")
    
    # 设备信息表格
    print(f"  设备 ID:    {device_id}")
    print(f"  当前 scopes: {scopes}")
    print(f"  pending:    {len(pending_reqs)} repair 请求" if pending_reqs else "  pending:    无")
    print()
    
    # 结论
    if needs_fix:
        print("\033[93m⚠️  需要修复：CLI 设备缺少 admin scope\033[0m")
        print("\033[93m   死循环：当前只有 read，无法 approve 自己的升级请求\033[0m")
        print("\n\033[92m修复命令：\033[0m")
        print("  python3 scripts/fix.py --dry-run  # 先预览")
        print("  python3 scripts/fix.py            # 执行修复")
    elif "operator.admin" in scopes:
        print("\033[92m✓ 设备正常：已有 admin scope\033[0m")
        print("  spawn/cron 应该能正常工作")
    else:
        print("\033[93m⚠️  状态不明确，请手动检查\033[0m")
    print()

def main():
    print("\n=== CLI Device Scope 诊断 ===")
    
    # 1. Gateway
    gw_ok = check_gateway()
    if not gw_ok:
        red("Gateway 未运行，请先启动: openclaw gateway start")
        sys.exit(1)
    
    # 2. 读配置文件（合并为一步）
    device_id, scopes = check_auth()
    
    # 3. pending 状态
    pending_reqs = check_pending()
    
    # 4. 输出紧凑摘要
    needs_fix = "operator.admin" not in scopes and pending_reqs
    print_summary(device_id, scopes, pending_reqs, needs_fix)

if __name__ == "__main__":
    main()