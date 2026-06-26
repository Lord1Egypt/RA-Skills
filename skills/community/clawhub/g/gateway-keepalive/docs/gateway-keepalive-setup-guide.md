# OpenClaw Gateway 黄金包活机制 - 安装指南

> **作者**: 康妃 (config)  
> **创建时间**: 2026-03-07  
> **版本**: 1.0  
> **适用系统**: macOS

---

## 📋 概述

**黄金包活机制**是 OpenClaw Gateway 的高可用保障系统，包含两层保护：

1. **Layer 1: Gateway LaunchAgent** - 进程级自动重启
2. **Layer 2: Health Check** - 应用级健康检测 + 自动恢复

### 架构图

```
┌─────────────────────────────────────────────────────────┐
│                   黄金包活机制                            │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Layer 1: LaunchAgent (秒级)                            │
│  ├─ KeepAlive: true                                     │
│  ├─ ThrottleInterval: 1                                 │
│  └─ 进程崩溃 → 立即重启                                  │
│                                                         │
│  Layer 2: Health Check (分钟级)                         │
│  ├─ StartInterval: 60 秒                                │
│  ├─ 检测端口 18789                                      │
│  ├─ 连续失败 3 次 → 自动恢复                             │
│  └─ 恢复到黄金备份配置                                   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## 🛠️ 安装步骤

### Step 1: 创建黄金备份目录

```bash
mkdir -p ~/.openclaw/backups/golden-config
mkdir -p ~/.openclaw/logs
mkdir -p ~/.openclaw/state
```

### Step 2: 创建黄金备份

**重要**: 必须在系统正常运行时创建！

```bash
# 复制当前配置作为黄金备份
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/golden-config/openclaw.json

# 创建元数据
cat > ~/.openclaw/backups/golden-config/metadata.json <<'EOF'
{
  "created_at": "$(date -Iseconds)",
  "description": "黄金备份 - 已验证可用的稳定配置",
  "verified": true
}
EOF
```

### Step 3: 创建 Gateway LaunchAgent

```bash
cat > ~/Library/LaunchAgents/ai.openclaw.gateway.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
  <dict>
    <key>Label</key>
    <string>ai.openclaw.gateway</string>
    
    <key>Comment</key>
    <string>OpenClaw Gateway (v2026.3.2)</string>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>ThrottleInterval</key>
    <integer>1</integer>
    
    <key>Umask</key>
    <integer>63</integer>
    
    <key>ProgramArguments</key>
    <array>
      <string>/opt/homebrew/opt/node/bin/node</string>
      <string>/opt/homebrew/lib/node_modules/openclaw/dist/index.js</string>
      <string>gateway</string>
      <string>--port</string>
      <string>18789</string>
    </array>
    
    <key>StandardOutPath</key>
    <string>/Users/你的用户名/.openclaw/logs/gateway.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/你的用户名/.openclaw/logs/gateway.err.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
      <key>HOME</key>
      <string>/Users/你的用户名</string>
      <key>PATH</key>
      <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
  </dict>
</plist>
EOF
```

**注意**: 替换 `你的用户名` 为实际用户名！

### Step 4: 创建健康检查脚本

```bash
cat > ~/.openclaw/scripts/health-check-recovery.sh <<'EOF'
#!/bin/bash
# OpenClaw 健康检测与自动恢复

# ============ 配置 ============
GOLDEN_CONFIG="$HOME/.openclaw/backups/golden-config/openclaw.json"
CURRENT_CONFIG="$HOME/.openclaw/openclaw.json"
LOG_FILE="$HOME/.openclaw/logs/health-recovery.log"
STATE_FILE="$HOME/.openclaw/state/recovery-count"
MAX_FAILURES=3
GATEWAY_PORT=18789

# ============ 初始化 ============
mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$STATE_FILE")"

if [ ! -f "$STATE_FILE" ]; then
    echo "0" > "$STATE_FILE"
fi

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# ============ 检测 Gateway ============
check_gateway() {
    # 1. 检查进程
    if ! pgrep -f "openclaw gateway" > /dev/null; then
        echo "Gateway 进程不存在"
        return 1
    fi
    
    # 2. 检查端口
    if ! nc -z localhost "$GATEWAY_PORT" 2>/dev/null; then
        echo "端口 $GATEWAY_PORT 无响应"
        return 1
    fi
    
    return 0
}

# ============ 自动恢复 ============
recover() {
    log "⚠️ 触发自动恢复..."
    
    # 恢复黄金配置
    if [ -f "$GOLDEN_CONFIG" ]; then
        cp "$GOLDEN_CONFIG" "$CURRENT_CONFIG"
        log "✅ 已恢复黄金配置"
    else
        log "❌ 黄金配置不存在"
        return 1
    fi
    
    # 重启 Gateway
    launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
    sleep 5
    
    # 验证恢复
    if check_gateway > /dev/null 2>&1; then
        log "✅ 恢复成功"
        echo "0" > "$STATE_FILE"
        return 0
    else
        log "❌ 恢复失败"
        return 1
    fi
}

# ============ 主流程 ============
FAILURE_COUNT=$(cat "$STATE_FILE")

if ! check_gateway; then
    FAILURE_COUNT=$((FAILURE_COUNT + 1))
    echo "$FAILURE_COUNT" > "$STATE_FILE"
    
    log "检测失败 ($FAILURE_COUNT/$MAX_FAILURES)"
    
    if [ "$FAILURE_COUNT" -ge "$MAX_FAILURES" ]; then
        recover
    fi
