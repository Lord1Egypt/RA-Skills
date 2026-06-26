#!/usr/bin/env node
/**
 * Agent 熔断恢复管理器 v5.2
 * 
 * 核心功能:
 * 1. 熔断检测（错误/超时/资源/健康）
 * 2. 自动恢复（冷却→探测→渐进恢复）
 * 3. 预防机制（隔离/降级/预警）
 */

const fs = require('fs');
const path = require('path');

// ============ 配置 ============

const CONFIG = {
  workspace: '/home/ubutu/.openclaw/workspace',
  logsDir: '/home/ubutu/.openclaw/workspace/logs/circuit-breaker',
  stateFile: '/home/ubutu/.openclaw/workspace/logs/circuit-breaker/breaker-states.json',
  
  // 熔断阈值
  failureThreshold: 5,          // 连续失败 5 次→熔断
  successThreshold: 3,          // 连续成功 3 次→恢复
  warningThreshold: 0.5,        // 错误率 50%→预警
  
  // 超时配置
  timeout: 30000,               // 任务超时 30 秒
  resetTimeout: 300000,         // 熔断重置 5 分钟
  recoveryTimeout: 600000,      // 完全恢复 10 分钟
  
  // 资源阈值
  memoryThreshold: 0.9,         // 内存 90%→预警
  cpuThreshold: 0.95,           // CPU 95%→预警
  
  // 恢复策略
  gradualRecovery: true,        // 启用渐进恢复
  autoRetry: true,              // 启用自动重试
  maxRetries: 3                 // 最大重试 3 次
};

// ============ 熔断器类 ============

class CircuitBreaker {
  constructor(agentName, options = {}) {
    this.agentName = agentName;
    this.state = 'NORMAL'; // NORMAL/WARNING/HALF_OPEN/OPEN/RECOVERING
    this.failureCount = 0;
    this.successCount = 0;
    this.lastFailureTime = null;
    this.lastStateChange = Date.now();
    this.errorStats = {
      TIMEOUT: 0,
      RESOURCE: 0,
      HEALTH: 0,
      DEPENDENCY: 0,
      BUSINESS: 0,
      UNKNOWN: 0
    };
    this.metrics = {
      totalRequests: 0,
      totalFailures: 0,
      errorRate: 0,
      avgResponseTime: 0,
      successRate: 100
    };
    this.config = {
      ...CONFIG,
      ...options
    };
    
    console.log(`🔌 [${this.agentName}] 熔断器初始化完成`);
  }

  // ============ 请求处理 ============

  /**
   * 记录请求结果
   */
  recordResult(success, error = null, responseTime = 0) {
    const now = Date.now();
    this.metrics.totalRequests++;

    if (success) {
      this.handleSuccess(responseTime);
    } else {
      this.handleFailure(error, responseTime);
    }

    this.updateMetrics();
    this.checkStateTransition();
    this.saveState();
  }

  /**
   * 处理成功
   */
  handleSuccess(responseTime) {
    this.successCount++;
    this.failureCount = 0; // 重置失败计数
    
    // 更新响应时间（移动平均）
    this.metrics.avgResponseTime = 
      (this.metrics.avgResponseTime * 0.9) + (responseTime * 0.1);

    // 恢复中状态，成功达到阈值→完全恢复
    if (this.state === 'RECOVERING' && this.successCount >= this.config.successThreshold) {
      this.transitionTo('NORMAL');
      console.log(`✅ [${this.agentName}] 恢复成功，回到正常状态`);
    }

    // 半熔断状态，成功→增加流量
    if (this.state === 'HALF_OPEN') {
      this.increaseTraffic();
    }
  }

