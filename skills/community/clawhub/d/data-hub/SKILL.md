---
name: data-hub
description: "数字货币量化交易系统的内存数据中枢，为多 Agent 提供统一的数据共享层。管理行情(market_state)、指标(indicators)、情报(intelligence)、风控(risk_audit)四个命名空间。Use when: Agent 需要读写共享数据、查询行情/指标/研报/风控状态。NOT for: 持久化存储、历史数据查询、直接下单交易。"
---

# Data Hub Skill

多 Agent 数字货币量化交易系统的内存数据共享中枢。

## When to Use

- Agent 需要写入或读取行情、指标、情报、风控状态
- 编排器(Orchestrator)推送最新行情和技术指标
- 分析官(Analyst)发布研报情报
- 风控卫士(Guard)更新全局风控状态
- 任意 Agent 调用 `get_summary()` 获取全局数据快照

## When NOT to Use

- 需要持久化历史数据 → 使用数据库
- 直接执行交易下单 → 使用交易 Skill
- 获取实时行情源数据 → 使用行情 API Skill

## 依赖

```python
import time, json, asyncio
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field, ValidationError
```

## 数据模型

所有写入数据必须通过 Pydantic 校验，防止 LLM 幻觉导致脏数据。

```python
# 行情数据
class MarketDataModel(BaseModel):
    last_price: float = Field(..., gt=0, description="最新成交价")
    volume_24h: float = Field(default=0.0, ge=0)
    timestamp: float = Field(default_factory=time.time)

# 情报数据（带 TTL）
class IntelligenceModel(BaseModel):
    author: str = Field(..., description="研报生成者ID")
    content: str = Field(..., description="研报正文内容")
    ttl_seconds: int = Field(default=1800, description="数据有效时长(秒)，默认30分钟")
    created_at: float = Field(default_factory=time.time)

# 风控状态
class RiskAuditModel(BaseModel):
    global_lock: bool = Field(default=False, description="是否触发全局爆仓保护，若为True则拦截开仓")
    max_position_allowance: float = Field(..., ge=0, description="当前允许的最大下单量(U或币本位)")
    current_drawdown: float = Field(default=0.0, description="当前账户回撤比例")

# 指标数据：Dict[str, List[float]]，通过代码逻辑限制滑动窗口上限 50
```

## 内存命名空间

`self._memory` 采用三级树状结构：`category → key → value`

| 命名空间 | Key | Value 类型 | 写入权限 (Agent_ID) | 维护策略 |
|----------|-----|-----------|-------------------|---------|
| `market_state` | symbol (如 `BTC_USDT`) | dict (MarketDataModel) | `Default_Orchestrator` | 覆盖式更新 |
| `indicators` | symbol | `Dict[str, List[float]]` | `Default_Orchestrator` | 滑动窗口 (上限 50) |
| `intelligence` | symbol | dict (IntelligenceModel) | `Analyst_Officer` | TTL 自动过期清除 |
| `risk_audit` | `"global_state"` | dict (RiskAuditModel) | `Guard_Agent` | 覆盖式更新 + 持久化快照 |

## 核心 API

### push_data — 写入数据

```python
async def push_data(self, agent_id: str, category: str, key: str, data: dict) -> dict:
```

调用示例：

```python
# 编排器推送行情
await hub.push_data("Default_Orchestrator", "market_state", "BTC_USDT", {
    "last_price": 65000.5,
    "volume_24h": 1234567.89
})

# 编排器推送指标
await hub.push_data("Default_Orchestrator", "indicators", "BTC_USDT", {
    "rsi": [45.2, 48.1, 52.3],
    "ma20": [64800.0, 64950.0, 65100.0]
})

# 分析官发布研报
await hub.push_data("Analyst_Officer", "intelligence", "BTC_USDT", {
    "author": "Analyst_Officer",
    "content": "BTC 短期看涨，建议轻仓做多",
    "ttl_seconds": 1800
})

# 风控卫士更新状态
await hub.push_data("Guard_Agent", "risk_audit", "global_state", {
    "global_lock": False,
    "max_position_allowance": 10000.0,
    "current_drawdown": 0.05
})
```

### get_summary — 读取全局快照（触发懒惰清理）

```python
await hub.get_summary()
```

## 规则

### 1. 写入权限隔离

每个命名空间只允许指定的 Agent 写入。错误的 agent_id 会被拒绝并返回错误信息，不会抛出异常。

### 2. 异步锁约束

所有 `self._memory` 读写必须在 `async with self._lock:` 内执行。**锁内禁止任何网络 IO**，只允许纯 CPU 的字典级读写，防止死锁。

### 3. LLM 友好型报错

绝不抛出 Exception 中断进程。捕获 `ValidationError` 后返回结构化英文错误信息，引导 LLM 自我纠错：

```
[VALIDATION_ERROR] Expected float for 'last_price', got string. Please fix and retry.
[PERMISSION_DENIED] Agent 'Analyst_Officer' cannot write to 'market_state'. Only 'Default_Orchestrator' is authorized.
```

### 4. 懒惰清理（Lazy Janitor）

不后台轮询，在 `get_summary()` 时按需清理：

- **行情陈旧检测**：`now() - timestamp > 10秒` → 标记 `is_stale = True`
- **情报过期检测**：`now() - created_at > ttl_seconds` → 内容替换为 `"[EXPIRED] Analyst report is outdated."`

### 5. 滑动窗口

`indicators` 命名空间对每个指标键维护 FIFO 队列，上限 50 条。超出时丢弃最早的数据。
