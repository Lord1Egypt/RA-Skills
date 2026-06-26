---
name: backup-manager-pro
description: Manage automated backups for OpenClaw configurations, clean expired backups, and create pre-modification snapshots. 自动化备份管理系统：配置备份、过期清理、修改前快照。
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["bash","find","cp","rm","date","mkdir"]}}}
---

# Backup Manager Pro 🔄 备份管理器

Automated backup management for OpenClaw configurations and critical files.
自动化备份管理系统，保护OpenClaw配置和关键文件。

## When to Use / 何时使用

**English**:
- Setting up automated backup schedules
- Before making significant configuration changes
- When needing to restore from a previous backup
- Managing backup storage and cleaning expired backups

**中文**:
- 设置自动备份计划
- 重大配置变更前创建备份
- 从之前的备份恢复系统
- 管理备份存储和清理过期备份

---

## Core Rules / 核心规则

### 1. Always Ask Before Backup / 备份前确认

**English**:
Never create backups automatically without user confirmation. Always explain what will be backed up and where.

**中文**:
未经用户确认，不要自动创建备份。始终解释将备份什么内容以及备份到何处。

### 2. Follow Retention Policies / 遵循保留策略

**English**:
Respect configured retention periods: daily (7 days), weekly (4 weeks), monthly (12 months). Never delete backups outside retention windows without confirmation.

**中文**:
尊重配置的保留周期：每日（7天）、每周（4周）、每月（12个月）。未经确认，不得删除保留期之外的备份。

### 3. Verify Backup Integrity / 验证备份完整性

**English**:
After creating a backup, verify the file exists and is readable. Report any backup failures immediately.

**中文**:
创建备份后，验证文件存在且可读。立即报告任何备份失败。

### 4. Document Backup Actions / 记录备份操作

**English**:
Record all backup operations in memory/backup-log.md with timestamps, file counts, and sizes.

**中文**:
将所有备份操作记录在memory/backup-log.md中，包括时间戳、文件数量和大小。

### 5. Safe Restoration / 安全恢复

**English**:
When restoring from backup, create a backup of current state first. Never overwrite without a safety copy.

**中文**:
从备份恢复时，先创建当前状态的备份。没有安全副本之前不要覆盖。

---

## Quick Reference / 快速参考

| Topic / 主题 | File / 文件 |
|---------------|-------------|
| Backup strategies / 备份策略 | `backup-strategies.md` |
| Script reference / 脚本参考 | `backup-scripts.md` |
| Recovery guide / 恢复指南 | `recovery-guide.md` |
| Memory template / 记忆模板 | `memory-template.md` |

---

## 🚨 Emergency Recovery / 紧急恢复

**If OpenClaw is completely broken and cannot start / 如果OpenClaw完全损坏无法启动**:

### 1. Quick Restore (2 commands) / 快速恢复（2个命令）

```bash
# List backups / 列出备份
ls -lht ~/.openclaw/backups/critical/

# Restore (replace with your backup file) / 恢复（替换为你的备份文件）
bash ~/.openclaw/workspace/skills/backup-manager/restore.sh ~/.openclaw/backups/critical/YOUR_BACKUP.tar.gz
```

### 2. Emergency Guides / 紧急指南

**English**:
- Quick guide: `~/OPENCLAW_EMERGENCY_RECOVERY.md`
- Detailed guide: `~/.openclaw/backups/README.md`

**中文**:
- 快速指南：`~/OPENCLAW_EMERGENCY_RECOVERY.md`
- 详细指南：`~/.openclaw/backups/README.md`

### 3. Important / 重要提示

**English**:
- The `restore.sh` script works WITHOUT OpenClaw running
- It's a pure bash script that can run even when OpenClaw is completely broken
- Always creates a backup of current state before restoring
- Restores from `critical/` backups first (highest priority)

**中文**:
- `restore.sh` 脚本可以在OpenClau未运行的情况下工作
- 这是一个纯bash脚本，即使OpenClaw完全损坏也能运行
- 恢复前总是创建当前状态的备份
- 优先从 `critical/` 备份恢复（最高优先级）

---

## Data Storage / 数据存储

**English**:
Backups are stored in `~/.openclaw/backups/` with a hybrid time-based directory structure:

