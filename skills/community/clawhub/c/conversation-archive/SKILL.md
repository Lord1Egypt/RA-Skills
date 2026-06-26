---
name: conversation-archive
version: 1.0.0
description: "对话记忆仓库：自动归档 session 对话，保留原始记录，支持检索和误解纠正。可与 memory-never-forget 联动形成完整记忆体系。"
author: Simon
tags: ["memory", "conversation", "archive", "openclaw", "session", "recall"]
metadata: { "openclaw": { "emoji": "💬" } }
license: MIT
---

> ⚠️ 作者信息待填写：ClawHub 上传前需要确认你的 ClawHub/GitHub 用户名

# 💬 Conversation Archive（对话记忆仓库）

## 核心理念

**「记忆会骗人，但对话记录不会。」**

当缪斯说「我不记得了」「我可能理解错了」——去对话仓库里找原始记录，比问老豆更快、更准。

---

## 工作流程

```
Session 结束
    ↓
1. ARCHIVE（归档）
   - 保存原始对话 JSON
   - 生成结构化摘要
   - 提取关键信息（主题/决策/教训）
   ↓
2. INDEX（索引）
   - 按日期/主题/关键词写入 index.json
   - （未来：生成 embedding 向量）
   ↓
3. RETRIEVE（检索）
   - 当需要回溯时 → 搜对话仓库
   - 当发现误解时 → 拉原始记录纠正
   ↓
4. INTEGRATE（整合）
   - 与 memory-never-forget 联动
   - 从归档中提取值得记忆的内容 → 4层分类
```

---

## 目录结构

```
conversation_archive/
├── sessions/           # 原始对话存档
│   └── YYYY-MM/
│       └── {session_id}.json
├── index.json          # 内存索引
└── embeddings/         # 预留：向量索引（未来）
```

---

## Session JSON 格式

```json
{
  "sessionId": "ccba19e7-...",
  "date": "2026-04-07",
  "channel": "webchat",
  "participants": ["Simon", "Muse"],
  "topics": ["OpenClaw升级", "Dreaming", "记忆系统"],
  "decisions": [
    {"text": "开启Dreaming每天0点运行", "context": "老豆同意"}
  ],
  "feedback": [
    {"user": "不要用Markdown表格", "from": "Simon"}
  ],
  "summary": "讨论了OpenClaw升级和记忆系统...",
  "messages": [
    {"role": "user", "content": "...", "time": "..."},
    {"role": "assistant", "content": "...", "time": "..."}
  ],
  "archivedAt": "2026-04-07T17:30:00+08:00"
}
```

---

## 工具（Tools）

### 1. `archive_session` — 归档当前 session

**触发时机：** session 结束前 / 手动触发 / cron 触发

```json
{
  "name": "archive_session",
  "arguments": {
    "sessionKey": "agent:main:main",
    "includeMessages": true
  }
}
```

**自动触发逻辑：**
- 当 session 被 compact 或 restart 时自动归档
- 每次 webchat 超过 30 分钟无活动时归档

### 2. `search_archive` — 搜索对话

**触发时机：** 老豆问「我之前说过什么」「那次对话」「记得3月29日吗」

```json
{
  "name": "search_archive",
  "arguments": {
    "query": "OpenClaw升级",
    "date": "2026-03-29",
    "limit": 5
  }
}
```

### 3. `get_session` — 获取原始对话

**触发时机：** 发现缪斯理解错了，用原始记录纠正

```json
{
  "name": "get_session",
  "arguments": {
    "sessionId": "ccba19e7-..."
  }
}
```

### 4. `extract_memories` — 从归档中提取记忆

**触发时机：** 与 memory-never-forget 联动时

```json
{
  "name": "extract_memories",
  "arguments": {
    "sessionId": "ccba19e7-...",
    "types": ["user", "feedback", "project"]
  }
}
```

---

## 检索策略

### 当前（关键词模式）

```python
# 搜索逻辑
1. 在 index.json 中模糊匹配 query
2. 匹配 topic、keywords、summary 字段
3. 按日期倒序返回 top N
4. 展示匹配的摘要片段
```

### 未来（向量模式）

当 embedding 配置好后：

```python
# 向量搜索
1. query → embedding 向量
2. 在 embeddings/ 目录做余弦相似度搜索
3. 返回 top N 最语义相关的对话
```

**接入条件：** `agents.defaults.memorySearch` 配置了 embedding provider

---

## 与 memory-never-forget 的联动

```
conversation_archive  ──→  memory-never-forget
     │                              │
     │ 提取值得记忆的内容              │ 使用4层分类
     ↓                              ↓
decisions/feedback/          memory/{user,feedback,
project/                     project,reference}/
     │                              │
     └───────────升华──────────────→ knowledge/
```

**联动触发：** 每次归档后，自动调用 `extract_memories` 把值得记忆的内容传给 memory-never-forget 处理。

---

## 自动归档规则

**立即归档：**
- session restart / compact 时
- 超过 30 分钟无活动时
- 每天 23:59 强制归档所有活跃 session

**保留对话：**
- 最近 7 天：完整原始记录
- 7-30 天：仅摘要（messages 字段清除）
- 30 天以上：压缩归档，保留摘要和元数据

**安全清理：**
- 不存 API key、token、密码等敏感信息
- messages 字段在归档时做敏感信息扫描和脱敏

---

## 误解纠正流程

当缪斯意识到自己可能理解错了：

1. 用 `search_archive` 搜相关对话
2. 用 `get_session` 拉原始记录
3. 核对原始对话，确认误解点
4. 更新对应分类记忆（feedback/）
5. 在这次 session 末尾做修正性回复

---

## 触发关键词

| 老豆说 | 缪斯做 |
|--------|--------|
| 「我之前说过...」 | `search_archive(query="...")` |
| 「那天...」 | `search_archive(date="YYYY-MM-DD")` |
| 「你不记得了？」 | `search_archive` + 展示原始记录 |
| 「理解错了」 | `get_session` + 纠正 + 更新记忆 |

---

*版本：v1.0 | 日期：2026-04-07 | 对话记忆仓库 + 未来向量检索预留*
