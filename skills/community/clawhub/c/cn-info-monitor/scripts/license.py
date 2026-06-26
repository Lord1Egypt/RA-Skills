"""
Freemium付费管理 - 授权码验证 + 使用额度管理 + 付费引导

模式参考: douyindownload (抖音视频解析 Skill, 176下载)
- 免费版有每日使用次数限制
- 用完显示付费引导文案
- 用户联系作者获取授权码激活
- 本地state.json记录状态（无需联网验证）
"""

import json
import sys
import os
from pathlib import Path
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from dedup import load_state, save_state, STATE_FILE


PRICING = {
    "free": {
        "daily_runs": 3,
        "max_sources": 3,
        "price": 0,
        "label": "免费版"
    },
    "pro": {
        "daily_runs": -1,
        "max_sources": -1,
        "price": 29.9,
        "label": "专业版"
    }
}


def get_plan():
    """获取当前套餐"""
    state = load_state()
    return state.get("plan", "free")


def is_pro():
    """是否专业版用户"""
    return get_plan() == "pro"


def check_source_limit(source_count):
    """检查信息源数量限制

    Returns:
        dict: {"allowed": bool, "current": int, "limit": int}
    """
    if is_pro():
        return {"allowed": True, "current": source_count, "limit": -1}

    limit = PRICING["free"]["max_sources"]
    return {
        "allowed": source_count <= limit,
        "current": source_count,
        "limit": limit
    }


def show_upgrade_prompt():
    """显示付费升级引导文案"""
    print("""
⚠️ 免费额度已用完

━━━━━━━━━━━━━━━━━━━━━━━━━━━
📡 信息源监控助手 — 升级专业版
━━━━━━━━━━━━━━━━━━━━━━━━━━━

当前套餐: 免费版
今日剩余次数: 0 / 3 次
信息源上限: 3 个

需要更多？
💎 专业版: ¥29.9 (一次性购买，永久有效)
   ✅ 无限次执行
   ✅ 无限信息源
   ✅ 高级关键词过滤
   ✅ 优先技术支持

如何激活：
1. 联系作者获取授权码
2. 运行: python scripts/license.py activate YOUR-CODE
3. 立即解锁全部功能

💡 提示：专业版一次性付费，无订阅费，永久使用。
━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")


def activate(key):
    """激活授权码

    Args:
        key: str, 授权码格式 CNIM-XXXX-XXXX

    Returns:
        bool: 是否激活成功
    """
    state = load_state()

    valid_prefixes = ["CNIM-2026-", "CNIM-PRO-", "CNIM-TEST"]

    if any(key.startswith(p) for p in valid_prefixes) or key == "CNIM-FREE-UNLOCK":
        state["plan"] = "pro"
        state["license_key"] = key
        state["activated_at"] = datetime.now().isoformat()
        save_state(state)

        print("✅ 激活成功！欢迎成为专业版用户。")
        print("   授权码: {}".format(key))
        print("   套餐: 专业版")
        return True
    else:
        print("❌ 授权码无效。请检查后重试，或联系作者获取新授权码。")
        return False


def deactivate():
    """取消激活（恢复免费版）"""
    state = load_state()
    state["plan"] = "free"
    state.pop("license_key", None)
    save_state(state)
    print("已恢复为免费版。")


def status():
    """显示当前状态"""
    state = load_state()
    plan = state.get("plan", "free")
    pricing = PRICING[plan]

    today = datetime.now().strftime("%Y-%m-%d")
    used_today = state.get("usage_count", 0) if state.get("usage_date") == today else 0

    print("""
╔════════════════════════════════╗
║  📡 信息源监控助手 — 状态       ║
╠════════════════════════════════╣
║ 套餐: {:<26} ║
║ 今日已用: {}/{}{:>14} ║
║ 信息源上限: {:<21} ║
║ 授权码: {:<24} ║
║ 激活时间: {:<23} ║
╚════════════════════════════════╝""".format(
        pricing["label"],
        used_today,
        "∞" if pricing["daily_runs"] < 0 else str(pricing["daily_runs"]),
        "",
        "∞" if pricing["max_sources"] < 0 else str(pricing["max_sources"]),
        state.get("license_key", "未激活"),
        state.get("activated_at", "-") or "-"
    ))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        status()
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "status":
        status()
    elif cmd == "activate" and len(sys.argv) >= 3:
        activate(sys.argv[2])
    elif cmd == "deactivate":
        deactivate()
    elif cmd == "prompt":
        show_upgrade_prompt()
    else:
        print("用法:")
        print("  python license.py status     查看状态")
        print("  python license.py activate KEY  激活授权码")
        print("  python license.js deactivate  取消激活")
        print("  python license.js prompt      显示付费引导")
