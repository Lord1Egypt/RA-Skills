# ADD v7.1: Agent 一小时无任务自动释放功能修复

**版本**: v7.1.0  
**日期**: 2026-03-13  
**问题**: 昨天完成的多 Agent 一小时无任务自动释放功能未生效

---

## 🎯 问题定义

### 用户问题
> 查一下昨天完成的多 Agent 一小时无任务自动释放的功能为何没有生效

### 第一性原理分析

```
第一原理 1: 功能生效的必要条件
├── 条件 1: 代码存在 ✅ (agent-manager.js 已实现)
├── 条件 2: 进程运行 ❌ (Agent Manager 未启动)
├── 条件 3: 定时调用 ❌ (无 cron 任务调用 idle-check)
└── 条件 4: 状态持久化 ❌ (agent-states.json 不存在)

第一原理 2: 空闲检测的工作原理
├── 前提：Agent 状态被追踪
├── 触发：定时器每分钟检测
├── 判断：当前时间 - lastTaskTime >= 阈值
└── 动作：stopAgent() 或 sleepAgent()

第一原理 3: 为何未生效
├── 代码已实现 ✅
├── 但从未被运行 ❌
└── 没有进程在调用 detectIdleAgents() ❌

核心洞察：
功能未生效不是因为代码错误，而是因为没有被部署和运行！
```

---

## 📐 MECE 拆解

### 维度 1: 功能未生效的根因

| 根因 | 验证方法 | 状态 | 解决方案 |
|------|----------|------|----------|
| 代码不存在 | 检查文件 | ❌ 已存在 | - |
| 进程未启动 | ps aux 检查 | ❌ 未运行 | 启动守护进程 |
| 无定时调用 | crontab 检查 | ❌ 无 cron | 添加 cron 任务 |
| 状态文件不存在 | 检查文件 | ❌ 不存在 | 首次运行自动创建 |
| 配置错误 | 检查 CONFIG | ✅ 配置正确 | - |

### 维度 2: 需要修复的组件

| 组件 | 当前状态 | 目标状态 | 修复方式 |
|------|----------|----------|----------|
| **agent-manager.js** | 存在但未运行 | 后台持续运行 | 创建守护进程脚本 |
| **cron 任务** | 无相关调用 | 每分钟调用 idle-check | 添加 cron 任务 |
| **状态文件** | 不存在 | 自动创建并持久化 | 首次运行创建 |
| **日志记录** | 无 | 记录状态变化和空闲检测 | 完善日志 |

### 维度 3: 验证步骤

| 步骤 | 验证内容 | 预期结果 |
|------|----------|----------|
| 1. 启动 Agent Manager | 进程存在 | ps aux 可见 |
| 2. 检查状态文件 | 文件创建 | agent-states.json 存在 |
| 3. 手动触发 idle-check | 功能正常 | 无报错 |
| 4. 添加 cron 任务 | 定时调用 | crontab -l 可见 |
| 5. 等待 1 小时 | 自动释放 | 日志显示释放记录 |

---

## 🏗️ 修复方案

### 方案 1: 创建守护进程脚本

**文件**: `/home/ubutu/.openclaw/workspace/scripts/agent-manager-daemon.sh`

```bash
#!/bin/bash
# Agent Manager 守护进程
# 功能：后台持续运行 Agent Manager，监控空闲 Agent

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/ubutu/.openclaw/workspace"
LOG_DIR="$WORKSPACE/logs/agent-manager"
PID_FILE="$LOG_DIR/agent-manager.pid"
LOG_FILE="$LOG_DIR/daemon.log"

# 确保日志目录存在
mkdir -p "$LOG_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

start() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            log "⚠️ Agent Manager 已在运行 (PID: $PID)"
            return 0
        fi
    fi

    log "🚀 启动 Agent Manager 守护进程..."
    
    # 后台运行 agent-manager.js
    cd "$WORKSPACE"
    nohup node skills/agile-workflow/core/agent-manager.js > "$LOG_DIR/agent-manager.log" 2>&1 &
    
    echo $! > "$PID_FILE"
    log "✅ Agent Manager 已启动 (PID: $(cat $PID_FILE))"
    
    # 等待启动完成
    sleep 2
    
    if ps -p $(cat "$PID_FILE") > /dev/null 2>&1; then
        log "✅ Agent Manager 启动成功"
        return 0
    else
        log "❌ Agent Manager 启动失败"
        rm -f "$PID_FILE"
        return 1
    fi
}

stop() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            log "🛑 停止 Agent Manager (PID: $PID)..."
            kill $PID
            sleep 2
            
            # 如果还在运行，强制停止
            if ps -p $PID > /dev/null 2>&1; then
                kill -9 $PID
            fi
            
            log "✅ Agent Manager 已停止"
        else
            log "⚠️ Agent Manager 未运行"
        fi
        rm -f "$PID_FILE"
    else
        log "⚠️ PID 文件不存在"
    fi
}

status() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p $PID > /dev/null 2>&1; then
            echo "✅ Agent Manager 正在运行 (PID: $PID)"
            return 0
        else
            echo "⚠️ Agent Manager 未运行 (PID 文件存在但进程不存在)"
            return 1
        fi
    else
        echo "❌ Agent Manager 未运行"
        return 1
    fi
}

restart() {
    stop
    sleep 1
    start
}

# 主程序
case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    status)
        status
        ;;
    *)
        echo "用法：$0 {start|stop|restart|status}"
        exit 1
        ;;
esac

exit 0
```

