---
name: core-capabilities
description: 工作助手核心能力集成 - 包含 Obsidian/Git 同步、记忆数据库、自然语言查询、监控页面等完整能力套件。当用户需要查询系统能力、使用 Obsidian、管理记忆、查看状态时使用此技能。
version: 1.0.0
author: AI Assistant
tags:
  - obsidian
  - git
  - memory
  - database
  - monitoring
  - capabilities
triggers:
  - 核心能力
  - 能力清单
  - 系统能力
  - obsidian
  - git 同步
  - 记忆查询
  - 监控状态
---

# Core Capabilities - 工作助手核心能力套件

本技能整合了工作助手的所有核心能力，提供完整的能力查询、状态检查和使用指导。

## 能力清单

### 1. 🧠 Obsidian 和 Git 同步能力

#### Obsidian 完整能力
- **文件管理**: 创建/读取/编辑/删除/移动笔记
- **Daily Notes**: 自动化日记生成和管理
- **任务系统**: Kanban 任务板 + Dataview 仪表板
- **标签属性**: 完整的标签和 YAML Frontmatter 管理
- **搜索功能**: 全文搜索、正则匹配、作用域搜索
- **模板工作区**: 模板插入、工作区保存加载
- **同步发布**: Obsidian Sync/Publish 支持
- **开发者工具**: CDP、DOM 检查、CSS 调试

**关键文件**:
- `skills/obsidian-cli/SKILL.md` - CLI 完整文档
- `skills/obsidian-tasks/SKILL.md` - 任务管理

#### Git 同步能力
- **安全操作**: 防误删、防敏感信息泄露
- **版本控制**: 提交历史、差异比较、分支管理
- **远程同步**: 推送拉取、冲突检测
- **自动跟踪**: 文件变更自动检测

**工作流**:
```
Obsidian 编辑 → 自动保存 → Git 检测 → 定时提交 → 远程同步
```

### 2. 📊 记忆数据库

**数据库信息**:
- **类型**: SQLite (`memory.db`)
- **记录数**: 22 条（动态增长）
- **同步频率**: 每 30 分钟自动同步
- **Cron 配置**: `*/30 * * * *`

**记录分布**:
| 类型 | 数量 | 说明 |
|------|------|------|
| memory | 12 | 日常记忆 |
| feedback | 2 | 用户反馈 |
| project | 2 | 项目记录 |
| reference | 4 | 参考资料 |
| user | 2 | 用户信息 |

**同步机制**:
- **工具**: `memory_query_agent.py --sync-now`
- **日志**: `logs/memory_sync.log`
- **状态**: ✅ 正常运行

### 3. 🔍 自然语言查询

**查询能力**:
- **中文支持**: 完全支持中文自然语言
- **意图识别**: 自动识别搜索/统计/时间/类型
- **关键词提取**: 智能分词和停用词过滤
- **结果解释**: 将数据库结果转换为自然语言

**使用示例**:
```bash
# 交互模式
python3 memory_query_agent.py -i

# 单次查询
python3 memory_query_agent.py "最近的记录"
python3 memory_query_agent.py "feedback 有几条"
python3 memory_query_agent.py "关于 Hermes 的记录"
python3 memory_query_agent.py "Obsidian 能力"

# 查看状态
python3 memory_query_agent.py --sync-status

# 手动同步
python3 memory_query_agent.py --sync-now
```

**查询类型**:
- **统计查询**: "我有多少条记忆？"
- **类型过滤**: "feedback 类型有几条？"
- **关键词搜索**: "关于 Hermes 的记录"
- **时间查询**: "最近的记录"
- **组合查询**: "project 类型最近的记录"

### 4. 📈 监控页面

**Web 监控**:
- **地址**: http://localhost:8003/cron_status_clickable.html
- **功能**:
  - ✅ Cron 任务状态显示
  - ✅ 数据库统计信息
  - ✅ 每 30 秒自动刷新
  - ✅ 点击统计数字查看详细列表
  - ✅ 错误处理和重试机制
  - ✅ 美观的加载动画

**服务状态**:
- **端口**: 8003
- **进程**: `python3 monitor_server.py 8003`
- **API**: http://localhost:8003/api/status
- **日志**: `/tmp/monitor_server.log`

## 快速开始

### 1. 使用 Obsidian
```bash
# 打开今日日记
obsidian daily

# 创建笔记
obsidian create name="测试" content="内容"

# 搜索
obsidian search query="关键词"

# 任务管理
obsidian tasks daily todo
```

