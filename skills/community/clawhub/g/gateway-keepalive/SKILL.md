---
title: "Gateway Keepalive"
description: "OpenClaw Gateway 黄金包活机制，确保 7x24 小时稳定运行"
author: "康妃 (config)"
version: "1.1.0"
created: "2026-03-08"
updated: "2026-03-08"
tags: [gateway, keepalive, high-availability, launchagent, auto-recovery]
---

# Gateway Keepalive Skill (黄金包活机制)

> **用途**: 确保 OpenClaw Gateway 7x24 小时稳定运行
> 
> **触发**: 系统自动运行，无需手动触发

## 架构

```
┌─────────────────────────────────────────────────────────┐
│                    黄金包活机制                          │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1: LaunchAgent KeepAlive (秒级)                  │
│  ├─ KeepAlive: true                                     │
│  ├─ ThrottleInterval: 1 秒                              │
│  └─ 进程崩溃 → 1 秒内自动重启                            │
│                                                         │
│  Layer 2: Health Check (每分钟)                         │
│  ├─ 检测进程 + 端口 18789                               │
│  ├─ 连续失败 3 次 → 触发恢复                             │
│  ├─ 恢复黄金备份配置                                     │
│  └─ 发送通知 (系统 + Telegram)                          │
│                                                         │
│  Layer 3: 日志轮转                                      │
│  ├─ 超过 5MB 自动压缩                                   │
│  └─ 保留 30 天内的日志                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

## 安装

```bash
# 一键安装
bash ~/.openclaw/skills/gateway-keepalive/scripts/install.sh
```

## 使用

### 查看状态

```bash
# 检查服务状态
bash ~/.openclaw/skills/gateway-keepalive/scripts/status.sh

# 或直接使用 openclaw
openclaw gateway status
launchctl list | grep openclaw
```

### 查看日志

```bash
# 健康检测日志（会轮转）
tail -f ~/.openclaw/logs/health-recovery.log

# 恢复历史（永久保留）
cat ~/.openclaw/logs/recovery-history.log

# Gateway 日志
tail -f ~/.openclaw/logs/gateway.log
```

### 恢复历史

**重要**：恢复历史永久保留，不受日志轮转影响。

```bash
# 查看所有恢复记录
cat ~/.openclaw/logs/recovery-history.log

# 统计成功恢复次数
grep -c "自动恢复成功" ~/.openclaw/logs/recovery-history.log

# 统计失败次数
grep -c "自动恢复失败" ~/.openclaw/logs/recovery-history.log
```

**日志轮转规则**：
- `health-recovery.log`：超过 5MB 压缩，保留 30 天
- `recovery-history.log`：**永久保留**（只记录恢复事件）

### 更新黄金备份

**重要**: 每次重大配置变更后，更新黄金备份！

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/golden-config/openclaw.json
```

### 手动恢复

```bash
# 触发手动恢复
bash ~/.openclaw/scripts/health-check-recovery.sh
```

## 统计

查看黄金包活机制的历史效果：

```bash
# 自动恢复次数
grep -c "自动恢复成功" ~/.openclaw/logs/health-recovery.log*

# 失败次数
grep -c "自动恢复失败" ~/.openclaw/logs/health-recovery.log*

# 总检测次数
grep -c "健康检测通过" ~/.openclaw/logs/health-recovery.log*
```

## 配置参数

**核心参数**:

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ThrottleInterval` | 1 秒 | Gateway 重启间隔 |
| `StartInterval` | 60 秒 | 健康检查间隔 |
| `MAX_FAILURES` | 3 次 | 触发恢复的连续失败次数 |
| `GATEWAY_PORT` | 18789 | Gateway 端口 |
| `LOG_MAX_SIZE_MB` | 5 | 日志轮转阈值 |
| `LOG_KEEP_DAYS` | 30 | 日志保留天数 |

**通知配置**（可选）:

| 参数 | 说明 |
|------|------|
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token（可选）|
| `TELEGRAM_CHAT_ID` | Telegram Chat ID（可选）|

配置文件位置：`~/.openclaw/config/keepalive.conf`

```bash
# 编辑配置
nano ~/.openclaw/config/keepalive.conf

# 配置示例
TELEGRAM_BOT_TOKEN="123456789:ABCdef..."
TELEGRAM_CHAT_ID="123456789"
```

**注意**：
- Telegram 通知是**可选的**，不配置也正常运行
- 系统通知（macOS Notification Center）始终启用
- 敏感信息**不会**包含在发布的技能包中

## 测试指南

### 测试 Layer 1 (KeepAlive)

**目的**：验证进程崩溃后能否秒级重启

```bash
# 1. 记录当前 PID
PID=$(pgrep -f "openclaw gateway")
echo "当前 PID: $PID"

