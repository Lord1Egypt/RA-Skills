# Auto-Heal Skill

全天自动监控 OpenClaw 状态，检测到卡死自动修复。

## 触发条件

当用户询问以下问题时激活：
- "自动修复卡死"
- "监控 OpenClaw"
- "自动重启"
- "健康检查"
- "防止卡死"
- "守护进程"

## 功能

### 1. Gateway 监控
- 每 60 秒检查一次 gateway 状态
- 如果无响应或异常，自动重启

### 2. Agent 会话监控
- 检测卡死的 Agent 会话（30分钟无响应）
- 自动清理僵尸会话

### 3. 内存监控
- 监控 OpenClaw 内存使用
- 超过 80% 时自动清理和重启

### 4. 日志记录
- 所有操作记录到 `logs/auto-heal.log`
- 状态保存到 `state.json`

## 使用方法

### 启动监控
```bash
# 前台运行
node ~/.openclaw/workspace/skills/auto-heal/monitor.js

# 后台运行
nohup node ~/.openclaw/workspace/skills/auto-heal/monitor.js > /dev/null 2>&1 &
```

### 使用 Cron 定时任务（推荐）
```bash
# 编辑 crontab
crontab -e

# 添加每5分钟检查一次
*/5 * * * * cd ~/.openclaw/workspace/skills/auto-heal && node monitor.js --check-once
```

### 手动检查
```bash
openclaw health check
```

## 配置

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "skills": {
    "auto-heal": {
      "enabled": true,
      "checkInterval": 60,
      "autoFix": true,
      "memoryThreshold": 80,
      "notifyChannel": "feishu"
    }
  }
}
```

## 工作流程

```
启动监控
    ↓
每60秒执行健康检查
    ↓
检查 Gateway 状态
检查 Agent 会话
检查内存使用
    ↓
发现问题？
    ↓ 是
自动修复
    ↓
记录日志
    ↓
等待下一次检查
```

## 日志查看

```bash
# 实时查看日志
tail -f ~/.openclaw/workspace/skills/auto-heal/logs/auto-heal.log

# 查看最近100行
tail -n 100 ~/.openclaw/workspace/skills/auto-heal/logs/auto-heal.log
```

## 状态查看

```bash
cat ~/.openclaw/workspace/skills/auto-heal/state.json
```

## 注意事项

1. 监控脚本需要 `openclaw` CLI 可用
2. 确保有足够的权限执行重启命令
3. 日志文件会定期清理（保留7天）
4. 如果自动修复失败，会记录错误日志
