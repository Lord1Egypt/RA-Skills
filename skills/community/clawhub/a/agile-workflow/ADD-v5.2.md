# ADD - 敏捷工作流 v5.2 Agent 熔断恢复架构设计

**日期**: 2026-03-12  
**版本**: v5.2.0  
**状态**: 设计完成 → 实现中

---

## 1. 架构概述

### 1.1 设计目标

1. **熔断检测**：实时检测各种熔断场景
2. **自动恢复**：熔断后自动恢复，无需人工干预
3. **渐进恢复**：从半熔断到完全恢复，避免二次故障
4. **预防机制**：提前预警，防止熔断发生

### 1.2 核心原则

```
正常 → 预警 → 半熔断 → 全熔断 → 冷却 → 探测 → 恢复
              ↓          ↓          ↓         ↓
           降级处理   拒绝请求   等待恢复   测试恢复
```

---

## 2. 系统架构

### 2.1 熔断状态机

```
                    错误率 > 阈值
        ┌─────────────────────────────┐
        │                             │
        ▼                             │
    [正常] ─── 预警 ──→ [半熔断] ────┤
        │                   │         │
        │                   │ 成功    │
        │                   ▼         │
        │               [恢复中] ─────┤
        │                   │
        │                   │ 失败
        │                   ▼
        └────────────── [全熔断]
                            │
                            │ 冷却期结束
                            ▼
                        [探测]
```

### 2.2 状态定义

| 状态 | 说明 | 请求处理 | 持续时间 | 转换条件 |
|------|------|----------|----------|----------|
| **正常** | 无错误 | 全部接受 | - | 错误率 < 阈值 |
| **预警** | 错误增加 | 全部接受 + 降级 | 5 分钟 | 错误率 > 50% 阈值 |
| **半熔断** | 部分错误 | 50% 接受 | 2 分钟 | 错误率 > 阈值 |
| **全熔断** | 严重错误 | 全部拒绝 | 5 分钟 | 连续失败 N 次 |
| **恢复中** | 测试恢复 | 10% 接受 | 1 分钟 | 冷却期结束 |
| **探测** | 验证恢复 | 探测请求 | 30 秒 | 手动/自动触发 |

### 2.3 熔断原因分类

| 原因 | 阈值 | 冷却期 | 恢复策略 |
|------|------|--------|----------|
| **连续失败** | 5 次 | 5 分钟 | 渐进恢复 |
| **执行超时** | 3 次 | 3 分钟 | 重试 + 恢复 |
| **资源耗尽** | 内存>90% | 10 分钟 | 重启 + 恢复 |
| **心跳丢失** | 90 秒 | 5 分钟 | 重启 + 恢复 |
| **依赖不可用** | 3 次 | 5 分钟 | 降级 + 恢复 |

---

## 3. 核心算法

### 3.1 熔断检测算法

