#!/usr/bin/env python3
import json
import shutil
import sys
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"
BACKUP_PATH = CONFIG_PATH.with_suffix(".json.bak")

ALLOWED_FIELDS = {"enabled", "appId", "appSecret", "dmPolicy", "allowlist"}

def clean_channel(channel):
    if not isinstance(channel, dict):
        return channel
    return {k: v for k, v in channel.items() if k in ALLOWED_FIELDS}

def is_full_channel(channel):
    return bool(channel.get("appId") and channel.get("appSecret"))

def main():
    if not CONFIG_PATH.exists():
        print(f"❌ 未找到配置文件: {CONFIG_PATH}")
        return 1

    shutil.copy2(CONFIG_PATH, BACKUP_PATH)
    print(f"✅ 已备份到: {BACKUP_PATH}")

    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        config = json.load(f)

    channels = config.get("channels", {})
    feishu = channels.get("feishu")
    openclaw_feishu = channels.get("openclaw-feishu")

    if not feishu or not openclaw_feishu:
        print("✅ 未检测到频道冲突，无需清理")
        return 0

    feishu_full = is_full_channel(feishu)
    openclaw_feishu_full = is_full_channel(openclaw_feishu)

    if feishu_full and not openclaw_feishu_full:
        keep_key, remove_key = 'feishu', 'openclaw-feishu'
        print("🔍 保留完整配置的 feishu")
    elif openclaw_feishu_full and not feishu_full:
        keep_key, remove_key = 'openclaw-feishu', 'feishu'
        print("🔍 保留完整配置的 openclaw-feishu")
    else:
        keep_key, remove_key = 'openclaw-feishu', 'feishu'
        print("⚠️ 默认保留 openclaw-feishu")

    keep_channel = channels[keep_key]
    remove_channel = channels[remove_key]

    keep_channel = clean_channel(keep_channel)

    if "allowlist" in remove_channel:
        old = keep_channel.get("allowlist", [])
        new = remove_channel["allowlist"]
        merged = list(set(old + new))
        keep_channel["allowlist"] = merged
        print(f"✅ 合并白名单: {merged}")

    if "dmPolicy" in remove_channel:
        keep_channel["dmPolicy"] = remove_channel["dmPolicy"]
        print(f"✅ 设置 dmPolicy: {keep_channel['dmPolicy']}")

    keep_channel["enabled"] = True

    channels[keep_key] = keep_channel
    del channels[remove_key]
    config["channels"] = channels

    with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print("✅ 配置文件已更新")

    print("\n⚠️ 请执行: openclaw gateway restart\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