# 2. 手动杀死进程
kill -9 $PID

# 3. 等待 1-2 秒，检查是否自动重启
sleep 2
pgrep -f "openclaw gateway"

# 预期结果：进程自动重启，PID 变化
```

### 测试 Layer 2 (Health Check)

**目的**：验证健康检测和自动恢复机制

```bash
# 方法 1: 停止 Gateway LaunchAgent
launchctl stop ai.openclaw.gateway

# 等待 3-5 分钟（需要连续失败 3 次）
# 观察日志：
tail -f ~/.openclaw/logs/health-recovery.log

# 预期结果：
# - 检测到失败（❌ Gateway 进程不存在）
# - 失败计数累加（1/3, 2/3, 3/3）
# - 触发自动恢复
# - 恢复成功（✅ 自动恢复成功）

# 方法 2: 手动运行检测脚本
bash ~/.openclaw/scripts/health-check-recovery.sh
```

### 验证机制起作用

**1. 查看恢复历史**（永久保留）：
```bash
cat ~/.openclaw/logs/recovery-history.log

# 输出示例：
# [2026-03-06 23:11:52] 🚨 触发自动恢复 - 原因: Gateway 进程不存在
# [2026-03-06 23:12:09] ✅ 自动恢复成功
```

**2. 统计恢复次数**：
```bash
# 成功次数
grep -c "自动恢复成功" ~/.openclaw/logs/recovery-history.log

# 失败次数
grep -c "自动恢复失败" ~/.openclaw/logs/recovery-history.log

# 总触发次数
grep -c "触发自动恢复" ~/.openclaw/logs/recovery-history.log
```

**3. 检查 LaunchAgent 状态**：
```bash
# 查看服务是否运行
launchctl list | grep openclaw

# 预期输出：
# 66266  -15  ai.openclaw.gateway
# -      0    com.openclaw.health-check

# 第一列是 PID（- 表示服务在运行但无进程）
# 第二列是退出码（0 = 正常，-15 = 被信号终止）
```

**4. 查看实时日志**：
```bash
# 健康检测日志
tail -f ~/.openclaw/logs/health-recovery.log

# 每分钟应该看到：
# [2026-03-08 10:30:00] 🔍 开始健康检测
# [2026-03-08 10:30:00] ✅ 健康检测通过
# [2026-03-08 10:30:00] ✅ 黄金备份已更新（健康检测通过）
```

### 快速状态检查

```bash
# 一键检查
~/.openclaw/skills/gateway-keepalive/scripts/status.sh

# 或手动检查
openclaw gateway status          # Gateway 状态
launchctl list | grep openclaw   # LaunchAgent 状态
cat ~/.openclaw/state/recovery-count  # 失败计数
```

## 故障排查

### Gateway 无法启动

```bash
tail -50 ~/.openclaw/logs/gateway.err.log
openclaw gateway config
openclaw gateway start
```

### 健康检查失败

```bash
bash ~/.openclaw/scripts/health-check-recovery.sh
cat ~/.openclaw/state/recovery-count
```

### 自动恢复失败

```bash
ls -la ~/.openclaw/backups/golden-config/
cp ~/.openclaw/backups/golden-config/openclaw.json ~/.openclaw/openclaw.json
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

## 卸载

```bash
# 一键卸载
bash ~/.openclaw/skills/gateway-keepalive/scripts/uninstall.sh
```

## 文件清单

```
~/.openclaw/skills/gateway-keepalive/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── install.sh                    # 安装脚本
│   ├── uninstall.sh                  # 卸载脚本
│   └── status.sh                     # 状态检查
└── docs/
    └── gateway-keepalive-setup-guide.md  # 详细安装指南

~/.openclaw/scripts/
└── health-check-recovery.sh          # 健康检测脚本

~/Library/LaunchAgents/
├── ai.openclaw.gateway.plist         # Gateway LaunchAgent
└── com.openclaw.health-check.plist   # 健康检测 LaunchAgent

~/.openclaw/backups/golden-config/
└── openclaw.json                     # 黄金备份配置
```

## 依赖

- **系统**: macOS (LaunchAgent)
- **OpenClaw**: 2026.3.2+
- **端口**: 18789 (可配置)

## 维护者

- **康妃 (config)** - 配置管理与系统稳定性

## 更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-08 | 1.1.0 | 添加日志轮转机制，打包为 skill |
| 2026-03-07 | 1.0.0 | 初始版本 |
