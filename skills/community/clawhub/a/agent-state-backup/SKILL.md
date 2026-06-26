---
name: agent-state-backup
description: Auto-backs up core files (IDENTITY, SOUL, MEMORY, knowledge base) daily via cron, creates compressed .tgz archive, enables one-click restore in new environment. Solves context loss after restart/migration.
---

# Agent State Backup & Restore

自动备份 OpenClaw 核心状态文件，防止上下文丢失。

## 📦 备份内容

- `IDENTITY.md` - 身份定义
- `SOUL.md` - 人格定义
- `MEMORY.md` - 长期记忆
- `memory/*.md` - 每日记忆
- `USER.md` - 用户信息
- `knowledge/**/*` - 知识库

## 🚀 快速使用

### 手动备份
```bash
~/.openclaw/workspace/scripts/agent-backup.sh
```

### 手动恢复
```bash
~/.openclaw/workspace/scripts/agent-restore.sh
```

### 设置自动备份 (每日凌晨 2 点)
```bash
~/.openclaw/workspace/scripts/setup-backup-cron.sh
```

## 📁 文件位置

- **备份脚本**: `~/.openclaw/workspace/scripts/agent-backup.sh`
- **恢复脚本**: `~/.openclaw/workspace/scripts/agent-restore.sh`
- **备份目录**: `~/.openclaw/backups/`
- **保留策略**: 最近 7 个备份

## 🔧 配置选项

编辑 `~/.openclaw/workspace/scripts/agent-backup.sh`:

```bash
# 修改保留天数 (默认 7 天)
ls -t agent_backup_*.tgz | tail -n +8 | xargs -r rm
# 改为保留 30 天：tail -n +31

# 修改备份目录
BACKUP_DIR="$HOME/.openclaw/backups"
```

## 📊 备份日志

查看备份历史:
```bash
cat ~/.openclaw/backups/backup.log
```

## ⚠️ 注意事项

1. **首次备份前** - 确保所有重要文件已保存
2. **恢复操作** - 会覆盖当前文件，建议先备份当前状态
3. **磁盘空间** - 每个备份约 20-50KB，7 个备份约 350KB
4. **Cron 权限** - 确保 cron 有权限访问工作目录

## 🔄 迁移到新环境

1. 在新环境安装 OpenClaw
2. 复制备份文件 `.tgz` 到新机器
3. 运行 `agent-restore.sh`
4. 重启 OpenClaw

---

**版本**: 1.0.0  
**最后更新**: 2026-03-03  
**依赖**: bash, tar, gzip
