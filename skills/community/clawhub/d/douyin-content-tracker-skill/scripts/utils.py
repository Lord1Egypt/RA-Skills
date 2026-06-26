"""
utils.py — 跨模块共用工具函数
"""
from __future__ import annotations

import pandas as pd


def video_id_from_url(url: str) -> str:
    """从抖音视频链接中提取视频 ID"""
    return str(url).rstrip("/").split("/")[-1].split("?")[0]


def compute_engagement_rate(df: pd.DataFrame) -> pd.Series:
    """计算互动率：(点赞+评论+转发) / max(播放,1) × 100，保留两位小数"""
    return (
        (df["点赞"] + df["评论"] + df["转发"])
        / df["播放"].replace(0, 1) * 100
    ).round(2)