else
    # 重置计数器
    echo "0" > "$STATE_FILE"
fi
EOF

chmod +x ~/.openclaw/scripts/health-check-recovery.sh
```

### Step 5: 创建健康检查 LaunchAgent

```bash
cat > ~/Library/LaunchAgents/com.openclaw.health-check.plist <<'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.health-check</string>
    
    <key>Comment</key>
    <string>OpenClaw 自动健康检测与恢复服务</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/你的用户名/.openclaw/scripts/health-check-recovery.sh</string>
    </array>
    
    <key>StartInterval</key>
    <integer>60</integer>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/你的用户名/.openclaw/logs/health-check.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/你的用户名/.openclaw/logs/health-check.err.log</string>
    
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
    </dict>
</dict>
</plist>
EOF
```

**注意**: 替换 `你的用户名` 为实际用户名！

### Step 6: 加载 LaunchAgents

```bash
# 加载 Gateway
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist

# 加载健康检查
launchctl load ~/Library/LaunchAgents/com.openclaw.health-check.plist
```

---

## ✅ 验证安装

### 检查服务状态

```bash
# 检查 Gateway 是否运行
launchctl list | grep gateway

# 检查健康检查是否运行
launchctl list | grep health-check

# 检查 Gateway 进程
pgrep -f "openclaw gateway"

# 检查端口
nc -z localhost 18789 && echo "端口正常" || echo "端口无响应"
```

### 模拟故障测试

```bash
# 1. 手动停止 Gateway
launchctl stop ai.openclaw.gateway

# 2. 等待 1-2 秒，应该自动重启
sleep 2

# 3. 检查是否恢复
pgrep -f "openclaw gateway"
```

### 查看日志

```bash
# Gateway 日志
tail -f ~/.openclaw/logs/gateway.log

# 健康检查日志
tail -f ~/.openclaw/logs/health-check.log

# 恢复日志
tail -f ~/.openclaw/logs/health-recovery.log
```

---

## 🔧 配置说明

### 可调参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `ThrottleInterval` | 1 秒 | Gateway 重启间隔 |
| `StartInterval` | 60 秒 | 健康检查间隔 |
| `MAX_FAILURES` | 3 次 | 触发恢复的连续失败次数 |
| `GATEWAY_PORT` | 18789 | Gateway 端口 |

### 调整建议

- **快速恢复**: 减小 `StartInterval`（如 30 秒）
- **减少误报**: 增加 `MAX_FAILURES`（如 5 次）
- **慢速恢复**: 增加 `ThrottleInterval`（如 5 秒）

---

## 📊 监控与维护

### 日志轮转机制

健康检测日志会自动轮转，防止无限增长：

| 配置 | 值 | 说明 |
|------|-----|------|
| `LOG_MAX_SIZE_MB` | 5 | 超过 5MB 触发压缩 |
| `LOG_KEEP_DAYS` | 30 | 保留 30 天内的日志 |

**轮转流程**：
1. 日志超过 5MB → gzip 压缩
2. 压缩文件命名：`health-recovery.log.YYYYMMDD-HHMMSS.gz`
3. 自动删除 30 天前的旧日志

**压缩效果**：3MB → 76KB（压缩率 ~97%）

**手动轮转**：
```bash
# 查看日志大小
du -h ~/.openclaw/logs/health-recovery.log

# 手动触发轮转
gzip -c ~/.openclaw/logs/health-recovery.log > ~/.openclaw/logs/health-recovery.log.$(date +%Y%m%d-%H%M%S).gz
> ~/.openclaw/logs/health-recovery.log
```

### 定期检查

```bash
# 每周检查一次
crontab -e

# 添加
0 0 * * 0 tail -20 ~/.openclaw/logs/health-recovery.log | grep -c "恢复成功"
```

### 更新黄金备份

**重要**: 每次重大配置变更后，更新黄金备份！

```bash
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/golden-config/openclaw.json
```

---

## 🚨 故障排查

### Gateway 无法启动

```bash
# 检查日志
tail -50 ~/.openclaw/logs/gateway.err.log

# 检查配置
openclaw gateway config

# 手动启动
openclaw gateway start
```

### 健康检查失败

```bash
# 手动运行检查脚本
bash ~/.openclaw/scripts/health-check-recovery.sh

# 检查失败计数
cat ~/.openclaw/state/recovery-count
```

### 自动恢复失败

```bash
# 检查黄金备份是否存在
ls -la ~/.openclaw/backups/golden-config/

# 检查权限
ls -la ~/.openclaw/scripts/health-check-recovery.sh

# 手动恢复
cp ~/.openclaw/backups/golden-config/openclaw.json ~/.openclaw/openclaw.json
launchctl kickstart -k gui/$(id -u)/ai.openclaw.gateway
```

---

## 📝 维护者

- **康妃 (config)** - 配置管理与系统稳定性

---

## 📜 更新记录

| 日期 | 版本 | 变更 |
|------|------|------|
| 2026-03-08 | 1.1 | 添加日志轮转机制（5MB 压缩，保留 30 天）|
| 2026-03-07 | 1.0 | 初始版本 |

---

**安装完成后，你的 OpenClaw Gateway 将拥有两层保护，确保 7x24 小时稳定运行。**
