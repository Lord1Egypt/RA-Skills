"""
抖音直播弹幕AI回复助手 - 程序入口（基础版）
"""
from douyinlive import DouYinLive
from config import ROOM_ID, HOST_NAME
import logging

if __name__ == '__main__':
    # 隐藏不必要的日志
    logging.getLogger('websocket').setLevel(logging.ERROR)
    logging.getLogger('requests').setLevel(logging.ERROR)
    logging.getLogger('urllib3').setLevel(logging.ERROR)

    print("=" * 60)
    print(f"抖音直播AI回复助手 - {HOST_NAME}")
    print("=" * 60)
    print(f"直播间: https://live.douyin.com/{ROOM_ID}")
    print("AI引擎: DeepSeek")
    print("-" * 60)
    print("功能：实时获取弹幕 → DeepSeek AI生成回复")
    print("=" * 60)
    print()

    douyin = DouYinLive(ROOM_ID)
    douyin.start()
