# API 消耗优化器 Skill

## 功能
根据 API 剩余调用次数动态调整消耗策略，最大化利用 API 额度。

## 触发场景
- 需要智能消耗 API 调用次数时
- 需要根据剩余次数和时间动态调整调用频率时

## 输入参数
```json
{
  "current_usage": "当前已使用次数",
  "time_window": "时间窗口(如10:00-15:00)",
  "total_quota": "总配额(默认1600)",
  "target_usage": "目标消耗比例(默认0.9，即90%)"
}
```

## 核心逻辑

### 1. 计算重置时间
```python
def get_reset_time(time_window):
    """从时间窗口计算下次重置时间"""
    start_hour = int(time_window.split('-')[0])
    now = datetime.now()
    
    # 下次重置时间
    if now.hour >= start_hour:
        next_reset = now.replace(hour=start_hour) + timedelta(hours=5)
    else:
        next_reset = now.replace(hour=start_hour)
    
    return next_reset
```

### 2. 计算消耗策略
```python
def calculate_consumption_strategy(current_usage, total_quota, time_until_reset):
    """
    根据剩余次数和时间计算最佳消耗策略
    
    策略:
    - 剩余>50%: 保守消耗，保持一定调用
    - 剩余20-50%: 正常消耗
    - 剩余<20%: 冲刺消耗，最大化调用
    - 最后10%时间: 疯狂消耗模式
    """
    remaining = total_quota - current_usage
    remaining_ratio = remaining / total_quota
    
    # 剩余时间比例
    time_ratio = time_until_reset / (5 * 3600)  # 5小时
    
    if time_ratio < 0.1:  # 最后10%时间
        # 疯狂模式 - 每分钟调用
        return {"mode": "crazy", "interval_seconds": 60}
    elif remaining_ratio < 0.2:  # 剩余<20%
        # 冲刺模式 - 每3分钟调用
        return {"mode": "sprint", "interval_seconds": 180}
    elif remaining_ratio < 0.5:  # 剩余<50%
        # 正常模式 - 每10分钟调用
        return {"mode": "normal", "interval_seconds": 600}
    else:
        # 保守模式 - 每30分钟调用
        return {"mode": "conservative", "interval_seconds": 1800}
```

### 3. 动态调整
```python
def adjust_strategy(current_usage, total_quota, elapsed_time):
    """
    实时调整策略
    
    如果当前消耗速度过快/过慢，动态调整
    """
    expected_usage = (elapsed_time / (5*3600)) * total_quota
    speed_ratio = current_usage / max(expected_usage, 1)
    
    if speed_ratio < 0.5:
        # 消耗太慢，加快
        return {"action": "increase_frequency", "factor": 2}
    elif speed_ratio > 1.5:
        # 消耗太快，减缓
        return {"action": "decrease_frequency", "factor": 0.5}
    else:
        return {"action": "maintain"}
```

## 使用示例

### Python 调用
```python
from api_consumption_optimizer import (
    get_reset_time,
    calculate_consumption_strategy,
    adjust_strategy
)
from datetime import datetime, timedelta

# 获取重置时间
time_window = "10:00-15:00"  # 从MiniMax状态获取
reset_time = get_reset_time(time_window)

# 计算当前剩余
current_usage = 800  # 从API获取
total_quota = 1600
time_until_reset = (reset_time - datetime.now()).total_seconds()

# 获取最佳策略
strategy = calculate_consumption_strategy(
    current_usage, 
    total_quota, 
    time_until_reset
)

print(f"当前模式: {strategy['mode']}")
print(f"调用间隔: {strategy['interval_seconds']}秒")

# 启动智能消耗
while True:
    time.sleep(strategy['interval_seconds'])
    do_api_call()
    
    # 每次调用后重新计算
    current_usage += 1
    strategy = calculate_consumption_strategy(...)
```

### 与游戏系统集成
```python
def intelligent_ai_consumer():
    """游戏AI智能消耗器"""
    while True:
        # 获取当前用量
        status = get_minimax_status()
        current_usage = status['today_usage']
        
        # 获取重置时间
        time_window = status['time_window']
        reset_time = get_reset_time(time_window)
        
        # 计算策略
        strategy = calculate_consumption_strategy(
            current_usage=current_usage,
            total_quota=1600,
            time_until_reset=(reset_time - datetime.now()).seconds
        )
        
        # 执行AI调用
        do_game_ai_call()
        
        # 根据策略等待
        time.sleep(strategy['interval_seconds'])
```

## 优势
1. **自适应**: 根据实际剩余次数动态调整
2. **最大化**: 确保在重置前尽可能消耗
3. **不过度**: 不会一次性耗尽，留有余地
4. **可预测**: 用户可以预估消耗速度

## 注意事项
- 需要配合 MiniMax 状态查询使用
- 重置周期默认5小时，可配置
- 建议保留10%缓冲避免突发需求
