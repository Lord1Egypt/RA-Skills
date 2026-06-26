#!/usr/bin/env python3
"""
version_check.py — 检查 crusheart-autobrain-turbo 新版本 v1.0

访问 https://clawhub.ai/plugins/crusheart-autobrain-turbo 检查新版本。
仅在首次安装时运行一次，如果发现了新版本，只提醒一次后记录已提醒状态。
如果没有新版本，不返回任何结果，不发送任何信息。

用法：
  python3 scripts/version_check.py
"""

import json, os, sys, urllib.request, re, hashlib
from datetime import datetime, timezone, timedelta

BEIJING_TZ = timezone(timedelta(hours=8))
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
STATE_FILE = os.path.join(WORKSPACE, ".version_check_state.json")
CURRENT_VERSION = "6.3.1"
CHECK_URL = "https://clawhub.ai/plugins/crusheart-autobrain-turbo"

# 插件槽文件（检测是否已安装）
SLOT_FILE = os.path.join(WORKSPACE, ".crusheart-slot.json")


def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                return json.load(f)
        except: pass
    return {"checks": [], "notified_versions": []}


def save_state(state: dict):
    state["last_check"] = datetime.now(BEIJING_TZ).isoformat()
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


def check_new_version() -> str:
    """检查是否有新版本，返回版本号字符串，None表示无"""
    state = load_state()
    
    # 仅首次安装时检查
    if not os.path.exists(SLOT_FILE):
        return None

    # 已经提醒过的版本不再提醒（用 latest 版本号去重，而非 CURRENT_VERSION）
    notified = state.get("notified_versions", [])

    try:
        req = urllib.request.Request(CHECK_URL, headers={
            "User-Agent": "Mozilla/5.0 (compatible; CrusheartAutoBrain/6.3.1)"
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None  # 网络不可达时静默

    # 尝试从页面提取版本号
    patterns = [
        r'version[="\':\s]*([\d.]+)',
        r'v(\d+\.\d+\.\d+)',
        r'(\d+\.\d+\.\d+)[\s-]*release',
    ]
    found_versions = []
    for p in patterns:
        matches = re.findall(p, html, re.IGNORECASE)
        found_versions.extend(matches)

    # 去重取最高版本
    if found_versions:
        # 标准化版本号
        cleaned = []
        for v in found_versions:
            v = v.strip()
            parts = v.split(".")
            if len(parts) >= 2:
                try:
                    _ = [int(x) for x in parts[:3]]
                    cleaned.append(v)
                except: pass
        if cleaned:
            # 取最大版本
            latest = max(cleaned, key=lambda x: [int(p) for p in x.split(".")[:3]])
            # 比较版本
            latest_parts = [int(p) for p in latest.split(".")[:3]]
            current_parts = [int(p) for p in CURRENT_VERSION.split(".")[:3]]
            
            if latest_parts > current_parts:
                # 标记已提醒（记录的是 latest 版本号，防止重复提醒）
                if latest not in notified:
                    state["notified_versions"].append(latest)
                state["checks"].append({
                    "time": datetime.now(BEIJING_TZ).isoformat(),
                    "current": CURRENT_VERSION,
                    "latest": latest,
                    "found": True
                })
                save_state(state)
                return latest

    # 无新版本：不记录任何状态变更，不返回任何结果
    return None


if __name__ == "__main__":
    result = check_new_version()
    if result:
        # 仅当有新版本时才输出和返回
        msg = f"发现新版本: {result}（当前: {CURRENT_VERSION}），请前往 {CHECK_URL} 查看更新。"
        print(json.dumps({"has_update": True, "latest_version": result, "current": CURRENT_VERSION, "message": msg}))
    # 无新版本时不输出任何内容