  /**
   * 处理失败
   */
  handleFailure(error, responseTime) {
    this.failureCount++;
    this.lastFailureTime = Date.now();
    this.metrics.totalFailures++;

    // 错误分类
    const errorType = this.classifyError(error);
    this.errorStats[errorType]++;

    console.warn(`❌ [${this.agentName}] 失败 (${errorType}): ${error?.message || 'Unknown'}`);

    // 根据状态处理
    if (this.state === 'NORMAL') {
      // 正常状态，失败次数超阈值→半熔断
      if (this.failureCount >= this.config.failureThreshold) {
        this.transitionTo('HALF_OPEN');
      } else if (this.failureCount >= this.config.failureThreshold * 0.6) {
        // 达到 60% 阈值→预警
        this.transitionTo('WARNING');
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

    // 触发自动恢复流程
    if (this.state === 'OPEN') {
      this.triggerAutoRecovery();
    }
  }

  /**
   * 错误分类
   */
  classifyError(error) {
    if (!error) return 'UNKNOWN';
    
    const message = error.message || String(error);
    
    if (message.includes('timeout') || message.includes('超时')) return 'TIMEOUT';
    if (message.includes('memory') || message.includes('内存')) return 'RESOURCE';
    if (message.includes('heartbeat') || message.includes('心跳')) return 'HEALTH';
    if (message.includes('connection') || message.includes('connect')) return 'DEPENDENCY';
    if (message.includes('circuit') || message.includes('熔断')) return 'CIRCUIT';
    
    return 'BUSINESS';
  }

  // ============ 状态管理 ============

  /**
   * 状态转换
   */
  transitionTo(newState) {
    const oldState = this.state;
    if (oldState === newState) return;

    this.state = newState;
    this.lastStateChange = Date.now();
    this.successCount = 0;

    console.log(`📊 [${this.agentName}] 熔断状态：${oldState} → ${newState}`);

    // 状态转换时的特殊处理
    if (newState === 'OPEN') {
      this.onOpen();
    } else if (newState === 'RECOVERING') {
      this.onRecovering();
    } else if (newState === 'NORMAL') {
      this.onNormal();
    }

    this.logStateChange(oldState, newState);
  }

  /**
   * 检查状态转换
   */
  checkStateTransition() {
    const now = Date.now();
    const timeInState = now - this.lastStateChange;

    // 全熔断状态，冷却期结束→恢复中
    if (this.state === 'OPEN' && timeInState >= this.config.resetTimeout) {
      this.transitionTo('RECOVERING');
    }

    // 预警状态，5 分钟无新错误→正常
    if (this.state === 'WARNING' && timeInState >= 300000) {
      if (!this.lastFailureTime || (now - this.lastFailureTime) >= 300000) {
        this.transitionTo('NORMAL');
      }
    }

    // 半熔断状态，超时未恢复→全熔断
    if (this.state === 'HALF_OPEN' && timeInState >= 120000) {
      this.transitionTo('OPEN');
    }
  }

  /**
   * 全熔断时的处理
   */
  onOpen() {
    console.log(`🚨 [${this.agentName}] 熔断器打开，停止分配新任务`);
    
    // 1. 发送告警
    this.sendAlert('CIRCUIT_OPEN', {
      failureCount: this.failureCount,
      errorStats: this.errorStats
    });

    // 2. 备份状态
    this.backupState();

    // 3. 等待当前任务完成（不立即停止）
    this.waitForCurrentTasks();
  }

  /**
   * 恢复中时的处理
   */
  onRecovering() {
    console.log(`🔄 [${this.agentName}] 开始恢复流程`);
    
    // 1. 发送探测请求
    this.sendProbeRequest();

    // 2. 准备渐进恢复
    this.trafficPercentage = 10; // 从 10% 流量开始

    // 3. 发送通知
    this.sendNotification('RECOVERING', {
      estimatedTime: this.config.recoveryTimeout / 1000
    });
  }

  /**
   * 恢复正常时的处理
   */
  onNormal() {
    console.log(`✅ [${this.agentName}] 完全恢复正常`);
    
    // 重置统计
    this.failureCount = 0;
    this.errorStats = Object.keys(this.errorStats).reduce((acc, key) => {
      acc[key] = 0;
      return acc;
    }, {});

    // 发送通知
    this.sendNotification('NORMAL');
  }

  // ============ 自动恢复 ============

  /**
   * 触发自动恢复
   */
  async triggerAutoRecovery() {
    console.log(`🔄 [${this.agentName}] 触发自动恢复流程`);

    // 制定恢复计划
    const plan = this.createRecoveryPlan();
    console.log(`📋 恢复计划：${plan.type}, 预计 ${plan.estimatedTime/1000} 秒`);

    // 执行恢复步骤
    for (const step of plan.steps) {
      console.log(`📍 执行步骤：${step.action}`);
      try {
        await this.executeStep(step);
        await this.verifyStepResult(step);
      } catch (error) {
        console.error(`❌ 步骤失败：${step.action}`, error);
        await this.handleStepFailure(step, error);
        return;
      }
    }

    console.log(`✅ [${this.agentName}] 自动恢复流程完成`);
  }

  /**
   * 创建恢复计划
   */
  createRecoveryPlan() {
    const dominantError = this.getDominantErrorType();
    
    const plans = {
      'TIMEOUT': {
        type: 'TIMEOUT_RECOVERY',
        steps: [
          { action: 'increase_timeout', duration: 60000 },
          { action: 'retry_with_backoff', duration: 120000 },
          { action: 'gradual_recovery', duration: 300000 }
        ],
        estimatedTime: 480000
      },
      'RESOURCE': {
        type: 'RESOURCE_RECOVERY',
        steps: [
          { action: 'cleanup_resources', duration: 30000 },
          { action: 'restart_agent', duration: 60000 },
          { action: 'monitor_resources', duration: 300000 },
          { action: 'gradual_recovery', duration: 300000 }
        ],
        estimatedTime: 690000
      },
      'HEALTH': {
        type: 'HEALTH_RECOVERY',
        steps: [
          { action: 'restart_agent', duration: 60000 },
          { action: 'verify_health', duration: 120000 },
          { action: 'gradual_recovery', duration: 300000 }
        ],
        estimatedTime: 480000
      },
      'DEFAULT': {
        type: 'GRADUAL_RECOVERY',
        steps: [
          { action: 'wait_cool_down', duration: 300000 },
          { action: 'send_probe', duration: 60000 },
          { action: 'gradual_recovery', duration: 300000 }
        ],
        estimatedTime: 660000
      }
    };

    return plans[dominantError] || plans.DEFAULT;
  }

  /**
   * 执行恢复步骤
   */
  async executeStep(step) {
    const actions = {
      'increase_timeout': () => {
        this.config.timeout *= 1.5;
        console.log(`⏱️ 超时时间增加到 ${this.config.timeout}ms`);
      },
      'cleanup_resources': () => {
        // 清理缓存、释放内存
        console.log(`🧹 清理资源中...`);
        if (global.gc) global.gc(); // 强制 GC
      },
      'restart_agent': () => {
        console.log(`🔄 重启 Agent 中...`);
        // TODO: 实际重启逻辑
      },
      'verify_health': () => {
        console.log(`❤️ 验证健康状态...`);
        // TODO: 健康检查
      },
      'send_probe': () => {
        console.log(`📡 发送探测请求...`);
        // TODO: 探测请求
      },
      'gradual_recovery': () => {
        console.log(`📈 开始渐进恢复...`);
        return this.gradualRecovery();
      },
      'wait_cool_down': () => {
        console.log(`⏳ 等待冷却期...`);
        return new Promise(resolve => setTimeout(resolve, step.duration));
      }
    };

    if (actions[step.action]) {
      await actions[step.action]();
    }
  }

  /**
   * 渐进恢复
   */
  async gradualRecovery() {
    const phases = [
      { percentage: 10, duration: 60000 },   // 10% 流量，1 分钟
      { percentage: 30, duration: 120000 },  // 30% 流量，2 分钟
      { percentage: 60, duration: 180000 },  // 60% 流量，3 分钟
      { percentage: 100, duration: 0 }       // 100% 流量
    ];

    this.trafficPercentage = 10;

    for (const phase of phases) {
      console.log(`📈 [${this.agentName}] 恢复进度：${phase.percentage}%`);
      this.trafficPercentage = phase.percentage;
      
      if (phase.duration > 0) {
        await this.monitorPhase(phase);
      }
    }

    // 恢复完成，回到正常状态
    this.transitionTo('NORMAL');
  }

  /**
   * 监控恢复阶段
   */
  async monitorPhase(phase) {
    const startTime = Date.now();
    
    while (Date.now() - startTime < phase.duration) {
      // 检查是否有新错误
      if (this.failureCount > 0) {
        console.warn(`⚠️ [${this.agentName}] 恢复阶段检测到错误，回退`);
        this.trafficPercentage = Math.max(10, this.trafficPercentage / 2);
        return;
      }
      
      await new Promise(resolve => setTimeout(resolve, 5000));
    }
  }

  // ============ 工具方法 ============

  updateMetrics() {
    this.metrics.errorRate = this.metrics.totalRequests > 0 
      ? this.metrics.totalFailures / this.metrics.totalRequests 
      : 0;
    this.metrics.successRate = (1 - this.metrics.errorRate) * 100;
  }

  getDominantErrorType() {
    return Object.entries(this.errorStats)
      .sort((a, b) => b[1] - a[1])[0]?.[0] || 'UNKNOWN';
  }

  increaseTraffic() {
    this.trafficPercentage = Math.min(100, (this.trafficPercentage || 10) + 20);
    console.log(`📈 [${this.agentName}] 流量增加到 ${this.trafficPercentage}%`);
  }

  sendAlert(type, data) {
    console.log(`🚨 [${this.agentName}] 告警：${type}`, data);
    // TODO: 发送到告警系统
  }

  sendNotification(type, data) {
    console.log(`📢 [${this.agentName}] 通知：${type}`, data);
    // TODO: 发送到通知系统
  }

  logStateChange(oldState, newState) {
    const logFile = path.join(CONFIG.logsDir, 'state-changes.log');
    const log = `[${new Date().toISOString()}] ${this.agentName}: ${oldState} → ${newState}\n`;
    fs.appendFileSync(logFile, log);
  }

  backupState() {
    const backupFile = path.join(
      CONFIG.logsDir,
      `backup-${this.agentName}-${Date.now()}.json`
    );
    const state = {
      agentName: this.agentName,
      state: this.state,
      failureCount: this.failureCount,
      errorStats: this.errorStats,
      metrics: this.metrics,
      timestamp: Date.now()
    };
    fs.writeFileSync(backupFile, JSON.stringify(state, null, 2));
    console.log(`💾 [${this.agentName}] 状态已备份：${backupFile}`);
  }

  saveState() {
    // 保存到状态文件（简化版）
  }

  waitForCurrentTasks() {
    console.log(`⏳ [${this.agentName}] 等待当前任务完成...`);
    // TODO: 等待逻辑
  }

  sendProbeRequest() {
    console.log(`📡 [${this.agentName}] 发送探测请求...`);
    // TODO: 探测请求逻辑
  }

  async verifyStepResult(step) {
    // TODO: 验证步骤结果
    return true;
  }

  async handleStepFailure(step, error) {
    console.error(`❌ [${this.agentName}] 步骤 ${step.action} 失败处理`, error);
    // TODO: 失败处理逻辑
  }

  // ============ 状态查询 ============

  getState() {
    return {
      agentName: this.agentName,
      state: this.state,
      failureCount: this.failureCount,
      successCount: this.successCount,
      errorStats: this.errorStats,
      metrics: this.metrics,
      trafficPercentage: this.trafficPercentage || 100,
      lastStateChange: this.lastStateChange,
      uptime: Date.now() - this.lastStateChange
    };
  }

  canAcceptRequest() {
    if (this.state === 'OPEN') return false;
    if (this.state === 'NORMAL') return true;
    if (this.state === 'WARNING') return true;
    if (this.state === 'HALF_OPEN') return Math.random() < 0.5; // 50% 概率
    if (this.state === 'RECOVERING') return Math.random() < (this.trafficPercentage / 100);
    
    return true;
  }
}

// ============ 熔断器管理器 ============

class CircuitBreakerManager {
  constructor() {
    this.breakers = new Map();
    this.ensureDirs();
    this.startMonitoring();
  }

  ensureDirs() {
    fs.mkdirSync(CONFIG.logsDir, { recursive: true });
  }

  /**
   * 获取或创建熔断器
   */
  getBreaker(agentName) {
    if (!this.breakers.has(agentName)) {
      this.breakers.set(agentName, new CircuitBreaker(agentName));
    }
    return this.breakers.get(agentName);
  }

  /**
   * 记录请求结果
   */
  recordResult(agentName, success, error = null, responseTime = 0) {
    const breaker = this.getBreaker(agentName);
    breaker.recordResult(success, error, responseTime);
  }

  /**
   * 检查是否可以接受请求
   */
  canAcceptRequest(agentName) {
    const breaker = this.getBreaker(agentName);
    return breaker.canAcceptRequest();
  }

  /**
   * 获取所有熔断器状态
   */
  getAllStates() {
    const states = {};
    for (const [name, breaker] of this.breakers) {
      states[name] = breaker.getState();
    }
    return states;
  }

  /**
   * 打印状态
   */
  printStatus() {
    console.log('\n📊 熔断器状态:\n');
    
    for (const [name, breaker] of this.breakers) {
      const state = breaker.getState();
      const statusIcon = this.getStatusIcon(state.state);
      console.log(`${statusIcon} ${name}: ${state.state}`);
      console.log(`   失败：${state.failureCount} | 成功率：${state.metrics.successRate.toFixed(1)}%`);
      console.log(`   流量：${state.trafficPercentage}% | 主要错误：${breaker.getDominantErrorType()}\n`);
    }
  }

  getStatusIcon(state) {
    const icons = {
      'NORMAL': '✅',
      'WARNING': '⚠️',
      'HALF_OPEN': '🟡',
      'OPEN': '🔴',
      'RECOVERING': '🔄'
    };
    return icons[state] || '❓';
  }

  startMonitoring() {
    // 每分钟打印一次状态
    setInterval(() => {
      this.printStatus();
    }, 60000);

    console.log('✅ 熔断器监控已启动');
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
Agent 熔断恢复管理器 v5.2

用法：node circuit-breaker.js <命令> [选项]

命令:
  status              查看所有熔断器状态
  test <Agent>        测试 Agent 熔断
  reset <Agent>       重置 Agent 熔断器
  recover <Agent>     手动触发恢复

示例:
  node circuit-breaker.js status
  node circuit-breaker.js test chapter_writer
  node circuit-breaker.js reset chapter_writer
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help') {
    printHelp();
    return;
  }

  const manager = new CircuitBreakerManager();

  switch (command) {
    case 'status':
      manager.printStatus();
      break;

    case 'test':
      const testAgent = args[1] || 'test_agent';
      console.log(`🧪 测试 Agent ${testAgent} 熔断...`);
      
      const breaker = manager.getBreaker(testAgent);
      
      // 模拟 5 次失败
      for (let i = 0; i < 5; i++) {
        breaker.recordResult(false, new Error(`测试失败 ${i+1}`));
        await new Promise(r => setTimeout(r, 1000));
      }
      
      console.log('\n测试后状态:');
      manager.printStatus();
      break;

    case 'reset':
      const resetAgent = args[1];
      if (!resetAgent) {
        console.log('❌ 请指定 Agent 名称');
        return;
      }
      console.log(`🔄 重置 Agent ${resetAgent} 熔断器...`);
      manager.breakers.delete(resetAgent);
      console.log('✅ 重置完成');
      break;

    case 'recover':
      const recoverAgent = args[1];
      if (!recoverAgent) {
        console.log('❌ 请指定 Agent 名称');
        return;
      }
      const recoverBreaker = manager.getBreaker(recoverAgent);
      recoverBreaker.triggerAutoRecovery();
      break;

    default:
      console.log(`未知命令：${command}`);
      printHelp();
  }
}

// 导出 API
module.exports = { CircuitBreaker, CircuitBreakerManager, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
