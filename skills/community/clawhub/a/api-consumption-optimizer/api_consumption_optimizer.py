#!/usr/bin/env python3
"""
API 消耗优化器
根据 MiniMax API 剩余调用次数动态调整消耗策略
"""

from datetime import datetime, timedelta
import json
import subprocess
import time
import threading
import random


def get_minimax_status():
    """获取 MiniMax 当前状态"""
    try:
        result = subprocess.run(
            ['/home/garfield/.local/bin/minimax-status-clean'],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout
        
        # 解析输出
        usage = {}
        for line in output.split('\n'):
            if '当前模型' in line:
                usage['model'] = line.split(':')[1].strip()
            elif '时间窗口' in line:
                # 提取时间窗口 10:00-15:00(UTC+8)
                time_str = line.split(':')[1].split('(')[0].strip()
                usage['time_window'] = time_str
            elif '今日消耗' in line:
                # 提取数字
                import re
                nums = re.findall(r'\d+', line)
                if nums:
                    usage['today_usage'] = int(nums[0])
            elif '已用额度' in line:
                import re
                nums = re.findall(r'\d+', line.split('%')[0])
                if nums:
                    usage['usage_percent'] = int(nums[0])
        
        return usage
    except Exception as e:
        print(f"获取状态失败: {e}")
        return {}


def get_next_reset_time(time_window):
    """计算下次重置时间"""
    now = datetime.now()
    
    if not time_window:
        # 默认 10:00
        start_hour = 10
    else:
        start_hour = int(time_window.split('-')[0])
    
    # 下次重置时间
    if now.hour >= start_hour:
        # 下一轮 (加上5小时)
        next_reset = now.replace(hour=start_hour, minute=0, second=0) + timedelta(hours=5)
    else:
        # 今天
        next_reset = now.replace(hour=start_hour, minute=0, second=0)
    
    return next_reset


def calculate_consumption_strategy(current_usage, total_quota=1600, time_until_reset=0):
    """
    根据剩余次数和时间计算最佳消耗策略
    """
    remaining = max(total_quota - current_usage, 0)
    remaining_ratio = remaining / total_quota
    
    # 如果没有传入时间，计算
    if time_until_reset <= 0:
        return {"mode": "conservative", "interval_seconds": 1800, "reason": "unknown"}
    
    # 剩余时间比例 (5小时 = 18000秒)
    time_ratio = time_until_reset / 18000
    
    # 计算理想消耗速度
    ideal_rate = remaining / time_until_reset  # 每秒应该消耗多少次
    
    if time_ratio < 0.1:  # 最后10%时间 (<30分钟)
        return {
            "mode": "crazy",
            "interval_seconds": 60,  # 每分钟
            "calls_per_minute": 1,
            "reason": f"最后{int(time_ratio*100)}%时间，冲刺模式"
        }
    elif remaining_ratio < 0.2:  # 剩余<20%
        return {
            "mode": "sprint",
            "interval_seconds": 180,  # 每3分钟
            "calls_per_minute": 0.33,
            "reason": f"剩余{int(remaining_ratio*100)}%，冲刺消耗"
        }
    elif remaining_ratio < 0.5:  # 剩余<50%
        return {
            "mode": "normal",
            "interval_seconds": 600,  # 每10分钟
            "calls_per_minute": 0.1,
            "reason": f"剩余{int(remaining_ratio*100)}%，正常消耗"
        }
    else:
        return {
            "mode": "conservative",
            "interval_seconds": 1800,  # 每30分钟
            "calls_per_minute": 0.033,
            "reason": f"剩余{int(remaining_ratio*100)}%，保守消耗"
        }


class APIConsumptionOptimizer:
    """API消耗优化器类"""
    
    def __init__(self, total_quota=1600):
        self.total_quota = total_quota
        self.last_status = {}
        self.current_strategy = {}
        
    def refresh_status(self):
        """刷新API状态"""
        self.last_status = get_minimax_status()
        return self.last_status
    
    def calculate_strategy(self):
        """计算当前最佳策略"""
        status = self.refresh_status()
        
        if not status or 'today_usage' not in status:
            return {
                "mode": "conservative",
                "interval_seconds": 1800,
                "reason": "无法获取状态"
            }
        
        current_usage = status.get('today_usage', 0)
        time_window = status.get('time_window', '10:00-15:00')
        
        # 计算下次重置
        reset_time = get_next_reset_time(time_window)
        now = datetime.now()
        
        if now >= reset_time:
            # 已重置
            time_until_reset = 5 * 3600
        else:
            time_until_reset = (reset_time - now).total_seconds()
        
        # 计算策略
        self.current_strategy = calculate_consumption_strategy(
            current_usage,
            self.total_quota,
            time_until_reset
        )
        
        # 添加状态信息
        self.current_strategy['current_usage'] = current_usage
        self.current_strategy['remaining'] = self.total_quota - current_usage
        self.current_strategy['reset_time'] = reset_time.isoformat()
        self.current_strategy['time_until_reset'] = int(time_until_reset)
        
        return self.current_strategy
    
    def get_interval(self):
        """获取当前调用间隔"""
        strategy = self.calculate_strategy()
        return strategy.get('interval_seconds', 1800)
    
    def get_status_summary(self):
        """获取状态摘要"""
        strategy = self.calculate_strategy()
        return f"""📊 API消耗状态:
- 已用: {strategy.get('current_usage', '?')}/{self.total_quota}
- 剩余: {strategy.get('remaining', '?')}
- 模式: {strategy.get('mode', '?')}
- 间隔: {strategy.get('interval_seconds', '?')}秒
- 原因: {strategy.get('reason', '')}
- 下次重置: {strategy.get('reset_time', '?')}"""


# 全局优化器实例
optimizer = APIConsumptionOptimizer(total_quota=1600)


# 测试用
if __name__ == "__main__":
    opt = APIConsumptionOptimizer()
    
    # 获取当前状态
    print(opt.get_status_summary())
    
    # 获取调用间隔
    interval = opt.get_interval()
    print(f"\n建议调用间隔: {interval}秒")
