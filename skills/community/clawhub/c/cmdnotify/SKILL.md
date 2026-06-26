---
name: cmdnotify
description: Lightweight command monitoring tool that periodically executes local commands/scripts in batches, detects output changes, and triggers alerts. Built with Go for minimal resource consumption.
tags: [monitoring, alerting, devops, system, go, cli]
author: qhz.hetu
version: 1.0.0
---

# CmdNotify - Command Monitor Skill

## 触发词

当用户提到以下关键词时激活此技能：
- "监控命令"
- "命令告警"
- "定时执行脚本"
- "输出变化检测"
- "cmdnotify"
- "command monitor"
- "batch script execution"

## 使用场景

- 批量监控多个系统命令的输出变化
- 定时执行脚本并检测异常
- 磁盘使用率、内存、进程数等系统指标监控
- API 健康检查与状态变化告警
- 配置文件漂移检测
- 日志模式监控

## Overview

CmdNotify is a lightweight, resource-optimized command monitoring system written in Go. It allows you to:

- **Batch monitor** multiple commands/scripts simultaneously
- Set **custom execution intervals** for each command
- Automatically **detect output changes** (stdout/stderr + exit code)
- **Trigger alerts** when changes are detected
- Run with **minimal CPU/memory footprint** using goroutine pools and timeouts

## Quick Start

### 1. Configuration

Create a `config.json` file:

```json
{
  "commands": [
    {
      "name": "disk_usage",
      "command": "df -h /",
      "interval": "30s",
      "timeout": "10s",
      "notify_on": ["change"],
      "max_history": 2
    },
    {
      "name": "memory_check",
      "command": "vm_stat | grep 'Pages free'",
      "interval": "20s",
      "timeout": "5s",
      "notify_on": ["change"],
      "notify_cmd": "echo '[ALERT] $CMD_NAME: $CMD_MESSAGE'",
      "max_history": 2
    }
  ]
}
```

### 2. Build & Run

```bash
# Build
go build -o cmdnotify .

# Run with default config
./cmdnotify

# Run with custom config
./cmdnotify -config /path/to/config.json
```

## Configuration Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | string | required | Unique identifier for the command |
| `command` | string | required | Shell command to execute |
| `interval` | duration | `1s` | Execution interval (e.g., `30s`, `5m`, `1h`) |
| `timeout` | duration | `30s` | Maximum execution time per run |
| `notify_on` | []string | `[]` | Events to notify on: `["change"]`, `["error"]`, `["all"]` |
| `notify_cmd` | string | `""` | Custom notification command (optional) |
| `max_history` | int | `2` | Number of results to keep for change detection |
| `working_dir` | string | `""` | Working directory for command execution |

## Notification

### Default Behavior
When no `notify_cmd` is specified, alerts are printed to `stderr`:
```
[disk_usage] Command 'disk_usage' output changed
Exit code: 0
Output:
Filesystem      Size   Used  Avail Capacity
/dev/disk1s1   228Gi  180Gi   48Gi    79%
```

### Custom Notification
Set `notify_cmd` to integrate with external systems:

```json
{
  "notify_cmd": "curl -X POST -d '{\"text\":\"$CMD_MESSAGE\"}' https://hooks.slack.com/services/..."
}
```

Environment variables available in `notify_cmd`:
- `CMD_NAME` - Command name
- `CMD_MESSAGE` - Alert message

## Resource Optimization

CmdNotify is designed for minimal resource consumption:

| Feature | Implementation |
|---------|---------------|
| **Goroutine Pool** | Semaphore-based concurrency limiting (default: CPU count, min 4) |
| **Timeout Control** | Per-command `context.WithTimeout` prevents zombie processes |
| **Memory Reuse** | `bytes.Buffer` for output; history limited to `max_history` |
| **Efficient Hashing** | SHA-256 of output + exit code for fast change detection |
| **Graceful Shutdown** | `context.Cancel` + `sync.WaitGroup` ensures clean exit |

## Project Structure

```
CmdNotify/
├── config.go      # Configuration loading & validation
├── config.json    # Example configuration
├── executor.go    # Command execution & change detection
├── scheduler.go   # Scheduling engine with goroutine pool
├── main.go        # Entry point
└── go.mod         # Go module definition
```

## Use Cases

- Monitor disk usage changes
- Track process counts
- Watch log file patterns
- Check service health endpoints
- Detect configuration drift
- Monitor system resource usage

## Advanced Example

```json
{
  "commands": [
    {
      "name": "api_health",
      "command": "curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/health",
      "interval": "10s",
      "timeout": "5s",
      "notify_on": ["change", "error"],
      "notify_cmd": "echo '[$(date)] $CMD_NAME status changed: $CMD_MESSAGE' >> /var/log/alerts.log",
      "max_history": 3
    },
    {
      "name": "db_connection_count",
      "command": "psql -c 'SELECT count(*) FROM pg_stat_activity;' -t",
      "interval": "1m",
      "timeout": "10s",
      "notify_on": ["all"],
      "working_dir": "/opt/monitoring"
    }
  ]
}
```
