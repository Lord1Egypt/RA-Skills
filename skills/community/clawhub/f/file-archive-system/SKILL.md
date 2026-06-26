---
name: file-archive-system
description: 本地文件归档系统。把习惯、偏好、日程、每日记录和长期知识结构化存放到四层记忆目录，并通过 index.json 建立可检索索引。
---

# File Archive System

将专属 AI 的记忆存储为本地结构化文件，便于检索、备份和多设备同步。

## 目录结构

```text
personal-ai-memory/
├── identity/
├── working-memory/
├── short-term-logs/
├── long-term-memory/
├── archive/
└── index.json
```

## 推荐命令

```bash
python3 scripts/personal_ai_memory.py init
python3 scripts/personal_ai_memory.py reindex
python3 scripts/personal_ai_memory.py archive --keep-days 14
```

## 同步建议

- 用 Git、iCloud Drive、Syncthing 或其他你已有的本地优先同步工具同步 `personal-ai-memory/`
- 把同步范围限制在记忆目录，不要把整套工作区随意暴露到公共盘
