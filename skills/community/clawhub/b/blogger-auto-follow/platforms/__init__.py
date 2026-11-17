# -*- coding: utf-8 -*-
"""
多平台注册与工厂模块
"""

from .base import BasePlatform
from .douyin import DouyinPlatform
from .bilibili import BilibiliPlatform
from .xiaohongshu import XiaohongshuPlatform
from .x_twitter import XPlatform
from .youtube import YouTubePlatform

PLATFORMS = {
    "douyin": DouyinPlatform(),
    "tiktok": DouyinPlatform(),
    "bilibili": BilibiliPlatform(),
    "b站": BilibiliPlatform(),
    "xiaohongshu": XiaohongshuPlatform(),
    "red": XiaohongshuPlatform(),
    "小红书": XiaohongshuPlatform(),
    "x": XPlatform(),
    "twitter": XPlatform(),
    "推特": XPlatform(),
    "youtube": YouTubePlatform(),
    "油管": YouTubePlatform(),
}

def get_platform(name: str) -> BasePlatform:
    key = name.strip().lower()
    return PLATFORMS.get(key, None)

def supported_platform_names():
    return [
        "douyin (抖音)",
        "xiaohongshu (小红书)",
        "bilibili (哔哩哔哩/B站)",
        "x (Twitter/推特)",
        "youtube (YouTube/油管)"
    ]