```javascript
class CircuitBreaker {
  constructor(agentName, config) {
    this.agentName = agentName;
    this.state = 'NORMAL'; // NORMAL/WARNING/HALF_OPEN/OPEN/RECOVERING
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.lastStateChange = Date.now();
    this.config = {
      failureThreshold: 5,        // 失败阈值
      successThreshold: 3,        // 成功阈值
      timeout: 30000,             // 超时时间
      resetTimeout: 300000,       // 重置超时（5 分钟）
      warningThreshold: 0.5,      // 预警阈值（50%）
      ...config
    };
  }

  // 记录请求结果
  recordResult(success, error = null) {
    const now = Date.now();

    if (success) {
      this.successCount++;
      this.failureCount = 0; // 重置失败计数
      
      // 恢复中状态，成功达到阈值→完全恢复
      if (this.state === 'RECOVERING' && this.successCount >= this.config.successThreshold) {
        this.transitionTo('NORMAL');
      }
    } else {
      this.failureCount++;
      this.lastFailureTime = now;
      
      // 根据状态处理
      this.handleFailure(error);
    }

    this.checkStateTransition();
  }

  // 处理失败
  handleFailure(error) {
    const errorType = this.classifyError(error);

    if (this.state === 'NORMAL') {
      // 正常状态，失败次数超阈值→半熔断
      if (this.failureCount >= this.config.failureThreshold) {
        this.transitionTo('HALF_OPEN');
      }
    } else if (this.state === 'WARNING') {
      // 预警状态，失败次数超阈值→全熔断
      if (this.failureCount >= this.config.failureThreshold * 2) {
        this.transitionTo('OPEN');
      }
    } else if (this.state === 'HALF_OPEN') {
      // 半熔断状态，任何失败→全熔断
      this.transitionTo('OPEN');
    }

    // 记录错误类型
    this.recordErrorType(errorType);
  }

  // 检查状态转换
  checkStateTransition() {
    const now = Date.now();
    const timeInState = now - this.lastStateChange;

    // 全熔断状态，冷却期结束→恢复中
    if (this.state === 'OPEN' && timeInState >= this.config.resetTimeout) {
      this.transitionTo('RECOVERING');
    }

    // 预警状态，5 分钟无新错误→正常
    if (this.state === 'WARNING' && 
        timeInState >= 300000 && 
        !this.lastFailureTime || now - this.lastFailureTime >= 300000) {
      this.transitionTo('NORMAL');
    }
  }

  // 状态转换
  transitionTo(newState) {
    const oldState = this.state;
    this.state = newState;
    this.lastStateChange = Date.now();
    this.successCount = 0;
    
    // 状态转换时的特殊处理
    if (newState === 'OPEN') {
      this.onOpen();
    } else if (newState === 'RECOVERING') {
      this.onRecovering();
    }

    console.log(`📊 [${this.agentName}] 熔断状态：${oldState} → ${newState}`);
    this.logStateChange(oldState, newState);
  }

  // 全熔断时的处理
  onOpen() {
    // 1. 停止分配新任务
    this.stopNewTasks();
    
    // 2. 等待当前任务完成
    this.waitForCurrentTasks();
    
    // 3. 备份状态
    this.backupState();
    
    // 4. 发送告警
    this.sendAlert('CIRCUIT_OPEN');
  }

  // 恢复中时的处理
  onRecovering() {
    // 1. 发送探测请求
    this.sendProbeRequest();
    
    // 2. 准备恢复
    this.prepareRecovery();
    
    // 3. 发送通知
    this.sendNotification('RECOVERING');
  }

  // 错误分类
  classifyError(error) {
    if (!error) return 'UNKNOWN';
    
    if (error.message?.includes('timeout')) return 'TIMEOUT';
    if (error.message?.includes('memory')) return 'RESOURCE';
    if (error.message?.includes('heartbeat')) return 'HEALTH';
    if (error.message?.includes('connection')) return 'DEPENDENCY';
    
    return 'BUSINESS';
  }
}
```

### 3.2 自动恢复算法

```javascript
class AutoRecovery {
  constructor(circuitBreaker) {
    this.cb = circuitBreaker;
    this.recoveryPlan = null;
  }

  // 制定恢复计划
  createRecoveryPlan() {
    const errorStats = this.cb.getErrorStats();
    
    const plan = {
      type: this.determineRecoveryType(errorStats),
      steps: [],
      estimatedTime: 0
    };

    // 根据错误类型制定恢复策略
    if (errorStats dominantType === 'TIMEOUT') {
      plan.steps = [
        { action: 'increase_timeout', duration: 60000 },
        { action: 'retry_with_backoff', duration: 120000 },
        { action: 'gradual_recovery', duration: 300000 }
      ];
      plan.estimatedTime = 480000;
    } else if (errorStats.dominantType === 'RESOURCE') {
      plan.steps = [
        { action: 'cleanup_resources', duration: 30000 },
        { action: 'restart_agent', duration: 60000 },
        { action: 'monitor_resources', duration: 300000 },
        { action: 'gradual_recovery', duration: 300000 }
      ];
      plan.estimatedTime = 690000;
    } else if (errorStats.dominantType === 'HEALTH') {
      plan.steps = [
        { action: 'restart_agent', duration: 60000 },
        { action: 'verify_health', duration: 120000 },
        { action: 'gradual_recovery', duration: 300000 }
      ];
      plan.estimatedTime = 480000;
    }

    return plan;
  }

  // 执行恢复计划
  async executeRecoveryPlan(plan) {
    console.log(`🔄 开始执行恢复计划，预计 ${plan.estimatedTime/1000} 秒`);

    for (const step of plan.steps) {
      console.log(`📍 执行步骤：${step.action}`);
      
      try {
        await this.executeStep(step);
        await this.verifyStepResult(step);
      } catch (error) {
        console.error(`❌ 步骤失败：${step.action}`, error);
        await this.handleStepFailure(step, error);
        return false;
      }
    }

    console.log(`✅ 恢复计划执行完成`);
    return true;
  }

  // 渐进恢复
  async gradualRecovery() {
    const phases = [
      { percentage: 10, duration: 60000 },   // 10% 流量，1 分钟
      { percentage: 30, duration: 120000 },  // 30% 流量，2 分钟
      { percentage: 60, duration: 180000 },  // 60% 流量，3 分钟
      { percentage: 100, duration: 0 }       // 100% 流量
    ];

    for (const phase of phases) {
      console.log(`📈 恢复进度：${phase.percentage}%`);
      
      this.cb.setTrafficPercentage(phase.percentage);
      
      if (phase.duration > 0) {
        await this.monitorPhase(phase);
      }
    }
  }
}
```