---

### 方案 2: 添加 cron 定时任务

**cron 配置**: 每分钟调用 idle-check

```bash
# 添加到 crontab
*/1 * * * * cd /home/ubutu/.openclaw/workspace && node skills/agile-workflow/core/agent-manager.js idle-check >> logs/agent-manager/idle-check.log 2>&1
```

---

### 方案 3: 完善日志记录

**日志文件**: `/home/ubutu/.openclaw/workspace/logs/agent-manager/idle-detection.log`

记录内容：
- 每次 idle-check 的时间
- 检测到的空闲 Agent
- 执行的动作（休眠/释放）
- 执行结果

---

## 🔧 实施步骤

### Step 1: 创建守护进程脚本

```bash
cat > /home/ubutu/.openclaw/workspace/scripts/agent-manager-daemon.sh << 'EOF'
[脚本内容见上方]
EOF

chmod +x /home/ubutu/.openclaw/workspace/scripts/agent-manager-daemon.sh
```

### Step 2: 启动 Agent Manager

```bash
/home/ubutu/.openclaw/workspace/scripts/agent-manager-daemon.sh start
```

### Step 3: 验证状态

```bash
# 检查进程
ps aux | grep agent-manager

# 检查状态文件
cat /home/ubutu/.openclaw/workspace/logs/agent-manager/agent-states.json

# 查看日志
tail -20 /home/ubutu/.openclaw/workspace/logs/agent-manager/daemon.log
```

### Step 4: 添加 cron 任务

```bash
(crontab -l 2>/dev/null; echo "*/1 * * * * cd /home/ubutu/.openclaw/workspace && node skills/agile-workflow/core/agent-manager.js idle-check >> logs/agent-manager/idle-check.log 2>&1") | crontab -
```

### Step 5: 测试 idle-check

```bash
cd /home/ubutu/.openclaw/workspace
node skills/agile-workflow/core/agent-manager.js idle-check
```

### Step 6: 验证 cron

```bash
crontab -l | grep agent-manager
```

---

## ✅ 自我校验

### 校验 1: 进程是否运行？
```bash
ps aux | grep agent-manager
# 预期：看到 node agent-manager.js 进程
```

### 校验 2: 状态文件是否存在？
```bash
ls -la /home/ubutu/.openclaw/workspace/logs/agent-manager/agent-states.json
# 预期：文件存在且有内容
```

### 校验 3: cron 是否配置？
```bash
crontab -l | grep agent-manager
# 预期：看到 idle-check 的 cron 任务
```

### 校验 4: 日志是否记录？
```bash
tail -20 /home/ubutu/.openclaw/workspace/logs/agent-manager/idle-check.log
# 预期：看到 idle-check 执行记录
```

### 校验 5: 功能是否生效？
等待 1 小时后检查：
```bash
tail -50 /home/ubutu/.openclaw/workspace/logs/agent-manager/daemon.log
# 预期：看到 "空闲 1 小时，释放资源" 或 "空闲 30 分钟，进入休眠" 的日志
```

---

## 📊 预期效果

### 修复前
```
❌ Agent Manager 未运行
❌ 无状态追踪
❌ 无空闲检测
❌ Agent 永不释放
```

### 修复后
```
✅ Agent Manager 后台运行
✅ 状态实时追踪
✅ 每分钟检测空闲
✅ 30 分钟空闲→休眠
✅ 1 小时空闲→释放
```

---

## 🎯 成功标准

| 标准 | 验证方法 | 目标 |
|------|----------|------|
| 进程运行 | ps aux | ✅ 看到进程 |
| 状态文件 | ls -la | ✅ 文件存在 |
| cron 配置 | crontab -l | ✅ 有 idle-check 任务 |
| 日志记录 | tail log | ✅ 有检测记录 |
| 自动释放 | 等待 1 小时 | ✅ 看到释放日志 |

---

## 📝 总结

### 根因
**功能未生效不是因为代码错误，而是因为没有被部署和运行！**

### 修复方案
1. 创建守护进程脚本
2. 启动 Agent Manager
3. 添加 cron 定时任务
4. 验证日志和状态

### 预期结果
- ✅ Agent 空闲 30 分钟自动休眠
- ✅ Agent 空闲 1 小时自动释放
- ✅ 资源利用率提升
- ✅ 无需手动管理

---

**下一步**: 立即执行修复步骤并验证！
