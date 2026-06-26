#!/usr/bin/env python3
"""Abby's Watch - Simple time display"""

import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description="Abby's Watch")
    parser.add_argument("--verbose", action="store_true", help="详细输出")
    parser.add_argument("--countdown", type=str, help="倒计时到指定时间 (HH:MM)")
    
    args = parser.parse_args()
    now = datetime.now()
    
    if args.countdown:
        try:
            target = datetime.strptime(args.countdown, "%H:%M").replace(
                year=now.year, month=now.month, day=now.day
            )
            diff = target - now
            if diff.total_seconds() < 0:
                diff = diff.replace(day=now.day + 1)
            hours = int(diff.total_seconds() // 3600)
            minutes = int((diff.total_seconds() % 3600) // 60)
            print(f"⏰ {hours}小时{minutes}分钟后")
        except ValueError:
            print("❌ 格式错误，请使用 HH:MM 格式")
    elif args.verbose:
        print(f"🕐 {now.strftime('%A, %B %d, %Y')} — {now.strftime('%I:%M %p')} (Australia/Sydney)")
    else:
        print(f"🕐 {now.strftime('%H:%M')}")

if __name__ == "__main__":
    main()