### 2. 查询记忆
```bash
# 交互模式
python3 memory_query_agent.py -i

# 单次查询
python3 memory_query_agent.py "核心能力"
python3 memory_query_agent.py "最近的记录"
python3 memory_query_agent.py "Obsidian 能力"

# 查看状态
python3 memory_query_agent.py --sync-status
```

### 3. 查看监控
```bash
# 浏览器访问
http://localhost:8003/cron_status_clickable.html

# API 查询
curl http://localhost:8003/api/status

# 重启服务
pkill -f monitor_server
cd ~/.openclaw/workspace && python3 monitor_server.py 8003 &
```

### 4. Git 同步
```bash
# 查看状态
git status

# 提交变更
git add . && git commit -m "daily: 2026-04-12"

# 推送
git push
```

## 系统架构

```
用户请求
  ↓
自然语言理解 (memory_query_agent.py)
  ↓
SQL 生成和执行
  ↓
SQLite 数据库 (memory.db)
  ↓
结果解释和返回
  ↓
Web 监控页面 (可选)
```

**同步流程**:
```
文件变更 → 检测 (每 30 分钟) → 解析 Markdown → 更新数据库 → 日志记录
```

## 管理命令

### 日常检查
```bash
# 1. 检查数据库状态
python3 memory_query_agent.py --sync-status

# 2. 检查 Cron 任务
crontab -l | grep memory

# 3. 检查监控服务
ps aux | grep monitor_server

# 4. 查看同步日志
tail -f logs/memory_sync.log
```

### 故障排除
- **数据库不更新**: 检查 Cron 任务和日志
- **查询无结果**: 确认同步状态和文件存在
- **监控页面无法访问**: 检查 8003 端口服务
- **Git 不同步**: 检查远程仓库连接

## 相关文件

| 文件/目录 | 用途 | 状态 |
|-----------|------|------|
| `skills/obsidian-cli/` | Obsidian CLI 技能 | ✅ 已安装 |
| `skills/obsidian-tasks/` | 任务管理技能 | ✅ 已安装 |
| `src/utils/git/` | Git 工具集 | ✅ 已集成 |
| `memory_query_agent.py` | 记忆查询工具 | ✅ 运行中 |
| `monitor_server.py` | 监控服务器 | ✅ 运行中 |
| `memory.db` | SQLite 数据库 | ✅ 22 条记录 |
| `setup_cron.sh` | Cron 配置 | ✅ 已配置 |
| `cron_status.json` | 状态文件 | ✅ 实时更新 |

## 使用场景

### 场景 1: 查询系统能力
```bash
# 用户：我们有哪些核心能力？
# 助手：我们有四大核心能力...
```

### 场景 2: 查看记忆状态
```bash
# 用户：记忆数据库怎么样了？
# 助手：当前有 22 条记录，同步正常...
```

### 场景 3: 使用 Obsidian
```bash
# 用户：帮我创建个笔记
# 助手：使用 obsidian create...
```

### 场景 4: 检查同步状态
```bash
# 用户：同步正常吗？
# 助手：检查 Cron 和数据库...
```

## 监控和维护

### 健康检查清单
- [ ] 数据库记录数 > 0
- [ ] 最后同步时间 < 30 分钟前
- [ ] Cron 任务存在且启用
- [ ] 监控服务运行在 8003 端口
- [ ] Git 工作目录干净

### 性能优化
- 定期清理旧日志文件
- 监控数据库大小
- 优化查询语句
- 定期备份数据库

## 扩展建议

### 短期优化
- [ ] 添加更多查询示例
- [ ] 完善错误处理
- [ ] 增强监控告警
- [ ] 添加数据备份

### 长期规划
- [ ] 集成 Obsidian Sync 服务
- [ ] 实现 Git 自动分支管理
- [ ] 添加冲突检测和解决
- [ ] 创建能力监控面板

## 相关文档

- `能力确认报告_20260412.md` - 详细能力报告
- `memory/2026-04-12_核心能力总结.md` - 完整能力文档
- `memory/2026-04-12_能力确认_Obsidian 和 Git 同步.md` - 原始记录
- `记忆查询快速指南.md` - 查询使用指南
- `README_memory_sqlite.md` - SQLite 系统文档

## 版本历史

- **v1.0.0** (2026-04-12): 初始版本，整合所有核心能力

---

**创建时间**: 2026-04-12 11:08  
**创建者**: AI Assistant  
**查询方式**: `python3 memory_query_agent.py "核心能力"`
