# 常见问题排查

## 故障诊断类型

AgentOps 支持以下预定义问题类型的诊断：

| 问题类型 | 说明 | 常见原因 |
|----------|------|----------|
| session_timeout | 会话超时 | Gateway停止、配置错误、网络问题 |
| high_memory | 内存过高 | 内存泄漏、并发任务过多 |
| slow_response | 响应缓慢 | 系统过载、CPU压力、API慢 |
| skill_error | 技能错误 | 技能目录缺失、SKILL.md缺失 |
| connection_error | 连接错误 | 网络断开、DNS未配置、API不可达 |
| config_error | 配置错误 | 配置文件缺失、JSON格式错误 |

## 常见排查步骤

### 1. 检查Gateway状态

```bash
# 检查进程
pgrep -f openclaw

# 检查端口
ss -tlnp | grep -E "3000|3001"

# 重启Gateway
openclaw gateway restart
```

### 2. 检查日志

```bash
# 查看最近的错误
python3 scripts/log_analyzer.py --level error

# 查看完整分析
python3 scripts/log_analyzer.py
```

### 3. 检查系统资源

```bash
# 性能快照
python3 scripts/perf_monitor.py

# 持续监控
python3 scripts/perf_monitor.py --watch 30
```

### 4. 检查配置

```bash
# 配置优化分析
python3 scripts/config_optimizer.py
```

### 5. 健康检查

```bash
# 全面检查
python3 scripts/health_check.py --check all
```

## 快速修复

| 症状 | 操作 |
|------|------|
| Gateway未运行 | `openclaw gateway start` |
| 磁盘满 | 清理 ~/.openclaw/logs 旧日志 |
| 内存过高 | 重启 gateway: `openclaw gateway restart` |
| 配置错误 | 检查 ~/.openclaw/openclaw.json JSON格式 |
| 技能加载失败 | 确保 SKILL.md 存在且格式正确 |
