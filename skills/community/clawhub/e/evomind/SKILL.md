---
name: evomind
description: "Agent进化操作系统 — 五层记忆×自我进化引擎。可直接安装运行，非纯文档。"
version: 1.1.2
tags: [Agent, 进化, 记忆, 自我优化, 中文, 可执行]
category: 开发工具
---

# EvoMind — Agent记忆与进化引擎

**不是文档，是代码。** `pip install` 后直接 `from evomind import MemoryCore`。

## 快速开始

```bash
pip install -r requirements.txt  # 零外部依赖，仅标准库

# CLI 演示
python scripts/memory_core.py health
python scripts/memory_core.py remember "用户偏好深色模式"
python scripts/memory_core.py recall "深色"

# Python API
python -c "
from scripts.memory_core import MemoryCore
mem = MemoryCore()
mem.remember('Python version: 3.11', priority=5, tags=['env'])
mem.skill_save('web-scraper', open('SKILL.md').read(), description='网页抓取')
mem.curate()
print(mem.stats())
"
```

## 五层架构

| 层 | 功能 | 方法 |
|---|------|------|
| **L1** 持久记忆 | 关键事实自动存档，≤20KB | `remember()`, `forget()`, `recall_l1()` |
| **L2** 技能层 | 成功方案永久固化 | `skill_save()`, `skill_load()`, `skill_find()` |
| **L3** 缓存层 | 会话临时数据，TTL过期 | `cache_set()`, `cache_get()`, `cache_clear()` |
| **L4** 策展层 | 每日自动审查优化 | `curate()`, `curator_log()` |
| **L5** 索引层 | FTS5全文搜索，跨层召回 | `recall()`, `stats()` |

## 核心特性

- ✅ **跨会话持久记忆** — SQLite存储，关了再开还在
- ✅ **自动归档** — L1超20KB自动归档最早条目到`l1_archive`
- ✅ **冗余检测** — L4 curator自动发现重复技能（Jaccard≥0.6）
- ✅ **自我进化** — `skill_save()` + `skill_load()` 形成改进循环
- ✅ **零依赖** — 仅Python标准库+内置sqlite3
- ✅ **FTS5全文搜索** — 跨L1/L2/L5统一语义检索

## 生产验证

来自 **Hermes Agent** 生产环境实战验证（2026年6月起），非理论设计。已在真实Agent系统中运行五层全架构。

## 许可证

MIT — 免费使用、修改、分发。
