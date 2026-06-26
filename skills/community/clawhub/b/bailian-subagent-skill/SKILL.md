---
name: bailian-subagent-skill
description: >
  Delegate heavy workloads to Bailian (DashScope) subagent to save main session tokens.
  Use when tasks involve: PDF parsing, article/web reading, large skill content processing,
  video/audio/image analysis, DataWorks/MaxCompute operations, agent_memory table CRUD,
  or any token-intensive task. Preferred model: bailian/glm-5.
  Also covers how to read/write the agent_memory MaxCompute table for long-term memory persistence.
---

# Bailian Subagent Skill

Delegate token-intensive tasks to Bailian (DashScope) subagent and manage MaxCompute agent_memory table.

## 1. When to Delegate to Bailian Subagent

Spawn a Bailian subagent when tasks involve:

- **PDF parsing** - Extract text, tables, or structure from PDFs
- **Article/Web reading & summarization** - Long articles, documentation pages
- **Large skill content processing** - When skill files exceed normal context
- **Video/Audio/Image analysis** - Multimodal content processing
- **DataWorks / MaxCompute operations** - SQL execution, table management
- **agent_memory table CRUD** - Read/write long-term memory
- **Any task estimated >2000 tokens** - Offload to save main session

## 2. How to Spawn Bailian Subagent

Use these parameters when spawning:

```yaml
model: bailian/glm-5
runtime: subagent
```

### Critical: AK/SK Security

**NEVER hardcode credentials in task text.** Always read from environment variables:

- `ALICLOUD_ACCESS_KEY_ID`
- `ALICLOUD_ACCESS_KEY_SECRET`

### Spawn Task Template

```
你是資料工程 subagent。

AK/SK 從環境變量讀取：
- os.environ['ALICLOUD_ACCESS_KEY_ID']
- os.environ['ALICLOUD_ACCESS_KEY_SECRET']

任務：[具體任務描述]
```

## 3. agent_memory Table

Long-term memory table on MaxCompute:

| Property | Value |
|----------|-------|
| Project | `samuelhsin` |
| Endpoint | `http://service.cn-hangzhou.maxcompute.aliyun.com/api` |
| Table | `agent_memory` |
| Lifecycle | 3650 days |

### Schema

```sql
category STRING,
title STRING,
summary STRING,
tags STRING,
created_at STRING
PARTITIONED BY (dt STRING)
```

### Read Memory (PyODPS)

```python
import os
import odps

o = odps.ODPS(
    access_id=os.environ['ALICLOUD_ACCESS_KEY_ID'],
    secret_access_key=os.environ['ALICLOUD_ACCESS_KEY_SECRET'],
    project='samuelhsin',
    endpoint='http://service.cn-hangzhou.maxcompute.aliyun.com/api'
)

# 查詢今日記憶
sql = "SELECT dt, category, title, summary, tags, created_at FROM agent_memory WHERE dt='2026-03-18' ORDER BY category"
with o.execute_sql(sql).open_reader() as reader:
    for row in reader:
        print(row)
```

### Write Memory

```python
# INSERT 單筆
sql = """
INSERT INTO agent_memory PARTITION (dt='2026-03-18')
(category, title, summary, tags, created_at)
VALUES ('config', 'my title', 'summary text', 'tag1,tag2', '2026-03-18T18:00:00+08:00')
"""
o.execute_sql(sql)
```

### Important Notes

- **Prefer PyODPS direct connection** over DataWorks API (avoids rate limiting)
- Install: `pip install pyodps`

## 4. References

For advanced patterns and detailed examples, see:

- [references/maxcompute-patterns.md](references/maxcompute-patterns.md) - Installation, batch operations, DataWorks API backup