---
name: core-capabilities
description: 工作助手核心能力集成包 - 包含 Obsidian/Git 同步、记忆数据库、自然语言查询工具、监控页面等完整能力。提供 memory_query_agent.py 工具和完整文档。
version: 2.0.0
author: AI Assistant
tags: [obsidian, git, memory, database, monitoring, capabilities, query-tool]
---

# Core Capabilities v2 - 工作助手核心能力完整包

本技能包整合了工作助手的所有核心能力，提供完整的工具集、查询能力和使用指导。

## 📦 包含工具

- **memory_query_agent.py** - 自然语言记忆查询工具
- **monitor_server.py** - Web 监控服务器  
- **setup_cron.sh** - Cron 配置脚本

## 🎯 核心能力

1. **🧠 Obsidian 和 Git 同步** - 完整的文件管理和版本控制
2. **📊 记忆数据库** - SQLite 存储 + 自动同步（24 条记录）
3. **🔍 自然语言查询** - 中文智能查询
4. **📈 监控页面** - Web 实时监控

## 🚀 使用

```bash
# 查询记忆
python3 memory_query_agent.py "最近的记录"

# 交互模式
python3 memory_query_agent.py -i

# 查看状态
python3 memory_query_agent.py --sync-status
```

## 📊 状态

- 数据库：24 条记录
- 同步：每 30 分钟
- 监控：8003 端口

## 💡 示例

```
用户：我们有哪些能力？
助手：我们有四大核心能力...
```

---

**版本**: 2.0.0  
**创建**: 2026-04-12