**中文**:
备份存储在 `~/.openclaw/backups/` 目录，采用基于时间的混合目录结构：

```
~/.openclaw/backups/
├── daily/                    # Daily backups (keep 7 days) / 每日备份（保留7天）
│   ├── 2026/
│   │   ├── 03/
│   │   │   ├── 08/
│   │   │   │   ├── config_20260308_020000.tar.gz    # Config backup / 配置备份
│   │   │   │   └── critical_20260308_103015.tar.gz  # Pre-change backup / 修改前备份
│   │   │   └── 09/
│   │   └── 04/
│   └── latest -> 2026/03/08  # Latest backup symlink / 最新备份软链接
├── weekly/                   # Weekly backups (keep 4 weeks) / 每周备份（保留4周）
│   ├── 2026/
│   │   ├── w10/
│   │   │   └── full_20260308_030000.tar.gz          # Full backup / 完整备份
│   │   └── w11/
│   └── latest -> 2026/w10/
├── weekly/skills/           # Weekly custom skills backup (keep 4 weeks) / 自定义技能每周备份
│   ├── skills-custom_2026w10_20260308_033000.tar.gz # Skills backup / 技能备份
│   └── latest -> skills-custom_2026w10_20260308_033000.tar.gz
├── monthly/                  # Monthly backups (keep 12 months) / 每月备份（保留12个月）
│   ├── 2026/
│   │   ├── 03/
│   │   │   └── full_20260301_040000.tar.gz          # Full backup / 完整备份
│   │   └── 04/
│   └── latest -> 2026/03/
└── critical/                 # Pre-major-change backups (manual cleanup) / 重大修改前备份（手动清理）
    ├── before-glm-config-20260308_102514.tar.gz
    └── before-plugin-config-20260308_103015.tar.gz
```

**English**:
Memory tracking uses `memory/backup-log.md`.

**中文**:
记忆追踪使用 `memory/backup-log.md`。

---

## External Endpoints / 外部端点

**English**:
None. This skill operates entirely locally.

**中文**:
无。此技能完全在本地运行。

---

## Related Skills / 相关技能

**English**:
- `skill-vetter` — security review before installation
- `openclaw-security-scanner` — security assessment
- `healthcheck` — system hardening

**中文**:
- `skill-vetter` — 安装前的安全审查
- `openclaw-security-scanner` — 安全评估
- `healthcheck` — 系统加固

---

## Feedback / 反馈

**English**:
Report issues or suggest improvements via memory/backup-log.md.

**中文**:
通过 memory/backup-log.md 报告问题或提出改进建议。

---

## Version History / 版本历史

### v1.0.2 (2026-04-06) / 紧急恢复系统

**English**:
- Added emergency recovery system with independent restore script
- Created bilingual documentation (English + Chinese)
- Added quick emergency guides in home directory and backup directory
- Fixed recovery guide to use independent restore script
- Now users can recover even if OpenClaw is completely broken!

**中文**:
- 添加紧急恢复系统，包含独立恢复脚本
- 创建双语文档（英文+中文）
- 在主目录和备份目录添加快速紧急指南
- 修复恢复指南，使用独立恢复脚本
- 现在即使OpenClaw完全损坏也能恢复！

### v1.0.1 (2026-04-06) / 格式迁移

**English**:
- Migrate to new OpenClaw skill format
- Simplified SKILL.md frontmatter, removed slug/version from SKILL.md
- Added metadata field with emoji and requirements

**中文**:
- 迁移到新的OpenClaw技能格式
- 简化SKILL.md frontmatter，从SKILL.md中移除slug/version
- 添加metadata字段，包含emoji和依赖

### v1.0.0 (2026-03-08) / 初始版本

**English**:
- Initial release of backup management system
- Automated daily/weekly/monthly backups
- Pre-modification snapshots
- Expired backup cleanup
- Comprehensive recovery guide

**中文**:
- 备份管理系统初始发布
- 自动化每日/每周/每月备份
- 修改前快照
- 过期备份清理
- 完整恢复指南

---

**Created by / 创建者**: xichen (虾维斯)
**Last Updated / 最后更新**: 2026-04-06
