# ADD v7.5: Agent 进程泄漏修复 - 每分钟 idle-check 导致进程累积

**版本**: v7.5.0  
**日期**: 2026-03-13  
**问题**: 128 个 agent-manager.js 进程累积，cron 每分钟启动新进程不退出  
**根因**: `startMonitoring()` 在 CLI 模式下自动启动定时器，导致进程无法退出

---

## 🎯 第一性原理分析

### 问题本质
```
现象：128 个 agent-manager.js idle-check 进程累积

根因分析：
1. cron 每分钟执行：node agent-manager.js idle-check
2. agent-manager.js 启动时自动调用 startMonitoring()
3. startMonitoring() 启动 setInterval 定时器
4. 进程无法退出（定时器保持进程活跃）
5. 新 cron 任务启动新进程，旧进程仍在运行
6. 进程累积：1 个/分钟 × 128 分钟 = 128 个进程

核心洞察：
CLI 工具应该执行完任务后立即退出，不应该启动常驻定时器。
定时器应该只在守护进程模式下启动。
```

### 代码分析

**问题代码**:
```javascript
class AgentStateManager {
  constructor() {
    this.states = this.loadStates();
    this.ensureDirs();
    this.startMonitoring();  // ❌ 问题：每次都启动定时器
  }

  startMonitoring() {
    // 每分钟检测一次空闲 Agent
    setInterval(() => {
      this.detectIdleAgents();
    }, 60000);  // ❌ 定时器保持进程活跃

    // 每 30 秒检查一次心跳
    setInterval(() => {
      this.checkHeartbeats();
    }, CONFIG.heartbeatInterval);

    console.log('✅ Agent 监控已启动');
  }
}

// CLI 入口
if (require.main === module) {
  main().catch(console.error);
}

async function main() {
  const manager = new AgentStateManager();  // ❌ 启动定时器
  
  switch (command) {
    case 'idle-check':
      await manager.detectIdleAgents();  // 执行检测
      break;  // ❌ 但定时器仍在运行，进程不退出
  }
}
```

**正确设计**:
```javascript
class AgentStateManager {
  constructor(config = {}) {
    this.states = this.loadStates();
    this.ensureDirs();
    
    // ✅ 只在守护进程模式下启动定时器
    if (config.daemonMode) {
      this.startMonitoring();
    }
  }
}

// CLI 模式：执行完任务立即退出
async function main() {
  const manager = new AgentStateManager({ daemonMode: false });  // ✅ 不启动定时器
  
  switch (command) {
    case 'idle-check':
      await manager.detectIdleAgents();
      process.exit(0);  // ✅ 明确退出
      break;
  }
}
```

---

## 📐 MECE 拆解

### 维度 1: 进程累积原因

| 原因 | 验证方法 | 状态 | 解决方案 |
|------|----------|------|----------|
| cron 频繁启动 | crontab -l | ✅ 每分钟 | 保持 |
| 进程不退出 | ps aux 检查 | ✅ 128 个累积 | 修复代码 |
| 定时器活跃 | 代码审查 | ✅ setInterval | 条件启动 |
| 无退出机制 | 代码审查 | ✅ 无 process.exit | 添加退出 |

### 维度 2: 运行模式

| 模式 | 用途 | 是否需要定时器 | 当前状态 |
|------|------|----------------|----------|
| **CLI 模式** | 单次任务（idle-check） | ❌ 不需要 | ❌ 错误启动 |
| **守护进程模式** | 持续监控 | ✅ 需要 | ⏳ 未实现 |

### 维度 3: 修复方案

| 方案 | 复杂度 | 效果 | 实施时间 |
|------|--------|------|----------|
| **方案 1**: 添加 daemonMode 参数 | 低 | ✅ 完全解决 | 30 分钟 |
| **方案 2**: 移除 startMonitoring() | 低 | ✅ 解决但失去监控 | 15 分钟 |
| **方案 3**: 创建独立守护进程 | 中 | ✅ 最佳实践 | 1 小时 |

---

## 🏗️ 修复方案

### 方案 1: 添加 daemonMode 参数（推荐）

**修改点**:
1. 构造函数添加 daemonMode 参数
2. 条件启动定时器
3. CLI 模式添加 process.exit()

**优势**:
- ✅ 简单直接
- ✅ 向后兼容
- ✅ 保留守护进程功能

---

## 🔧 实施步骤

### Step 1: 修复 agent-manager.js

**文件**: `/home/ubutu/.openclaw/workspace/skills/agile-workflow/core/agent-manager.js`

**修改内容**:
1. 构造函数添加 `daemonMode` 参数
2. 条件启动 `startMonitoring()`
3. CLI 模式添加 `process.exit(0)`

### Step 2: 清理累积进程

```bash
# 清理所有 idle-check 进程
ps aux | grep "agent-manager.js idle-check" | grep -v grep | awk '{print $2}' | xargs kill -9

# 验证清理
ps aux | grep "agent-manager.js idle-check" | grep -v grep | wc -l
# 应该输出 0
```

### Step 3: 验证修复

```bash
# 手动执行 idle-check
cd /home/ubutu/.openclaw/workspace
node skills/agile-workflow/core/agent-manager.js idle-check

# 检查进程是否退出
ps aux | grep "agent-manager.js idle-check" | grep -v grep | wc -l
# 应该输出 0（进程已退出）
```

---

## ✅ 自我校验

### 校验 1: 进程是否正确退出？

**验证步骤**:
1. 执行 idle-check
2. 检查进程数
3. 确认进程退出

**预期**: 进程数从 1→0

---

### 校验 2: 功能是否正常？

**验证步骤**:
1. 检查 idle-check.log
2. 确认检测到空闲 Agent
3. 确认执行无错误

**预期**: 日志正常，无错误

---

### 校验 3: 10 分钟清理是否生效？

**验证步骤**:
1. 检查 agent-manager.js 配置
2. 确认 idleToOffline 设置
3. 手动测试清理功能

**预期**: 10 分钟空闲 Agent 自动释放

---

## 📊 10 分钟清理配置验证

### 当前配置

```javascript
const CONFIG = {
  // 超时配置
  idleToSleep: 5 * 60 * 1000,       // 5 分钟空闲→休眠
  idleToOffline: 10 * 60 * 1000,    // 10 分钟空闲→释放 ✅
  heartbeatInterval: 30000,
  startupTimeout: 30000
};
```

**验证**: ✅ 配置正确（10 分钟释放）

### 为何未生效？

**原因**:
1. ❌ 进程累积，每个进程都在运行
2. ❌ 可能没有 Agent 处于 idle 状态
3. ⏳ 需要等待 10 分钟验证

**解决**:
1. ✅ 修复进程泄漏
2. ⏳ 等待 10 分钟验证清理功能

---

## 📝 总结

### 问题根因
**agent-manager.js 在 CLI 模式下启动了常驻定时器，导致进程无法退出，cron 每分钟启动新进程导致累积**

### 修复方案
1. 添加 daemonMode 参数，条件启动定时器
2. CLI 模式添加 process.exit(0)
3. 清理现有累积进程

### 10 分钟清理
- ✅ 配置正确（idleToOffline: 10 分钟）
- ⏳ 需要修复进程泄漏后验证
- ⏳ 需要等待 Agent 空闲 10 分钟

---

**下一步**: 立即修复代码并清理进程！
