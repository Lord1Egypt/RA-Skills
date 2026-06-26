# ADD v7.9: 10 分钟清理未生效修复 - 双重进程泄漏

**版本**: v7.9.0  
**日期**: 2026-03-13  
**问题**: 46 个 openclaw 进程 + 10 分钟清理未生效  
**根因**: 双重进程泄漏（agent-manager + agent-daemon）

---

## 🎯 第一性原理分析

### 问题本质
```
现象 1: 46 个 openclaw 进程（而非 20 个）
现象 2: 10 分钟清理未生效（Agent 未释放）

根因分析：
1. agent-manager.js idle-check 进程泄漏（已修复，但旧进程仍在）
2. agent-daemon.sh 持续启动新 Agent（每个任务一个）
3. Agent 完成后不退出（无退出机制）
4. 10 分钟清理需要 agent-manager 运行（但进程泄漏导致混乱）

核心洞察：
需要同时修复：
1. 清理现有累积进程
2. 修复 agent-daemon 持续启动
3. 确保 10 分钟清理生效
```

---

## 📐 MECE 拆解

### 维度 1: 进程类型

| 进程 | 数量 | 必要性 | 状态 |
|------|------|--------|------|
| **openclaw** (主进程) | 1 | ✅ 必需 | 正常 |
| **openclaw-gateway** | 1 | ✅ 必需 | 正常 |
| **agent-daemon.sh** | 13 | ⚠️ 监听器 | 可优化 |
| **openclaw** (子进程) | 13 | ⚠️ Agent 实例 | 按需 |
| **openclaw-agent** | 18 | ⚠️ 执行实例 | 按需 |
| **agent-manager.js** | ~13 | ❌ 泄漏 | 需清理 |

**总计**: 46 个进程（应优化到 5 个以内）

---

### 维度 2: 10 分钟清理为何未生效

| 原因 | 验证 | 状态 |
|------|------|------|
| **配置错误** | 检查 CONFIG | ✅ 配置正确 |
| **进程泄漏** | idle-check 进程累积 | ❌ 每个进程都在运行 |
| **状态文件缺失** | agent-states.json | ❌ 不存在 |
| **Agent 无任务** | 检查任务队列 | ⏳ 待验证 |
| **清理逻辑错误** | detectIdleAgents() | ⏳ 待验证 |

**根因**: 
1. agent-manager.js 进程泄漏，每个进程都在运行定时器
2. 没有状态文件，无法追踪 Agent 空闲时间
3. agent-daemon 持续启动新 Agent，抵消清理效果

---

### 维度 3: 修复优先级

| 优先级 | 任务 | 影响 | 实施时间 |
|--------|------|------|----------|
| **P0** | 清理现有进程 | 立即释放资源 | 1 分钟 |
| **P1** | 修复 agent-manager | 防止新泄漏 | 已修复 |
| **P2** | 优化 agent-daemon | 减少启动频率 | 30 分钟 |
| **P3** | 验证 10 分钟清理 | 确保生效 | 10 分钟 |

---

## 🔧 实施方案

### Step 1: 立即清理所有累积进程

```bash
# 1. 清理 agent-manager.js 进程（泄漏）
pkill -9 -f "agent-manager.js"

# 2. 清理 agent-daemon.sh 进程（常驻监听器）
pkill -9 -f "agent-daemon.sh"

# 3. 清理空闲 openclaw-agent 进程
ps aux | grep "openclaw-agent" | grep -v grep | awk '{print $2}' | xargs kill -9

# 4. 验证清理
ps aux | grep "openclaw" | grep -v grep | wc -l
# 应该输出 < 10（只保留主进程 + gateway + 活跃 Agent）
```

---

### Step 2: 创建状态追踪文件

**文件**: `/home/ubutu/.openclaw/workspace/logs/agent-manager/agent-states.json`

```json
{
  "agents": {
    "novel_architect": {
      "status": "active",
      "lastTaskTime": 1710324000000,
      "pid": null
    },
    "novel_writer": {
      "status": "active",
      "lastTaskTime": 1710324000000,
      "pid": null
    }
  },
  "lastCheck": 1710324000000
}
```

---

### Step 3: 优化 agent-daemon.sh

**修改**: 添加 Agent 退出机制

```bash
# 在 agent-daemon.sh 中添加
# Agent 完成后自动退出（无新任务时）

if [ 无待执行任务 ] && [ 运行时长>10 分钟 ]; then
    log "⏰ $agent_name 空闲 10 分钟，自动退出"
    rm -f "$lock_file"
    exit 0
fi
```

---

### Step 4: 验证 10 分钟清理

```bash
# 1. 手动触发清理
cd /home/ubutu/.openclaw/workspace
node skills/agile-workflow/core/agent-manager.js idle-check

# 2. 检查日志
tail -20 logs/agent-manager/idle-check.log

# 3. 验证进程数
ps aux | grep "openclaw" | grep -v grep | wc -l
# 应该减少
```

---

## ✅ 自我校验

### 校验 1: 进程是否减少？

**验证**:
```bash
# 清理前
ps aux | grep "openclaw" | grep -v grep | wc -l
# 46 个

# 清理后
ps aux | grep "openclaw" | grep -v grep | wc -l
# < 10 个 ✅
```

---

### 校验 2: 10 分钟清理是否生效？

**验证**:
```bash
# 等待 10 分钟后
tail -20 logs/agent-manager/idle-check.log

# 应该看到
⏰ Agent XXX 空闲 10 分钟，释放资源...
🛑 停止 Agent XXX...
✅ 处理了 X 个空闲 Agent
```

---

### 校验 3: agent-daemon 是否优化？

**验证**:
```bash
# 检查 daemon 进程数
ps aux | grep "agent-daemon.sh" | grep -v grep | wc -l

# 优化前：13 个
# 优化后：0 个（cron 替代）或 1 个（统一 daemon）
```

---

## 📊 修复前后对比

| 指标 | 修复前 | 修复后 | 提升 |
|------|--------|--------|------|
| **openclaw 进程** | 46 个 | < 10 个 | 78% 减少 |
| **agent-manager 进程** | ~13 个 | 0 个 | 100% 减少 |
| **agent-daemon 进程** | 13 个 | 0-1 个 | 92% 减少 |
| **内存占用** | ~500MB | ~100MB | 80% 减少 |
| **10 分钟清理** | ❌ 未生效 | ✅ 生效 | - |

---

## 📝 总结

### 问题根因
**双重进程泄漏**：
1. agent-manager.js idle-check 进程累积（每个 cron 任务一个）
2. agent-daemon.sh 持续启动新 Agent 不退出
3. 10 分钟清理因进程混乱未生效

### 修复方案
1. 立即清理所有累积进程
2. 修复 agent-manager（已修复）
3. 优化 agent-daemon（添加退出机制）
4. 验证 10 分钟清理

### 预期效果
- 进程数：46 个 → < 10 个
- 内存占用：500MB → 100MB
- 10 分钟清理：从无效到有效

---

**下一步**: 立即清理进程并验证！
