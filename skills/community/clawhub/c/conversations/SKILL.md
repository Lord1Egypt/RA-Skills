---
name: conversations-universal
description: 从 OpenClaw sessions/*.jsonl 导入对话历史到本地 SQLite，配合 FTS5 全文搜索。成为真正的记忆库，支持语义化查询历史对话，让整理和回顾更高效。装好后跑一次 import，之后随时可以 query。
---

# conversations-universal

对话历史的本地记忆库。

## 使用方式

### 第一次使用

1. 运行导入脚本，把历史 session 读入本地库：
```
python {baseDir}/scripts/import_sessions.py
```

2. 之后每次想回顾历史，直接用 query 脚本：
```
python {baseDir}/scripts/query_conversations.py <搜索内容>
```

### 查询示例

```bash
# 查询某天的讨论
python scripts/query_conversations.py "我们讨论过内存泄漏"

# 查询某个话题
python scripts/query_conversations.py "OpenClaw 配置"
```

### 自动导入

建议配合 cron 定期导入新 session：
```
openclaw cron add \
  --name "对话历史导入" \
  --cron "0 */6 * * *" \
  --session isolated \
  --message "python {baseDir}/scripts/import_sessions.py" \
  --announce
```

## 工作原理

- **存储**：SQLite + FTS5 全文搜索，零外部依赖
- **导入**：读取 `agents/main/sessions/*.jsonl`，解析 role/content，写入 chunks 表
- **搜索**：FTS5 MATCH，支持自然语言查询

## 环境变量

| 变量 | 默认值 | 说明 |
|------|--------|------|
| OPENCLAW_WORKSPACE | 自动推断 | session 文件所在目录 |
| CONVERSATIONS_DB | `{workspace}/conversations.db` | 数据库路径 |
| DRY_RUN | false | 试运行，不写入 |

## 依赖

- Python 3.8+（内置 sqlite3，FTS5 需要 3.9+）
- OpenClaw sessions 目录

## 与 conversations 1.0 的区别

| | conversations 1.0 | conversations-universal |
|--|--|--|
| 搜索方式 | Ollama 向量搜索 | SQLite FTS5 |
| 外部依赖 | 需要 Ollama | 纯 Python |
| 搜索质量 | 高（语义） | 中（关键词） |
| 适用场景 | 已有 Ollama 的用户 | 所有人 |
