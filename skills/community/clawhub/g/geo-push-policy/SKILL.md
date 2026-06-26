# geo-push-policy

推送策略管理技能。负责事件冷却期、观察池、频率限制等推送策略管理。

## 功能

- **事件冷却期**: 防止同一事件短时间内重复推送
- **观察池机制**: 评分 50-69 的事件进入观察池，等待确认后再推送
- **推送次数限制**: 单事件最多推送 3 次
- **事件状态机**: 追踪事件从 new → escalating → ongoing → resolved 的演化
- **频率限制保护**: 检测飞书频率限制，自动等待重试
- **死信队列**: 记录推送失败的消息，支持后续补投

## 冷却期配置

| 事件级别 | 冷却时间 | 突破条件 |
|:---|:---|:---|
| 高优先级 (≥70 分) | 90 分钟 | 级别升级、新增权威来源、市场联动扩大 |
| 中优先级 (50-69 分) | 180 分钟 | 同上 |

## 观察池机制

- **进入条件**: 评分 50-69 分
- **池大小限制**: 最多 20 条
- **升级检测**: 观察池事件评分上升至≥70 分时转为推送

## 推送决策流程

```
新闻 → 评分 → 是否≥50 分？
         ↓ 否
         忽略
         ↓ 是
    检查冷却期 → 是否在冷却期？
         ↓ 是           ↓ 否
    检查是否升级      推送
         ↓ 是
        推送
```

## 使用方法

### Python API

```python
from geo_push_policy import (
    PushPolicy,
    AppState,
    should_push_event,
    update_event_cache,
    update_watch_pool,
)

# 加载状态
state = AppState.load(STATE_FILE)

# 创建策略
policy = PushPolicy(
    cooldown_high=90,
    cooldown_medium=180,
    max_push_count=3,
)

# 判断是否推送
should_push, reason = policy.should_push(event, state)
print(f"推送决策：{reason}")

# 更新事件缓存
push_events = [event1, event2]  # 本次推送的事件
update_event_cache(state, all_events, push_events)

# 更新观察池
update_watch_pool(state, all_events, push_events)

# 保存状态
state.save(STATE_FILE)
```

### 状态文件结构

```json
{
  "last_run_time": "2026-03-27T15:00:00",
  "last_push_time": "2026-03-27T14:00:00",
  "event_cache": {
    "event_id_1": {
      "event_id": "event_id_1",
      "fingerprint": "abc123",
      "title": "事件标题",
      "severity": "high",
      "first_seen": "2026-03-27T10:00:00",
      "last_seen": "2026-03-27T15:00:00",
      "push_count": 2,
      "stage": "ongoing"
    }
  },
  "watch_pool": [...],
  "dead_letter_queue": [...]
}
```

## 死信队列

推送失败的消息会进入死信队列，最多保留 10 条。下次运行时会尝试补投。

```python
# 处理死信队列
from geo_push_policy import process_dead_letter_queue, send_to_feishu

success = process_dead_letter_queue(state, send_to_feishu)
if success:
    print("✅ 死信补投成功")
```

## 依赖

- `geo_push_ops`: 推送操作模块（可选，用于死信补投）

## 相关文件

- 主模块：`geo_push_policy.py`

## 版本

- **v1.0.0**: 初始版本，从 smart-geo-push.py v2.0 拆分
