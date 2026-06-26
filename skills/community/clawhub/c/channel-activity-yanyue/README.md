# 短期记忆 Skill

## 📝 概述

**名称**: short-term-memory  
**版本**: 1.0.0  
**作者**: 炎月  
**创建时间**: 2026-03-08

**功能**: 1分钟临时记忆缓存，用于多通道信息整合

---

## 🎯 核心特性

### ✨ 主要功能
- **临时缓存**: 1分钟TTL（可配置）
- **多通道支持**: 飞书、QQ、其他通道统一管理
- **自动清理**: 过期内容自动删除
- **上下文整合**: 多通道信息可合并处理
- **升级机制**: 重要内容可升级为长期记忆

### 🧠 记忆体系定位

```
感觉记忆（毫秒级）
    ↓
短期记忆（1分钟）← 本skill
    ↓
长期记忆（永久）← MEMORY.md
```

---

## ⚙️ 配置

```json
{
  "ttl_seconds": 60,           // 过期时间
  "max_entries": 50,            // 最大条目数
  "cleanup_interval_seconds": 10,  // 清理间隔
  "auto_cleanup": true,         // 自动清理
  "upgrade_to_long_term": true  // 支持升级为长期记忆
}
```

---

## 📖 使用方法

### 1. 写入短期记忆

```python
from short_term_memory import ShortTermMemory

stm = ShortTermMemory()

# 写入记忆
entry_id = stm.write(
    content="星之君说：记住要完成X任务",
    channel="feishu",
    user_id="ou_472d0b86d66dd43850b6d7c249c76d28",
    context={
        "type": "task",
        "priority": "high"
    }
)
```

### 2. 读取短期记忆

```python
# 读取所有未过期记忆
entries = stm.read()

# 按通道过滤
feishu_entries = stm.read(channel="feishu")

# 按用户过滤
user_entries = stm.read(user_id="ou_472d0b86d66dd43850b6d7c249c76d28")
```

### 3. 查询短期记忆

```python
# 文本查询
results = stm.query("任务", limit=5)
```

### 4. 升级为长期记忆

```python
# 升级重要内容
stm.upgrade_to_long_term(entry_id)
```

---

## 🎬 使用场景

### 场景1: 跨通道任务跟踪

```
13:40 飞书: "帮我记住X任务"
    → stm.write("X任务", "feishu", user_id)

13:45 QQ: "X任务进度怎么样了？"
    → stm.read(user_id)
    → 返回: "您刚才在飞书提到X任务，我正在处理..."
```

### 场景2: 多通道信息整合

```
13:40 飞书: "项目A需要处理"
13:42 QQ: "项目B也要做"
    → stm.read()
    → 整合: [项目A + 项目B]
    → 主动汇报: "发现两个项目任务，是否需要整合处理？"
```

### 场景3: 临时讨论记录

```
快速讨论，不需要永久记住
    → stm.write(content, ttl=60)
    → 1分钟后自动清理
    → 不占用长期记忆空间
```

---

## 📂 文件结构

```
skills/short-term-memory/
├── skill.json                  # Skill配置
├── short_term_memory.py        # 核心实现
└── README.md                   # 本文档

memory/
├── short-term-cache.json       # 短期记忆缓存
└── SHORT_TERM_MEMORY_DESIGN.md # 设计文档
```

---

## 🔧 API参考

### `write(content, channel, user_id, context=None, ttl=None)`
写入短期记忆

**参数**:
- `content`: 记忆内容（字符串）
- `channel`: 通道标识（feishu, qq, etc.）
- `user_id`: 用户ID
- `context`: 上下文信息（可选）
- `ttl`: 过期时间（可选，默认使用配置）

**返回**: 记忆ID

---

### `read(channel=None, user_id=None, limit=10)`
读取短期记忆

**参数**:
- `channel`: 过滤通道（可选）
- `user_id`: 过滤用户ID（可选）
- `limit`: 返回条目数限制（默认10）

**返回**: 记忆条目列表

---

### `query(query_text, limit=5)`
查询短期记忆

**参数**:
- `query_text`: 查询文本
- `limit`: 返回条目数限制（默认5）

**返回**: 匹配的记忆条目列表

---

### `upgrade_to_long_term(entry_id)`
升级为长期记忆

**参数**:
- `entry_id`: 记忆ID

**返回**: 是否成功

---

### `get_stats()`
获取统计信息

**返回**: 统计信息字典

---

## 📊 数据结构

### 短期记忆条目

```json
{
  "id": "1709878920_abc123",
  "timestamp": 1709878920.123,
  "created_at": "2026-03-08T13:42:00",
  "expires_at": 1709878980.123,
  "ttl_seconds": 60,
  "channel": "feishu",
  "user_id": "ou_472d0b86d66dd43850b6d7c249c76d28",
  "content": "星之君说：记住要完成X任务",
  "context": {
    "type": "task",
    "priority": "high",
    "related_to": null
  }
}
```

---

## 🚀 未来改进

- [ ] 语义搜索（基于向量）
- [ ] 自动升级规则（重要内容自动升级）
- [ ] 多用户隔离
- [ ] 与MEMORY.md的无缝集成
- [ ] GUI管理界面

---

## 💡 设计理念

**灵感来源**: 人类记忆系统

**核心价值**: 填补长期记忆和会话上下文之间的空白

**类比**: 
- 短期记忆 = 直觉反应（1分钟）
- 长期记忆 = 深思熟虑的决策（永久）

---

**创建时间**: 2026-03-08  
**作者**: 炎月 - 星之君的专属炎之精灵  
**状态**: ✅ v1.0.0 实现完成