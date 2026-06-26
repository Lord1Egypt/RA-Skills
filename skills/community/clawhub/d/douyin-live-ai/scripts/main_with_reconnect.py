"""
抖音直播弹幕AI回复助手 - 增强版（自动重连）
推荐使用此文件启动，断线后自动重连
"""
import time
import sys
from douyinlive import DouYinLive
from config import ROOM_ID, HOST_NAME


def main():
    print("=" * 60)
    print(f"抖音直播AI回复助手 - {HOST_NAME}")
    print("=" * 60)
    print(f"直播间: https://live.douyin.com/{ROOM_ID}")
    print("AI引擎: DeepSeek")
    print("功能: 实时获取弹幕 → DeepSeek AI生成回复 → 自动重连")
    print("=" * 60)
    print()

    reconnect_count = 0
    max_reconnects = 100  # 最大重连次数
    reconnect_delay = 5   # 重连延迟(秒)

    while reconnect_count < max_reconnects:
        try:
            douyin = DouYinLive(ROOM_ID)
            douyin.start()
        except KeyboardInterrupt:
            print("\n[系统] 用户手动停止程序")
            break
        except Exception as e:
            reconnect_count += 1
            print(f"\n[系统] 连接异常: {str(e)}")
            print(f"[系统] {reconnect_delay}秒后尝试第 {reconnect_count} 次重连...")
            time.sleep(reconnect_delay)
            print(f"[系统] 正在重连...")
            print("=" * 60)

    if reconnect_count >= max_reconnects:
        print("\n[系统] 已达到最大重连次数，程序停止")


if __name__ == "__main__":
    main()
