---
name: backup-recovery-toolkit
version: 1.0.0
description: |
  企业级备份恢复工具包，支持文件备份、数据库备份、增量备份、定时任务和灾难恢复。
  Enterprise-grade backup and recovery toolkit supporting file backup, database backup, incremental backup, scheduled tasks and disaster recovery.
---

# Backup Recovery Toolkit | 备份恢复工具包

一套完整的数据备份与灾难恢复解决方案，保护您的重要数据安全。

A comprehensive data backup and disaster recovery solution to protect your critical data.

## 核心功能 | Core Features

- 📦 **文件备份** | File Backup - 本地和远程文件备份
- 🗄️ **数据库备份** | Database Backup - MySQL/PostgreSQL/MongoDB备份
- 📈 **增量备份** | Incremental Backup - 只备份变更部分，节省空间
- ⏰ **定时任务** | Scheduled Tasks - Cron式备份计划
- 🔄 **版本管理** | Version Management - 保留多版本，支持回滚
- 🚨 **灾难恢复** | Disaster Recovery - 快速恢复数据到任意时间点

## 快速开始 | Quick Start

### 命令行使用 | CLI Usage

```bash
# 备份目录 | Backup directory
python scripts/backup_toolkit.py backup --source /data --dest /backup --name "daily-backup"

# 增量备份 | Incremental backup
python scripts/backup_toolkit.py incremental --source /data --dest /backup --last-backup /backup/previous

# 恢复数据 | Restore data
python scripts/backup_toolkit.py restore --backup /backup/daily-backup --dest /data
```

### Python API

```python
from backup_recovery_toolkit import FileBackup, DatabaseBackup

# 文件备份 | File backup
backup = FileBackup(source="/data", destination="/backup")
backup.run(name="daily-backup")

# 数据库备份 | Database backup
db_backup = DatabaseBackup(
    db_type="mysql",
    host="localhost",
    user="root",
    password="secret",
    database="mydb"
)
db_backup.run()
```

## 测试 | Tests

```bash
python -m pytest tests/ -v
```
