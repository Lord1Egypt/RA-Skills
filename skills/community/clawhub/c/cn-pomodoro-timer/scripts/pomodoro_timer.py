#!/usr/bin/env python3
"""cn-pomodoro-timer - 番茄钟计时器"""
import time, sys

def run_pomodoro(work_minutes=25, break_minutes=5, rounds=4):
    """运行番茄钟
    
    标准番茄工作法：
    - 工作25分钟，休息5分钟
    - 每4轮后长休息15-30分钟
    
    Args:
        work_minutes: 工作时长（分钟）
        break_minutes: 短休息时长（分钟）
        rounds: 轮数
    """
    print(f"🍅 番茄钟开始!")
    print(f"   工作: {work_minutes}分钟 | 休息: {break_minutes}分钟 | 轮数: {rounds}")
    print("-" * 40)
    
    for i in range(1, rounds + 1):
        print(f"\n⏱  第 {i}/{rounds} 轮 - 工作中 ({work_minutes}分钟)")
        print("   Ctrl+C 提前结束")
        
        remaining = work_minutes * 60
        while remaining > 0:
            mins = remaining // 60
            secs = remaining % 60
            print(f"\r   剩余: {mins:02d}:{secs:02d}", end='', flush=True)
            time.sleep(1)
            remaining -= 1
        
        print(f"\n\n🔔 时间到！休息 {break_minutes} 分钟")
        
        if i < rounds:
            print("   按回车开始休息...")
        
        remaining = break_minutes * 60
        while remaining > 0:
            mins = remaining // 60
            secs = remaining % 60
            print(f"\r   休息剩余: {mins:02d}:{secs:02d}", end='', flush=True)
            time.sleep(1)
            remaining -= 1
    
    print("\n\n✅ 完成了所有轮次！")
    return True

if __name__ == '__main__':
    run_pomodoro()
