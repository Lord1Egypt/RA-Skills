# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

Data Hub 是一个 Python 异步内存数据中枢（Skill），服务于 LLM 驱动的多 Agent 交易系统。它负责在多个 Agent（编排器、分析官、风控卫士等）之间统一管理行情、指标、情报和风控状态数据。

## 技术栈

- Python 3.x + asyncio
- Pydantic（数据校验与序列化）
- 异步读写锁（`asyncio.Lock`）

## 架构要点

### 内存命名空间（三级树状结构）

`self._memory` 按 category → symbol → value 组织，四个命名空间有严格的写入权限隔离：

| 命名空间 | 写入者 | 更新策略 |
|----------|--------|----------|
| `market_state` | Default_Orchestrator | 覆盖式更新 |
| `indicators` | Default_Orchestrator | 滑动窗口（上限 50） |
| `intelligence` | Analyst_Officer | TTL 自动过期（默认 30 分钟） |
| `risk_audit` | Guard_Agent | 覆盖式更新 + 持久化快照 |

### 核心设计原则

1. **Pydantic 强校验**：所有写入数据必须通过 `MarketDataModel`、`IntelligenceModel`、`RiskAuditModel` 校验，防止 LLM 幻觉导致脏数据
2. **异步锁约束**：所有 `self._memory` 读写必须在 `async with self._lock:` 内；锁内禁止网络 IO
3. **LLM 友好型报错**：捕获 `ValidationError` 后返回结构化英文错误信息（如 `[VALIDATION_ERROR] ...`），不抛异常中断进程
4. **懒惰清理（Lazy Janitor）**：在 `get_summary()` 时执行数据清理——行情超 10 秒标记 `is_stale`，情报超 TTL 替换为 `[EXPIRED]`

## 开发规范

- 使用中文进行沟通和注释
- 数据模型变更须同步更新 `docs/Data_Hub_Skill.md` 规范文档
- `indicators` 命名空间使用 `Dict[str, List[float]]` 类型，通过代码逻辑限制滑动窗口大小
