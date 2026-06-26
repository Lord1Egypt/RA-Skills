# Backup Manager Memory Template

## Backup Configuration

### Retention Policies
```yaml
daily_retention_days: 7
weekly_retention_weeks: 4
monthly_retention_months: 12
critical_retention: "manual"  # manual, 1year, permanent
```

### Backup Targets
```yaml
openclaw_config:
  - ~/.openclaw/openclaw.json
  - ~/.openclaw/agents/main/agent/models.json
  - ~/.openclaw/agents/main/agent/agent.json

workspace_files:
  - MEMORY.md
  - USER.md
  - SOUL.md
  - IDENTITY.md
  - LAOCHEN_TODOLIST.md
  - XIACHEN_TODOLIST.md
  - OUR_TODOLIST.md
  - HEARTBEAT.md
  - TOOLS.md

skill_configs:
  - skills/skill-vetter/
  - skills/openclaw-security-scanner/
  - skills/skill-builder/
  - skills/backup-manager/
```

### Schedule Configuration
```yaml
daily_backup_time: "02:00"
weekly_backup_day: "monday"
weekly_backup_time: "03:00"
monthly_backup_day: 1
monthly_backup_time: "04:00"
cleanup_time: "05:00"
```

## Backup History

### Recent Backups
```yaml
last_daily_backup:
  timestamp: "2026-03-08 02:00:00"
  directory: "~/.openclaw/backups/daily/20260308_020000"
  file_count: 12
  total_size: "1.2MB"
  status: "success"

last_weekly_backup:
  timestamp: "2026-03-07 03:00:00"
  directory: "~/.openclaw/backups/weekly/2026-w10"
  file_count: 12
  total_size: "1.2MB"
  status: "success"

last_monthly_backup:
  timestamp: "2026-03-01 04:00:00"
  directory: "~/.openclaw/backups/monthly/2026-03"
  file_count: 12
  total_size: "1.2MB"
  status: "success"
```

### Critical Backups
```yaml
critical_backups:
  - reason: "before-glm-config"
    timestamp: "2026-03-08 10:25:14"
    directory: "~/.openclaw/backups/critical/before-glm-config-20260308_102514"
    notes: "智谱API配置变更前"

  - reason: "before-plugin-config"
    timestamp: "2026-03-08 10:30:15"
    directory: "~/.openclaw/backups/critical/before-plugin-config-20260308_103015"
    notes: "memory-lancedb-pro插件配置前"

  - reason: "before-security-scan"
    timestamp: "2026-03-08 11:47:00"
    directory: "~/.openclaw/backups/critical/before-security-scan-20260308_114700"
    notes: "首次安全扫描前"
```

## Cleanup History

### Recent Cleanups
```yaml
last_cleanup:
  timestamp: "2026-03-08 05:00:00"
  deleted_daily: 3
  deleted_weekly: 1
  deleted_monthly: 0
  freed_space: "3.6MB"
  status: "success"
```

### Cleanup Statistics
```yaml
cleanup_stats:
  total_daily_deleted: 24
  total_weekly_deleted: 8
  total_monthly_deleted: 2
  total_freed_space: "28.8MB"
  last_30_days_cleanups: 30
```

## Recovery History

### Recent Recoveries
```yaml
recoveries:
  - timestamp: "2026-03-08 11:30:00"
    backup_source: "~/.openclaw/backups/daily/20260308_020000"
    reason: "测试恢复流程"
    files_restored: 12
    status: "success"
    notes: "测试目的，恢复后立即回滚"
```

## Performance Metrics

### Backup Performance
```yaml
performance:
  average_backup_time: "45s"
  average_backup_size: "1.2MB"
  backup_success_rate: "100%"
  last_failure: null
  compression_ratio: "60%"  # 如果启用压缩
```

### Storage Usage
```yaml
storage:
  total_backups: 42
  total_size: "50.4MB"
  daily_usage: "8.4MB"
  weekly_usage: "4.8MB"
  monthly_usage: "14.4MB"
  critical_usage: "22.8MB"
  available_space: "45.6GB"
  usage_percentage: "0.11%"
```

## Configuration Changes

### Recent Config Updates
```yaml
config_changes:
  - timestamp: "2026-03-08 11:54:00"
    change: "新增backup-manager技能"
    affected_files:
      - "skills/backup-manager/SKILL.md"
      - "skills/backup-manager/backup-strategies.md"
      - "skills/backup-manager/backup-scripts.md"
      - "skills/backup-manager/recovery-guide.md"
      - "skills/backup-manager/memory-template.md"
    backup_created: true
    backup_location: "~/.openclaw/backups/critical/before-backup-manager-20260308_115400"
```

## Issues and Alerts

### Active Issues
```yaml
active_issues: []
```

### Resolved Issues
```yaml
resolved_issues:
  - issue: "备份目录权限过宽"
    detected: "2026-03-08 11:47:00"
    resolved: "2026-03-08 11:50:00"
    solution: "chmod 700 ~/.openclaw/backups"
    severity: "warning"
```

### Alerts Configuration
```yaml
alerts:
  low_storage_threshold: "1GB"
  failed_backup_alert: true
  failed_cleanup_alert: true
  recovery_alert: true
  alert_channels:
    - "openclaw-control-ui"
    - "memory/backup-log.md"
```

## User Preferences

### Notification Preferences
```yaml
notifications:
  daily_backup: false
  weekly_backup: false
  monthly_backup: false
  cleanup_operations: false
  recovery_operations: true
  storage_warnings: true
  failed_operations: true
```

### Automation Preferences
```yaml
automation:
  auto_backup: true
  auto_cleanup: true
  auto_verify: true
  require_confirmation: true
  confirmation_level: "medium"  # low, medium, high
```

### Security Preferences
```yaml
security:
  encrypt_backups: false
  backup_verification: true
  log_integrity_check: true
  access_logging: true
  retention_enforcement: true
```

## Skill Integration

### Integrated Skills
```yaml
integrated_skills:
  skill-vetter:
    integration: "pre-install-check"
    status: "active"
    
  openclaw-security-scanner:
    integration: "security-audit"
    status: "active"
    
  healthcheck:
    integration: "system-health"
    status: "pending"
```

### Integration Status
```yaml
integration_status:
  setup_complete: true
  scripts_configured: true
  cron_jobs_configured: false
  permissions_verified: true
  test_backup_complete: true
  test_recovery_complete: false
```

## Maintenance Schedule

### Upcoming Maintenance
```yaml
maintenance:
  next_verification: "2026-03-15"
  next_test_restore: "2026-04-01"
  next_config_review: "2026-06-01"
  next_storage_audit: "2026-07-01"
```

### Maintenance History
```yaml
maintenance_history:
  - date: "2026-03-08"
    task: "初始设置"
    status: "completed"
    notes: "创建backup-manager技能"
```

---

## Usage Notes

### 如何更新此内存
1. **备份操作后**：自动更新备份历史部分
2. **配置变更后**：更新配置变更部分
3. **定期维护**：每月审查和更新所有部分
4. **问题解决后**：更新问题与警报部分

### 数据一致性
- 此模板与`~/.openclaw/workspace/memory/backup-log.md`同步
- 关键变更需要同时更新两个文件
- 定期验证数据一致性

### 备份策略
- 此文件本身应包含在备份目标中
- 重大变更前创建此文件的备份
- 定期审查和优化内存结构
