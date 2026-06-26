#!/usr/bin/env python3
"""
验证 scope 修复是否成功
用法: python3 verify.py
"""
import json
import os
import time
import subprocess

HOME = os.path.expanduser("~")
BASE = f"{HOME}/.openclaw"
PAIRED = f"{BASE}/devices/paired.json"
AUTH = f"{BASE}/identity/device-auth.json"

def green(msg): print(f"\033[92m✓ {msg}\033[0m")
def red(msg): print(f"\033[91m✗ {msg}\033[0m")
def yellow(msg): print(f"\033[93m! {msg}\033[0m")
def info(msg): print(f"  {msg}")

def check_files():
    info("检查配置文件...")
    if not os.path.exists(PAIRED):
        red(f"paired.json 不存在")
        return False
    if not os.path.exists(AUTH):
        red(f"device-auth.json 不存在")
        return False
    with open(PAIRED) as f:
        paired = json.load(f)
    with open(AUTH) as f:
        auth = json.load(f)
    auth_token = auth.get("tokens", {}).get("operator", {}).get("token", "")
    auth_scopes = auth.get("tokens", {}).get("operator", {}).get("scopes", [])

    # Find this device in paired
    from openclaw.identity import device as id_module  # may not exist, use fallback
    device_id = None
    device_json = os.path.expanduser(f"{BASE}/identity/device.json")
    if os.path.exists(device_json):
        with open(device_json) as f:
            device_id = json.load(f).get("deviceId")
    if not device_id:
        # Try to guess from paired
        for k in paired:
            if paired[k].get("clientId") == "gateway-client":
                device_id = k
                break
    if not device_id:
        yellow("无法确定当前设备 ID")
        return False

    if device_id not in paired:
        red(f"设备 {device_id} 不在 paired.json 中")
        return False

    paired_scopes = paired[device_id].get("scopes", [])
    paired_token = paired[device_id].get("tokens", {}).get("operator", {}).get("token", "")
    info(f"Device ID: {device_id}")
    info(f"paired.json token: {paired_token[:15]}...")
    info(f"device-auth token: {auth_token[:15]}...")
    info(f"paired.json scopes: {paired_scopes}")
    info(f"device-auth scopes: {auth_scopes}")

    if "operator.admin" not in paired_scopes:
        red("paired.json 中没有 admin scope")
        return False
    if "operator.admin" not in auth_scopes:
        red("device-auth.json 中没有 admin scope")
        return False
    if paired_token != auth_token:
        red("两个文件的 token 不一致！")
        return False
    green("配置文件 scopes 正确")
    return True

def check_gateway():
    info("检查 Gateway 状态...")
    r = subprocess.run(["openclaw", "gateway", "status"], capture_output=True, text=True)
    if "running" not in r.stdout:
        red("Gateway 未运行")
        return False
    green("Gateway 运行中")
    return True

def check_spawn():
    info("测试 spawn（sessions_spawn）...")
    # Use sessions_spawn via openclaw CLI if possible
    # Actually just check if the token works by querying the gateway
    # Try a lightweight API call
    import socket
    try:
        # Simple probe
        sock = socket.create_connection(("127.0.0.1", 18789), timeout=3)
        sock.close()
        green("Gateway 端口可访问")
    except Exception as e:
        red(f"Gateway 端口不可访问: {e}")
        return False

    # The actual spawn test is done via the sessions_spawn tool call
    # since we're in the agent context
    info("实际 spawn 测试由 sessions_spawn 工具完成")
    info("请在对话中运行: sessions_spawn 测试任务")
    return True

def main():
    print("\n=== 验证修复结果 ===\n")
    ok = True
    if not check_files():
        ok = False
    print()
    if not check_gateway():
        ok = False
    print()
    check_spawn()
    print()
    if ok:
        green("配置文件验证通过")
        print("\n⚠️  必须重启 gateway 才能生效:")
        print("   openclaw gateway restart")
        print("\n重启后等待 5 秒再测试 spawn。")
    else:
        red("配置文件有问题，请重新运行 fix.py")

if __name__ == "__main__":
    main()