# mempalace-integration

> MemPalace记忆系统集成 - AAAK压缩 + Hall分类 + L0-L3分层

[English](./README.md)

## 概述

集成 MemPalace 核心概念到你的 AI agent 系统：
- **AAAK压缩**：30x无损压缩
- **Hall分类**：facts/events/discoveries/preferences/advice
- **L0-L3分层**：记忆加载优先级

## 核心概念

### AAAK压缩
30x无损压缩。

**格式**: `KEY: VALUE | KEY2: VALUE2`

### Hall分类

| Hall | 内容 |
|------|------|
| hall_facts | 决策、选择 |
| hall_events | 会话、里程碑 |
| hall_discoveries | 新洞察 |
| hall_preferences | 习惯、偏好 |
| hall_advice | 建议 |

### L0-L3分层

| Layer | 内容 | 加载 |
|-------|------|------|
| L0 | 身份(~50) | 始终 |
| L1 | 关键事实(~120) | 始终 |
| L2 | 近期会话 | 按需 |
| L3 | 深度搜索 | 按需 |

## 检索性能

- Wing + Room: **94.8%**

## 使用方法

1. 压缩原始内容
2. 分类到Hall
3. 按L0-L3加载

## 安装

```bash
git clone https://github.com/0xcjl/mempalace-integration.git ~/.hermes/skills/mempalace-integration
```

## 致谢

- **来源**: [MemPalace](https://github.com/milla-jovovich/mempalace)
- **集成**: [0xcjl](https://github.com/0xcjl)

## 许可证

MIT
