# ClawSync 🔄 | 配置同步备份

> Backup and sync your entire OpenClaw configuration
> 备份并同步你的整个 OpenClaw 配置

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-blue)](https://openclaw.ai)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**English**: Never lose your OpenClaw setup again. One command to backup everything, one command to restore anywhere.

**中文**: 再也不怕丢失 OpenClaw 配置。一条命令备份所有内容，一条命令在任何地方恢复。

---

## ✨ Features | 功能特性

- **💾 Complete Backup | 完整备份** - Skills, memory, settings, credentials | 技能、记忆、设置、凭证
- **🔐 Encryption | 加密** - Password-protect sensitive data | 密码保护敏感数据
- **☁️ Multi-Storage | 多存储** - Local, cloud, Git repositories | 本地、云端、Git 仓库
- **🔄 Smart Restore | 智能恢复** - Selective restore, version control | 选择性恢复、版本控制

---

## 🚀 Quick Start | 快速开始

```bash
# Full backup with encryption | 加密完整备份
python3 scripts/clawsync.py backup --encrypt

# Quick backup (skills + settings only) | 快速备份（仅技能+设置）
python3 scripts/clawsync.py backup --quick

# List backups | 列出备份
python3 scripts/clawsync.py list

# Restore | 恢复
python3 scripts/clawsync.py restore --backup ~/backups/openclaw_backup.zip
```

---

## 📦 Installation | 安装

### For OpenClaw Users | OpenClaw 用户

```bash
clawhub install Zaosusu/clawsync-skill
```

### Standalone Usage | 独立使用

```bash
git clone https://github.com/Zaosusu/clawsync-skill.git
cd clawsync-skill
python3 scripts/clawsync.py --version
```

---

## 🎯 Use Cases | 使用场景

### 1. Computer Migration | 电脑迁移
```bash
# On old computer | 在旧电脑上
python3 scripts/clawsync.py backup --encrypt --output migration.zip

# Transfer file, then on new computer | 传输文件，然后在新电脑上
python3 scripts/clawsync.py restore --backup migration.zip --fresh-install
```

### 2. Daily Auto-Backup | 每日自动备份
```bash
# Add to cron/job scheduler | 添加到定时任务
python3 scripts/clawsync.py backup --quick
```

### 3. Team Configuration Sharing | 团队配置共享
```bash
# Export only skills (no credentials) | 仅导出技能（不含凭证）
python3 scripts/clawsync.py export skills --output team_skills.zip
```

---

## 🛠️ Commands | 命令

### `backup` - Create Backup | 创建备份
```bash
python3 scripts/clawsync.py backup [options]

Options | 选项:
  --output PATH      # Output file path | 输出文件路径
  --encrypt          # Encrypt backup | 加密备份
  --quick            # Quick backup | 快速备份
  --include-history  # Include conversation history | 包含对话历史
  --include-workspace # Include workspace files | 包含工作区文件
```

### `restore` - Restore Backup | 恢复备份
```bash
python3 scripts/clawsync.py restore [options]

Options | 选项:
  --backup PATH      # Backup file to restore | 要恢复的备份文件
  --selective        # Choose what to restore | 选择性恢复
  --overwrite        # Overwrite existing files | 覆盖现有文件
  --fresh-install    # Setup on new machine | 在新机器上设置
```

### `list` - List Backups | 列出备份
```bash
python3 scripts/clawsync.py list [options]
```

---

## 🔒 Safety Features | 安全特性

- ✅ **Dry-run mode | 试运行模式** - Preview changes | 预览变更
- ✅ **Incremental backups | 增量备份** - Only changed files | 仅备份变更文件
- ✅ **Integrity verification | 完整性验证** - Verify backup integrity | 验证备份完整性
- ✅ **Atomic operations | 原子操作** - All-or-nothing restore | 全有或全无恢复

---

## 📄 License | 许可证

MIT License - See [LICENSE](LICENSE) file

---

**Never lose your configuration again | 再也不丢失配置** 💾
