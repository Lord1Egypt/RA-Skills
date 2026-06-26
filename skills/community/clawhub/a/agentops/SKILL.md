---
name: agentops
description: >
  OpenClaw Agent运维管理工具。Trigger when user mentions: Agent运维, agentops,
  Agent健康检查, 日志分析, 性能监控, 告警, Agent配置, 故障诊断, Agent协调,
  运维报告, 性能报告, Agent管理, 系统监控.
  Supports freemium: free (健康检查/日志分析/基础性能监控)
  and premium (配置优化/自动化告警/多Agent协调/故障诊断/性能报告).
---

# AgentOps — Agent运维管理

面向OpenClaw Agent用户的运维管理工具。与OpenClaw生态深度绑定。

## 功能分级

| 功能 | 等级 | 脚本 | 说明 |
|------|------|------|------|
| Agent健康检查 | 免费 | `scripts/health_check.py` | 检查Agent运行状态、会话健康、配置有效性 |
| 日志分析 | 免费 | `scripts/log_analyzer.py` | 分析OpenClaw日志，提取错误/警告/异常 |
| 性能监控 | 免费 | `scripts/perf_monitor.py` | 系统资源、Agent响应时间、会话统计 |
| 配置优化 | 付费 | `scripts/config_optimizer.py` | 分析配置并提供优化建议 |
| 自动化告警 | 付费 | `scripts/alert_manager.py` | 设置阈值告警规则 |
| 多Agent协调 | 付费 | `scripts/multi_agent_coordinator.py` | 多Agent间依赖与协调分析 |
| 故障诊断 | 付费 | `scripts/diagnostic.py` | 根因分析与故障定位 |
| 性能报告 | 付费 | `scripts/perf_report.py` | 生成综合性能报告 |

## 使用流程

### 1. Agent健康检查（免费）

```bash
# 检查OpenClaw服务状态
python3 scripts/health_check.py --check service

# 检查Agent会话状态
python3 scripts/health_check.py --check session

# 检查配置有效性
python3 scripts/health_check.py --check config

# 全面检查
python3 scripts/health_check.py --check all

# JSON输出
python3 scripts/health_check.py --check all --json
```

### 2. 日志分析（免费）

```bash
# 分析默认位置的OpenClaw日志
python3 scripts/log_analyzer.py

# 分析指定日志文件
python3 scripts/log_analyzer.py --log-file /path/to/logfile

# 按级别过滤
python3 scripts/log_analyzer.py --level error

# 输出JSON
python3 scripts/log_analyzer.py --json

# 按时间段分析
python3 scripts/log_analyzer.py --since "2024-01-01" --until "2024-01-31"
```

### 3. 性能监控（免费）

```bash
# 当前性能快照
python3 scripts/perf_monitor.py

# 持续监控（每30秒采样）
python3 scripts/perf_monitor.py --watch 30

# JSON输出
python3 scripts/perf_monitor.py --json
```

### 4. 配置优化（付费）

```bash
python3 scripts/config_optimizer.py

# 分析指定配置文件
python3 scripts/config_optimizer.py --config-file ~/.openclaw/openclaw.json

# 输出优化建议为Markdown
python3 scripts/config_optimizer.py --format markdown
```

### 5. 自动化告警（付费）

```bash
# 列出当前告警规则
python3 scripts/alert_manager.py --action list

# 添加CPU使用率告警
python3 scripts/alert_manager.py --action add --metric cpu --threshold 90 --operator gt

# 添加内存告警
python3 scripts/alert_manager.py --action add --metric memory --threshold 80 --operator gt

# 检查当前是否触发告警
python3 scripts/alert_manager.py --action check
```

### 6. 多Agent协调（付费）

```bash
# 分析Agent依赖关系
python3 scripts/multi_agent_coordinator.py --action dependencies

# 查看Agent拓扑
python3 scripts/multi_agent_coordinator.py --action topology

# 检查冲突
python3 scripts/multi_agent_coordinator.py --action conflicts
```

### 7. 故障诊断（付费）

```bash
python3 scripts/diagnostic.py

# 诊断特定问题
python3 scripts/diagnostic.py --issue "session_timeout"
python3 scripts/diagnostic.py --issue "high_memory"
```

### 8. 性能报告（付费）

```bash
python3 scripts/perf_report.py

# 生成指定时间范围报告
python3 scripts/perf_report.py --period 7d

# 输出到文件
python3 scripts/perf_report.py --output report.md
```

## 参考文档

- OpenClaw配置参考 → `references/openclaw_config_reference.md`
- 性能指标说明 → `references/metrics_reference.md`
- 常见问题排查 → `references/troubleshooting.md`

## 注意事项

- 健康检查、日志分析、性能监控为基础功能，无需付费
- 高级功能需要AgentOps Pro订阅
- 所有建议仅供参考，请结合实际情况判断
- 脚本依赖Python 3.8+环境
