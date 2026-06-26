# Core Capabilities Skill - 工作助手核心能力套件

## 📦 发布信息

- **名称**: core-capabilities
- **版本**: 1.0.0
- **作者**: AI Assistant
- **创建日期**: 2026-04-12
- **状态**: ✅ 已发布

## 🎯 功能特性

本技能整合了工作助手的四大核心能力：

1. **🧠 Obsidian 和 Git 同步能力**
   - 完整的 Obsidian 自动化
   - Git 版本控制和同步

2. **📊 记忆数据库**
   - SQLite 存储（22 条记录）
   - 每 30 分钟自动同步

3. **🔍 自然语言查询**
   - 中文自然语言支持
   - 智能意图识别

4. **📈 监控页面**
   - Web 监控界面
   - 实时状态显示

## 📋 安装方法

技能已安装在工作区：
```bash
~/.openclaw/workspace/skills/core-capabilities/SKILL.md
```

## 🚀 使用方式

### 1. 查询能力
```bash
python3 memory_query_agent.py "核心能力"
```

### 2. 交互模式
```bash
python3 memory_query_agent.py -i
```

### 3. 查看状态
```bash
python3 memory_query_agent.py --sync-status
```

## 📊 当前状态

- **数据库记录**: 22 条
- **同步状态**: ✅ 正常（每 30 分钟）
- **监控页面**: http://localhost:8003/cron_status_clickable.html
- **Cron 任务**: ✅ 已配置

## 📁 文件结构

```
skills/core-capabilities/
├── SKILL.md       # 技能主文件
├── README.md      # 本文件
└── metadata.json  # 元数据
```

## 🔧 管理命令

### 检查状态
```bash
# 数据库状态
python3 memory_query_agent.py --sync-status

# Cron 任务
crontab -l | grep memory

# 监控服务
ps aux | grep monitor_server

# 同步日志
tail -f logs/memory_sync.log
```

### 故障排除
- 数据库不更新 → 检查 Cron 和日志
- 查询无结果 → 确认同步状态
- 监控不可用 → 检查 8003 端口
- Git 不同步 → 检查远程连接

## 📈 监控指标

| 指标 | 当前值 | 状态 |
|------|--------|------|
| 数据库记录 | 22 条 | ✅ |
| 同步间隔 | 30 分钟 | ✅ |
| 监控端口 | 8003 | ✅ |
| Cron 任务 | 已配置 | ✅ |

## 📝 更新日志

### v1.0.0 (2026-04-12)
- ✅ 初始版本发布
- ✅ 整合 Obsidian/Git 能力
- ✅ 整合记忆数据库
- ✅ 整合自然语言查询
- ✅ 整合监控页面

## 🔗 相关链接

- [能力确认报告](../../../能力确认报告_20260412.md)
- [记忆查询指南](../../../记忆查询快速指南.md)
- [SQLite 文档](../../../README_memory_sqlite.md)

## 💡 使用示例

### 示例 1: 查询能力
```
用户：我们有哪些核心能力？
助手：我们有四大核心能力...
```

### 示例 2: 查看状态
```
用户：记忆数据库怎么样了？
助手：当前有 22 条记录，同步正常...
```

### 示例 3: 使用 Obsidian
```
用户：帮我创建个笔记
助手：使用 obsidian create...
```

## 🎯 下一步

### 短期
- [ ] 添加更多使用示例
- [ ] 完善错误处理
- [ ] 增强监控告警

### 长期
- [ ] 集成 Obsidian Sync
- [ ] Git 自动分支管理
- [ ] 冲突检测解决
- [ ] 能力监控面板

---

**创建时间**: 2026-04-12  
**维护者**: AI Assistant  
**查询**: `python3 memory_query_agent.py "core-capabilities"`
