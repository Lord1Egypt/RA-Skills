"""
BiliYouTik2Brain — 灰度发布通道 (v4.0)

用户可选 stable（稳定版）/ beta（尝鲜版）。
stable 只收大版本，beta 可收小修复和实验功能。
"""

import os
import json
from typing import Dict, Optional

_VERSION_FILE = os.path.expanduser("~/.biliyoutik2brain/version_config.json")


def get_channel() -> str:
    """获取当前更新通道

    Returns:
        "stable" or "beta"
    """
    if os.path.exists(_VERSION_FILE):
        with open(_VERSION_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return data.get("channel", "stable")
    return "stable"


def set_channel(channel: str):
    """设置更新通道

    Args:
        channel: "stable" or "beta"
    """
    if channel not in ("stable", "beta"):
        raise ValueError(f"无效通道: {channel}，可选: stable, beta")

    os.makedirs(os.path.dirname(_VERSION_FILE), exist_ok=True)
    with open(_VERSION_FILE, "w", encoding="utf-8") as f:
        json.dump({"channel": channel}, f, ensure_ascii=False, indent=2)


def get_version() -> Dict:
    """获取当前版本信息"""
    return {
        "version": "4.0.0-dev",
        "channel": get_channel(),
        "commit": "3c8ac78",
    }


def check_for_updates() -> Optional[Dict]:
    """检查是否有可用更新

    Returns:
        None（无更新）或 {version, channel, changes, download_url}
    """
    # TODO: 实际实现需要查询 ClawHub API
    # 这里只做框架
    current = get_version()
    channel = current["channel"]

    # 模拟：beta 通道有更多更新
    if channel == "beta":
        return {
            "version": "4.0.0-beta.1",
            "channel": "beta",
            "changes": ["实验功能: 新 OCR 引擎", "修复: 抖音评论抓取"],
            "download_url": "clawhub update biliyoutik2brain --channel beta",
        }

    return None


def get_channel_info() -> Dict:
    """获取通道信息"""
    return {
        "stable": {
            "description": "稳定版，只收大版本更新",
            "update_frequency": "低（每月）",
            "risk": "低",
        },
        "beta": {
            "description": "尝鲜版，包含小修复和实验功能",
            "update_frequency": "高（每周）",
            "risk": "中",
        },
    }
