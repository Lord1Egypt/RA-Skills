# Backup Recovery Toolkit | 备份恢复工具包

<p align="center">
  📦 Enterprise-grade backup and recovery solution for data protection
</p>

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

---

<a name="english"></a>
## English

### Overview

Backup Recovery Toolkit is a comprehensive solution for data backup and disaster recovery. It supports file backup, database backup, incremental backup, and scheduled tasks with version management.

### Installation

```bash
pip install -r requirements.txt
```

### Features

| Feature | Description |
|---------|-------------|
| File Backup | Local and remote file backup with compression |
| Database Backup | MySQL, PostgreSQL, MongoDB backup support |
| Incremental Backup | Only backup changed files to save space |
| Scheduled Tasks | Cron-style backup scheduling |
| Version Management | Keep multiple versions with rollback support |
| Disaster Recovery | Fast restore to any point in time |

### Quick Start

```python
from backup_recovery_toolkit import FileBackup, DatabaseBackup

# File backup
backup = FileBackup(source="/data", destination="/backup")
result = backup.run(name="daily-backup")
print(f"Backup completed: {result['files_backed_up']} files")

# Database backup
db = DatabaseBackup(
    db_type="mysql",
    host="localhost",
    user="root",
    password="secret",
    database="mydb"
)
db.run()
```

### CLI Usage

```bash
# Basic backup
python scripts/backup_toolkit.py backup \
  --source /path/to/data \
  --dest /path/to/backup \
  --name "my-backup"

# Incremental backup
python scripts/backup_toolkit.py incremental \
  --source /data \
  --dest /backup \
  --reference /backup/previous

# Restore from backup
python scripts/backup_toolkit.py restore \
  --backup /backup/my-backup-20240101 \
  --dest /data

# Schedule daily backup
python scripts/backup_toolkit.py schedule \
  --source /data \
  --dest /backup \
  --cron "0 2 * * *" \
  --name "daily-backup"
```

---

<a name="中文"></a>
## 中文

### 概述

备份恢复工具包是一个全面的数据备份与灾难恢复解决方案。支持文件备份、数据库备份、增量备份和定时任务，并提供版本管理功能。

### 安装

```bash
pip install -r requirements.txt
```

### 功能特性

| 特性 | 说明 |
|------|------|
| 文件备份 | 本地和远程文件备份，支持压缩 |
| 数据库备份 | 支持MySQL、PostgreSQL、MongoDB备份 |
| 增量备份 | 只备份变更的文件，节省空间 |
| 定时任务 | Cron风格的备份计划 |
| 版本管理 | 保留多个版本，支持回滚 |
| 灾难恢复 | 快速恢复到任意时间点 |

### 快速开始

```python
from backup_recovery_toolkit import FileBackup, DatabaseBackup

# 文件备份
backup = FileBackup(source="/data", destination="/backup")
result = backup.run(name="daily-backup")
print(f"备份完成: {result['files_backed_up']} 个文件")

# 数据库备份
db = DatabaseBackup(
    db_type="mysql",
    host="localhost",
    user="root",
    password="secret",
    database="mydb"
)
db.run()
```

### 命令行使用

```bash
# 基础备份
python scripts/backup_toolkit.py backup \
  --source /path/to/data \
  --dest /path/to/backup \
  --name "my-backup"

# 增量备份
python scripts/backup_toolkit.py incremental \
  --source /data \
  --dest /backup \
  --reference /backup/previous

# 从备份恢复
python scripts/backup_toolkit.py restore \
  --backup /backup/my-backup-20240101 \
  --dest /data

# 定时备份
python scripts/backup_toolkit.py schedule \
  --source /data \
  --dest /backup \
  --cron "0 2 * * *" \
  --name "daily-backup"
```

## 测试 | Testing

```bash
python -m pytest tests/test_backup_recovery.py -v
```

## 许可证 | License

MIT License
