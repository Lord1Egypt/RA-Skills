# ADD - 敏捷工作流 v5.1 Agent 动态伸缩架构设计

**日期**: 2026-03-12  
**版本**: v5.1.0  
**状态**: 设计完成 → 实现中

---

## 1. 架构概述

### 1.1 设计目标

1. **资源优化**：从"所有 Agent 常驻"改为"按需常驻"
2. **智能伸缩**：有任务→启动，1 小时无任务→释放
3. **状态管理**：活跃/空闲/休眠/离线四状态
4. **健康监控**：实时检测，自动恢复

### 1.2 核心原则

```
任务分配 → 检查状态 → 离线？→ 启动 → 验证 → 分配
             ↓          ↓
           活跃/空闲 → 直接分配

空闲检测 → 1 小时无任务 → 备份状态 → 优雅关闭 → 释放资源
```

---

## 2. 系统架构

### 2.1 Agent 状态机

```
                    分配任务
        ┌─────────────────────────┐
        │                         │
        ▼                         │
    [离线] ───启动───→ [空闲] ────┤
        │              │          │
        │              │ 分配任务  │
        │              ▼          │
        │          [活跃] ←───────┘
        │              │
        │              │ 任务完成
        │              ▼
        └────────── [空闲]
                       │
                       │ 1 小时无任务
                       ▼
                   [离线]
```

### 2.2 状态定义

| 状态 | 说明 | 资源占用 | 启动时间 | 转换条件 |
|------|------|----------|----------|----------|
| **活跃** | 正在执行任务 | 100% | - | 分配任务 |
| **空闲** | 已启动无任务 | 30% | - | 任务完成 |
| **休眠** | 暂停可快速恢复 | 10% | 5 秒 | 30 分钟空闲 |
| **离线** | 已释放 | 0% | 30 秒 | 1 小时空闲 |

### 2.3 核心组件

```
┌─────────────────────────────────────────────────────────┐
│              Agent 状态管理器 (State Manager)             │
│  - 状态追踪（活跃/空闲/休眠/离线）                        │
│  - 最后任务时间                                          │
│  - 资源占用统计                                          │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              任务分配器 (Task Dispatcher)                │
│  - 状态检查                                              │
│  - 智能启动（离线→启动）                                 │
│  - 健康验证                                              │
│  - 任务分配                                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              空闲检测器 (Idle Detector)                  │
│  - 30 分钟空闲→休眠                                         │
│  - 1 小时空闲→释放                                          │
│  - 优雅关闭                                              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              健康监控器 (Health Monitor)                 │
│  - 心跳检测（30 秒）                                        │
│  - 日志监控（实时）                                      │
│  - 进程监控（实时）                                      │
│  - 自动恢复（失败重启）                                  │
└─────────────────────────────────────────────────────────┘
```

---

## 3. 核心算法

### 3.1 任务分配算法

```javascript
async function assignTask(task, agentName) {
  // 1. 检查 Agent 状态
  const agent = await getAgentState(agentName);
  
  // 2. 根据状态处理
  if (agent.status === 'offline') {
    // 离线→启动
    console.log(`Agent ${agentName} 离线，启动中...`);
    await startAgent(agentName);
    
    // 验证启动成功
    const healthy = await verifyAgentHealth(agentName);
    if (!healthy) {
      throw new Error(`Agent ${agentName} 启动失败`);
    }
  } else if (agent.status === 'sleeping') {
    // 休眠→唤醒
    console.log(`Agent ${agentName} 休眠中，唤醒中...`);
    await wakeupAgent(agentName);
  }
  
  // 3. 分配任务
  await dispatchTask(agentName, task);
  
  // 4. 更新状态
  await updateAgentState(agentName, {
    status: 'active',
    currentTask: task.id,
    lastTaskTime: Date.now()
  });
}
```

### 3.2 空闲检测算法

