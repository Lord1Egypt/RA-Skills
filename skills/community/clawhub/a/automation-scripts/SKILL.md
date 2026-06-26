# Automation Scripts Skill

> 自动化脚本管理 - 创建、执行、维护自动化任务

## 功能

- 脚本模板库
- 定时任务管理
- 执行日志记录
- 失败自动重试
- 状态通知

## 脚本分类

| 类别 | 说明 | 示例 |
|------|------|------|
| 监控 | 系统监控 | 健康检查、磁盘监控 |
| 备份 | 数据备份 | 配置备份、日志清理 |
| 同步 | 数据同步 | Git自动提交、文件同步 |
| 报告 | 报告生成 | 日报、周报、月报 |
| 研究 | 自动化研究 | GitHub项目分析 |

## 使用方法

```bash
# 列出可用脚本
skill:automation-scripts --list

# 创建新脚本
skill:automation-scripts --create --name "my-script" --type "monitor"

# 执行脚本
skill:automation-scripts --run "script-name"

# 查看执行日志
skill:automation-scripts --log "script-name"

# 定时执行
skill:automation-scripts --schedule "script-name" --cron "0 6 * * *"

# 禁用脚本
skill:automation-scripts --disable "script-name"

# 启用脚本
skill:automation-scripts --enable "script-name"
```

## 内置脚本模板

### 1. 健康检查脚本

```bash
#!/bin/bash
# OpenClaw 健康检查
# 位置: ~/scripts/openclaw-health-check.sh

# 检查项目
- 服务状态 (Gateway进程)
- 配置文件语法
- 磁盘空间
- 内存使用
- 日志错误

# 输出格式
✓ 检查通过
✗ 检查失败 (显示原因)
```

### 2. 自动备份脚本

```bash
#!/bin/bash
# 配置自动备份
# 位置: ~/scripts/backup-openclaw-config.sh

# 功能
- 每日自动备份配置
- 保留30天历史
- 清理旧备份

# 配置
BACKUP_DIR="~/.openclaw/backups"
RETENTION_DAYS=30
```

### 3. Git 自动同步脚本

```bash
#!/bin/bash
# Git 自动同步
# 位置: ~/scripts/auto-git-sync.sh

# 功能
- 检查文件变更
- 自动 add + commit
- 自动 push
- 记录同步日志
```

### 4. 定时报告脚本

```bash
#!/bin/bash
# 定时报告生成
# 位置: ~/scripts/daily-report.sh

# 功能
- 生成日报
- 发送到指定位置
- 记录发送状态
```

### 5. OpenCode 集成脚本

```bash
#!/bin/bash
# OpenCode 自动修复
# 位置: ~/scripts/opencode-auto-fix.sh

# 功能
- 检测服务故障
- 调用 OpenCode 诊断
- 自动修复
- 验证结果
```

## 脚本结构

```
scripts/
├── templates/           # 脚本模板
│   ├── monitor.sh
│   ├── backup.sh
│   ├── sync.sh
│   └── report.sh
├── custom/             # 自定义脚本
├── logs/               # 执行日志
└── config.conf         # 全局配置
```

## 配置示例

```json
{
  "automation": {
    "enabled": true,
    "logRetentionDays": 30,
    "maxRetries": 3,
    "retryDelay": 60,
    "notifications": {
      "onFailure": true,
      "onSuccess": false
    }
  }
}
```

## 执行日志

| 字段 | 说明 |
|------|------|
| timestamp | 执行时间 |
| script | 脚本名称 |
| status | success/failure |
| duration | 执行耗时 |
| output | 输出摘要 |
| error | 错误信息（如有） |

## 最佳实践

1. **脚本命名**
   - 使用描述性名称
   - 包含类型前缀: `backup-`, `monitor-`, `sync-`

2. **错误处理**
   - 总是检查返回值
   - 失败时发送通知
   - 保留错误日志

3. **日志管理**
   - 记录执行详情
   - 定期清理旧日志
   - 分析失败模式

4. **定时任务**
   - 避免高峰期执行
   - 设置合理重试
   - 监控执行状态
