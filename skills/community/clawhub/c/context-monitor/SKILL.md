# 📊 Context Monitor Skill

**版本：** 1.0.0  
**创建时间：** 2026-03-09  
**作者：** AI Agent Team

---

## 🎯 技能说明

监控 OpenClaw 上下文窗口占用情况，当占用率超过阈值时自动压缩旧对话，保持系统响应速度。

---

## 📋 功能特性

- ✅ 实时监控上下文窗口占用
- ✅ 超过阈值自动压缩
- ✅ 保留最近 50 轮对话
- ✅ 保留关键记忆
- ✅ 自动告警通知

---

## 🔧 配置参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `warning_threshold` | 70% | 警告阈值 |
| `critical_threshold` | 90% | 危险阈值 |
| `keep_recent_rounds` | 50 | 保留最近对话轮数 |
| `check_interval` | 3600 | 检查间隔（秒） |

---

## 📁 文件结构

```
context-monitor/
├── SKILL.md              # 本文件
├── monitor.ps1           # 主监控脚本
├── compress.ps1          # 压缩脚本 脚本
├── config.json           # 配置文件
└── README.md             # 使用说明
```

---

## 🚀 使用方式

### 手动执行

```powershell
powershell -ExecutionPolicy Bypass -File workspace/skills/context-monitor/monitor.ps1
```

### Cron 自动执行

```bash
# 每小时检查一次
openclaw cron add --name context-monitor --cron "0 * * * *" --agent main --message "执行 context-monitor 技能"
```

---

## 📊 输出日志

**日志位置：** `workspace/skills/context-monitor/log.txt`

**日志格式：**
```
[2026-03-09 22:00:00] ✅ 上下文健康：占用率 45%
[2026-03-09 23:00:00] ⚠️ 上下文警告：占用率 75%
[2026-03-09 23:00:01] 🗜️ 已压缩旧对话，释放 30% 空间
```

---

## ⚠️ 注意事项

1. **不要修改核心配置** - 本技能不修改 openclaw.json
2. **定期清理日志** - 避免日志文件过大
3. **检查压缩效果** - 确保重要对话未被压缩

---

## 📞 故障排查

### 问题 1：脚本无法执行

**解决：**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
```

### 问题 2：压缩失败

**解决：**
- 检查文件权限
- 检查磁盘空间
- 查看日志文件

---

*Last updated: 2026-03-09 22:41（东八区）*
