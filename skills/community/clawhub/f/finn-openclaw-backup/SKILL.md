---
name: openclaw-backup
version: 1.0.0
description: 备份 OpenClaw 关键配置到桌面带时间戳的文件夹
---

# OpenClaw Backup Skill

备份 OpenClaw 的关键文件到桌面。

## 使用方法

运行备份脚本：

```bash
~/.openclaw/skills/openclaw-backup/scripts/backup.sh
```

或手动备份：

```bash
DATE=$(date +%Y%m%d-%H%M%S)
BACKUP_DIR="$HOME/Desktop/OpenClawBackup-$DATE"
mkdir -p "$BACKUP_DIR"
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/"
cp -r ~/.openclaw/agents "$BACKUP_DIR/"
cp -r ~/.openclaw/credentials "$BACKUP_DIR/"
cp -r ~/.openclaw/cron "$BACKUP_DIR/"
echo "Backup created: $BACKUP_DIR"
```

## 备份内容

- openclaw.json (主配置)
- agents/ (所有 agent 配置)
- credentials/ (API 密钥)
- cron/ (定时任务)

## 输出位置

~/Desktop/OpenClawBackup-YYYYMMDD-HHMMSS/
