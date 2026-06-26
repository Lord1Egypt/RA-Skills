---
name: backup-restore
description: "系统备份恢复 - 全量备份、增量备份、自动备份计划、一键恢复、备份验证。保护配置、数据、技能和工作区。"
version: 1.0.0
---

# Backup & Restore - 系统备份恢复技能

## 核心功能

- ✅ 全量备份
- ✅ 增量备份
- ✅ 自动备份计划
- ✅ 一键恢复
- ✅ 备份验证

## 备份范围

| 类型 | 内容 | 路径 |
|------|------|------|
| **配置** | openclaw.json, cron/jobs.json, crons.json(兼容) 等 | `~/.openclaw/` |
| **数据** | memory/, workspace/ | `~/.openclaw/workspace/` |
| **技能** | skills/ | `~/.openclaw/workspace/skills/` |
| **Agent** | 所有 Agent 工作区 | `~/.openclaw/workspace-*/` |

## 使用方法

### 全量备份

```bash
python backup-restore.py full
```

### 增量备份

```bash
python backup-restore.py incremental
```

### 恢复备份

```bash
python backup-restore.py restore --backup <backup_file>
```

### 验证备份

```bash
python backup-restore.py verify --backup <backup_file>
```

## 自动备份计划

推荐配置（添加到 Cron）：

```json
{
  "id": "daily-backup",
  "name": "每日备份",
  "schedule": "0 2 * * *",
  "command": "python backup-restore.py incremental",
  "agent": "main"
}
```

## 备份保留策略

- 每日备份：保留 7 天
- 每周备份：保留 4 周
- 每月备份：保留 12 个月

## 注意事项

1. 备份前停止 Cron 调度器
2. 验证备份完整性
3. 定期测试恢复流程
4. 备份到外部存储（可选）
