#!/usr/bin/env python3
"""
修复 CLI 设备 scope：把 pending repair 请求的完整 scopes 写入 paired.json
用法:
  python3 fix.py              # 自动检测设备，交互确认后执行
  python3 fix.py --dry-run    # 仅展示改动，不写入
  python3 fix.py --force      # 跳过确认直接执行（自动化场景）
  python3 fix.py <device_id>  # 手动指定设备 ID
"""
import json
import os
import sys
import shutil
import secrets
from datetime import datetime

HOME = os.path.expanduser("~")
BASE = f"{HOME}/.openclaw"
PAIRED = f"{BASE}/devices/paired.json"
PENDING = f"{BASE}/devices/pending.json"
AUTH = f"{BASE}/identity/device-auth.json"

# 默认完整 scopes（如果找不到 pending 请求且未指定 device_id，用这个）
FALLBACK_SCOPES = [
    "operator.admin",
    "operator.read",
    "operator.write",
    "operator.approvals",
    "operator.pairing",
    "operator.talk.secrets",
]

def green(msg): print(f"\033[92m{msg}\033[0m")
def red(msg): print(f"\033[91m{msg}\033[0m")
def yellow(msg): print(f"\033[93m{msg}\033[0m")
def info(msg): print(f"  {msg}")

def find_device_id_from_pending():
    """从 pending repair 请求获取设备 ID"""
    if not os.path.exists(PENDING):
        return None, None
    with open(PENDING) as f:
        pending = json.load(f)
    for req in pending.values():
        if req.get("isRepair"):
            return req.get("deviceId"), req.get("scopes", FALLBACK_SCOPES)
    return None, None

def find_cli_device_from_paired():
    """从 paired.json 自动找 CLI 设备"""
    with open(PAIRED) as f:
        paired = json.load(f)
    for k, v in paired.items():
        client_id = v.get("clientId", "")
        platform = v.get("platform", "")
        scopes = v.get("scopes", [])
        # 匹配 CLI 设备特征
        if ("cli" in client_id.lower() or "gateway-client" in client_id) and platform.lower() in ["linux", "unknown"]:
            if "operator.admin" not in scopes:
                return k, v
    return None, None

def show_changes(device_id, old_scopes, new_scopes, new_token, dry_run=False):
    """展示即将进行的改动"""
    print(f"\n{'='*50}")
    print(f"{'DRY RUN - 不会写入文件' if dry_run else '即将执行的改动'}")
    print(f"{'='*50}\n")
    info(f"Device ID: {device_id}")
    info(f"当前 scopes: {old_scopes}")
    green(f"新 scopes: {new_scopes}")
    info(f"新 token: {new_token[:20]}...")
    print(f"\n将修改的文件:")
    info(f"  - paired.json (更新设备 scopes + token)")
    info(f"  - device-auth.json (更新本地 token)")
    info(f"  - pending.json (清理 repair 请求)")
    print()

def confirm():
    """等待用户确认"""
    try:
        resp = input("\033[93m❓ Proceed? [y/N]: \033[0m").strip().lower()
        return resp in ["y", "yes"]
    except EOFError:
        return False

def fix(device_id, full_scopes, dry_run=False, force=False):
    """执行修复"""
    new_token = f"cli_admin_{secrets.token_urlsafe(20)}"
    ts = int(datetime.now().timestamp() * 1000)

    # Read current state
    with open(PAIRED) as f:
        paired = json.load(f)
    with open(AUTH) as f:
        auth = json.load(f)

    if device_id not in paired:
        red(f"设备 {device_id} 不在 paired.json 中！")
        red(f"可用设备: {list(paired.keys())}")
        sys.exit(1)

    old_scopes = paired[device_id].get("scopes", [])

    # Show changes first (检查点！)
    show_changes(device_id, old_scopes, full_scopes, new_token, dry_run=dry_run)

    if dry_run:
        yellow("DRY RUN 模式 - 未写入任何文件")
        print("\n如需执行，运行: python3 fix.py")
        return

    # 检查点：用户确认
    if not force:
        if not confirm():
            yellow("已取消，未做任何改动")
            return

    # Backup
    for f, label in [(PAIRED, "paired.json"), (AUTH, "device-auth.json")]:
        bak = f"{f}.bak.{datetime.now().strftime('%Y%m%d%H%M%S')}"
        shutil.copy(f, bak)
        info(f"备份: {bak}")

    # Update paired.json
    paired[device_id]["scopes"] = full_scopes
    paired[device_id]["approvedScopes"] = full_scopes
    paired[device_id]["tokens"] = {
        "operator": {
            "token": new_token,
            "role": "operator",
            "scopes": full_scopes,
            "createdAtMs": ts,
        }
    }
    with open(PAIRED, "w") as f:
        json.dump(paired, f, indent=2)
    green(f"✓ paired.json 已更新")

    # Update device-auth.json
    auth["tokens"]["operator"]["token"] = new_token
    auth["tokens"]["operator"]["scopes"] = full_scopes
    auth["tokens"]["operator"]["updatedAtMs"] = ts
    with open(AUTH, "w") as f:
        json.dump(auth, f, indent=2)
    green("✓ device-auth.json 已更新")

    # Clean pending
    if os.path.exists(PENDING):
        with open(PENDING) as f:
            pending = json.load(f)
        keys_deleted = []
        for k, v in list(pending.items()):
            if v.get("deviceId") == device_id:
                keys_deleted.append(k)
        for k in keys_deleted:
            del pending[k]
        with open(PENDING, "w") as f:
            json.dump(pending, f, indent=2)
        if keys_deleted:
            info(f"已清理 pending 请求: {keys_deleted}")

    print(f"\n\033[92m✓ 修复完成！\033[0m")
    print(f"\n下一步：重启 gateway 加载新配置")
    print(f"  openclaw gateway restart")
    print(f"\n验证（重启后等待 5 秒）:")
    print(f"  python3 scripts/verify.py")

def main():
    # Parse args
    dry_run = "--dry-run" in sys.argv
    force = "--force" in sys.argv
    target_device_id = None

    for arg in sys.argv[1:]:
        if arg not in ["--dry-run", "--force", "--help"]:
            target_device_id = arg

    if "--help" in sys.argv:
        print(__doc__)
        sys.exit(0)

    # Find device to fix
    scopes = FALLBACK_SCOPES

    if target_device_id:
        info(f"指定设备: {target_device_id}")
    else:
        info("自动检测需要修复的设备...")
        device_id, pending_scopes = find_device_id_from_pending()
        if device_id:
            target_device_id = device_id
            scopes = pending_scopes
            green(f"从 pending repair 获取: {device_id}")
        else:
            # Fallback: find from paired.json
            device_id, device_info = find_cli_device_from_paired()
            if device_id:
                target_device_id = device_id
                green(f"从 paired.json 找到: {device_id}")
                yellow(f"无 pending repair，使用 fallback scopes")
            else:
                red("无法自动找到需要修复的设备")
                red("手动指定: python3 fix.py <device_id>")
                sys.exit(1)

    print(f"\n  目标 scopes: {scopes}")

    fix(target_device_id, scopes, dry_run=dry_run, force=force)

if __name__ == "__main__":
    main()