### 3.3 预防机制算法

```javascript
class PreventionMechanism {
  // 错误隔离
  isolateError(error, agent) {
    // 1. 识别错误影响范围
    const impactScope = this.assessImpact(error, agent);
    
    // 2. 隔离受影响的任务
    this.quarantineTasks(impactScope.affectedTasks);
    
    // 3. 防止错误扩散
    this.preventSpread(impactScope);
  }

  // 降级策略
  getDegradationStrategy(agent) {
    const strategies = {
      'chapter_writer': {
        level1: 'use_cache',           // 一级降级：使用缓存
        level2: 'simplified_mode',     // 二级降级：简化模式
        level3: 'queue_and_retry'      // 三级降级：排队重试
      },
      'world_builder': {
        level1: 'use_template',
        level2: 'partial_generation',
        level3: 'manual_review'
      }
    };

    return strategies[agent.name] || strategies.default;
  }

  // 预警通知
  sendEarlyWarning(agent, metrics) {
    const warnings = [];

    // 错误率上升
    if (metrics.errorRate > 0.1) {
      warnings.push({
        type: 'ERROR_RATE_INCREASE',
        level: 'WARNING',
        message: `${agent.name} 错误率上升至 ${(metrics.errorRate * 100).toFixed(1)}%`
      });
    }

    // 响应时间增加
    if (metrics.responseTime > metrics.baseline * 2) {
      warnings.push({
        type: 'RESPONSE_TIME_INCREASE',
        level: 'WARNING',
        message: `${agent.name} 响应时间增加 ${(metrics.responseTime / metrics.baseline).toFixed(1)}x`
      });
    }

    // 资源使用率高
    if (metrics.memoryUsage > 0.8) {
      warnings.push({
        type: 'HIGH_MEMORY_USAGE',
        level: 'WARNING',
        message: `${agent.name} 内存使用率 ${(metrics.memoryUsage * 100).toFixed(1)}%`
      });
    }

    // 发送预警
    if (warnings.length > 0) {
      this.sendNotification(warnings);
    }
  }
}
```

---

## 4. 数据结构

### 4.1 熔断器状态

```json
{
  "agentName": "chapter_writer",
  "state": "NORMAL",
  "failureCount": 0,
  "successCount": 10,
  "lastFailureTime": null,
  "lastStateChange": 1710288000000,
  "errorStats": {
    "TIMEOUT": 2,
    "RESOURCE": 0,
    "HEALTH": 0,
    "DEPENDENCY": 1,
    "BUSINESS": 0
  },
  "metrics": {
    "errorRate": 0.02,
    "avgResponseTime": 1500,
    "successRate": 98.5
  }
}
```

### 4.2 恢复计划

```json
{
  "agentName": "chapter_writer",
  "triggerReason": "CONTINUOUS_FAILURE",
  "failureCount": 5,
  "plan": {
    "type": "GRADUAL_RECOVERY",
    "steps": [
      { "action": "cleanup_resources", "status": "pending" },
      { "action": "restart_agent", "status": "pending" },
      { "action": "verify_health", "status": "pending" },
      { "action": "gradual_recovery", "status": "pending" }
    ],
    "estimatedTime": 480000,
    "createdAt": 1710288000000
  }
}
```

---

## 5. 预期效果

| 指标 | v5.1 | v5.2 | 提升 |
|------|------|------|------|
| **熔断恢复时间** | 手动 | 自动 5 分钟 | ⬆️ 效率 |
| **工作中断率** | 30% | < 5% | ⬇️ 83% |
| **人工干预** | 每次 | 罕见 | ⬇️ 95% |
| **错误扩散** | 常见 | 隔离 | ⬆️ 稳定性 |

---

## 6. 实施计划

### Phase 1: 熔断器核心 (已完成)
- [x] 状态机设计
- [x] 检测算法
- [x] 状态转换逻辑

### Phase 2: 自动恢复 (进行中)
- [ ] 恢复计划生成
- [ ] 渐进恢复实现
- [ ] 验证机制

### Phase 3: 预防机制 (待开始)
- [ ] 错误隔离
- [ ] 降级策略
- [ ] 预警通知

---

**ADD 设计完成，准备实施！** 🚀