```javascript
async function detectIdleAgents() {
  const now = Date.now();
  const IDLE_TO_SLEEP = 30 * 60 * 1000;  // 30 分钟
  const IDLE_TO_OFFLINE = 60 * 60 * 1000; // 1 小时
  
  for (const agent of allAgents) {
    if (agent.status !== 'idle') continue;
    
    const idleTime = now - agent.lastTaskTime;
    
    if (idleTime >= IDLE_TO_OFFLINE) {
      // 1 小时空闲→释放
      console.log(`Agent ${agent.name} 空闲 1 小时，释放资源...`);
      await backupAgentState(agent.name);
      await stopAgent(agent.name);
      await updateAgentState(agent.name, { status: 'offline' });
    } else if (idleTime >= IDLE_TO_SLEEP) {
      // 30 分钟空闲→休眠
      console.log(`Agent ${agent.name} 空闲 30 分钟，进入休眠...`);
      await sleepAgent(agent.name);
      await updateAgentState(agent.name, { status: 'sleeping' });
    }
  }
}
```

### 3.3 健康监控算法

```javascript
async function monitorAgentHealth(agentName) {
  // 1. 心跳检测
  const heartbeat = await checkHeartbeat(agentName);
  if (!heartbeat) {
    console.warn(`Agent ${agentName} 心跳丢失`);
    await recoverAgent(agentName);
    return;
  }
  
  // 2. 日志监控
  const errors = await checkAgentLogs(agentName);
  if (errors.length > 0) {
    console.warn(`Agent ${agentName} 检测到 ${errors.length} 个错误`);
    await handleAgentErrors(agentName, errors);
  }
  
  // 3. 进程监控
  const processInfo = await checkAgentProcess(agentName);
  if (!processInfo.running) {
    console.error(`Agent ${agentName} 进程异常退出`);
    await restartAgent(agentName);
  }
}
```

---

## 4. 数据结构

### 4.1 Agent 状态结构

```json
{
  "name": "chapter_writer",
  "status": "active",
  "pid": 12345,
  "port": 3001,
  "currentTask": "task_001",
  "lastTaskTime": 1710288000000,
  "startedAt": 1710284400000,
  "idleTime": 0,
  "health": {
    "heartbeat": 1710288000000,
    "memory": 256,
    "cpu": 15,
    "errors": 0
  },
  "stats": {
    "totalTasks": 150,
    "successRate": 98.5,
    "avgDuration": 180000
  }
}
```

### 4.2 资源配置

```json
{
  "agents": {
    "chapter_writer": {
      "command": "node agents/chapter-writer.js",
      "port": 3001,
      "autoStart": false,
      "idleTimeout": 3600000,
      "sleepTimeout": 1800000,
      "minInstances": 0,
      "maxInstances": 3
    },
    "world_builder": {
      "command": "node agents/world-builder.js",
      "port": 3002,
      "autoStart": false,
      "idleTimeout": 3600000,
      "sleepTimeout": 1800000,
      "minInstances": 0,
      "maxInstances": 2
    }
  }
}
```

---

## 5. 资源优化效果

### 5.1 对比分析

| 指标 | v5.0 (全常驻) | v5.1 (动态) | 优化 |
|------|-------------|-----------|------|
| **常驻进程** | 20 个 | 0-5 个 | 75% ↓ |
| **内存占用** | 4GB | 0.5-1GB | 75% ↓ |
| **CPU 占用** | 15% | 2-5% | 70% ↓ |
| **启动延迟** | 0 秒 | 30 秒 | - |
| **响应时间** | 即时 | 即时/30 秒 | - |

### 5.2 成本节省

```
按 20 个 Agent 计算：
- 内存：4GB → 1GB (节省 3GB)
- CPU: 15% → 3% (节省 12%)
- 电费：约 50 元/月 → 15 元/月 (节省 70%)
```

---

## 6. 实施计划

### Phase 1: 状态管理 (已完成)
- [x] Agent 状态定义
- [x] 状态存储结构
- [x] 状态转换逻辑

### Phase 2: 任务分配 (进行中)
- [ ] 状态检查接口
- [ ] 智能启动逻辑
- [ ] 健康验证

### Phase 3: 空闲检测 (待开始)
- [ ] 空闲计时器
- [ ] 休眠逻辑
- [ ] 释放逻辑

### Phase 4: 健康监控 (待开始)
- [ ] 心跳检测
- [ ] 日志监控
- [ ] 自动恢复

---

## 7. 风险评估

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| 启动延迟 | 高 | 中 | 预热常用 Agent |
| 状态丢失 | 低 | 高 | 实时备份 |
| 频繁启停 | 中 | 中 | 设置最小空闲时间 |
| 健康误判 | 低 | 中 | 多重检测机制 |

---

**ADD 设计完成，准备实施！** 🚀
