#!/usr/bin/env node
/**
 * 监控告警系统 v1.0
 * 
 * 核心职责：
 * 1. Token 使用监控
 * 2. 缓存命中率监控
 * 3. Agent 状态监控
 * 4. 任务队列监控
 * 5. 自动告警
 */

const fs = require('fs');
const path = require('path');

class MonitoringAlertSystem {
  constructor(options = {}) {
    this.workspace = options.workspace || '/home/ubutu/.openclaw/workspace';
    this.logFile = options.logFile || path.join(this.workspace, 'logs/monitoring/alerts.json');
    this.stateFile = options.stateFile || path.join(this.workspace, 'logs/monitoring/monitor-state.json');
    
    // 告警阈值配置
    this.thresholds = {
      tokenUsage: {
        warning: 80,    // 80% 预警
        critical: 95    // 95% 严重
      },
      cacheHitRate: {
        warning: 30,    // 低于 30% 预警
        critical: 10    // 低于 10% 严重
      },
      taskFailureRate: {
        warning: 20,    // 失败率 20% 预警
        critical: 50    // 失败率 50% 严重
      },
      agentOffline: {
        warning: 1,     // 1 个 Agent 离线预警
        critical: 3     // 3 个 Agent 离线严重
      },
      queueLength: {
        warning: 50,    // 队列 50 个任务预警
        critical: 100   // 队列 100 个任务严重
      }
    };
    
    // 告警冷却（防止重复告警）
    this.alertCooldown = options.alertCooldown || 3600000; // 1 小时
    this.lastAlerts = this.loadLastAlerts();
    
    // 统计
    this.stats = {
      alertsSent: 0,
      warnings: 0,
      criticals: 0
    };
    
    this.ensureDirs();
  }

  ensureDirs() {
    const dir = path.dirname(this.logFile);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }

  loadLastAlerts() {
    if (fs.existsSync(this.stateFile)) {
      try {
        return JSON.parse(fs.readFileSync(this.stateFile, 'utf-8'));
      } catch {
        return {};
      }
    }
    return {};
  }

  saveLastAlerts() {
    fs.writeFileSync(this.stateFile, JSON.stringify(this.lastAlerts, null, 2));
  }

  // ============ 核心监控方法 ============

  /**
   * 检查 Token 使用情况
   */
  checkTokenUsage(usage) {
    const { used, total } = usage;
    const percentage = (used / total * 100).toFixed(1);
    
    if (percentage >= this.thresholds.tokenUsage.critical) {
      this.sendAlert('critical', 'token_usage', `Token 使用已达 ${percentage}%，即将耗尽！`, {
        used, total, percentage
      });
    } else if (percentage >= this.thresholds.tokenUsage.warning) {
      this.sendAlert('warning', 'token_usage', `Token 使用已达 ${percentage}%，请注意控制`, {
        used, total, percentage
      });
    }
    
    return { percentage, status: this.getTokenStatus(percentage) };
  }

  /**
   * 检查缓存命中率
   */
  checkCacheHitRate(hitRate) {
    const rate = parseFloat(hitRate);
    
    if (rate < this.thresholds.cacheHitRate.critical) {
      this.sendAlert('critical', 'cache_hit_rate', `缓存命中率仅 ${rate}%，严重影响性能！`, { hitRate });
    } else if (rate < this.thresholds.cacheHitRate.warning) {
      this.sendAlert('warning', 'cache_hit_rate', `缓存命中率 ${rate}% 偏低，建议优化`, { hitRate });
    }
    
    return { hitRate: rate, status: rate >= 30 ? 'healthy' : 'warning' };
  }

  /**
   * 检查任务失败率
   */
  checkTaskFailureRate(stats) {
    const { completed, failed } = stats;
    const total = completed + failed;
    if (total === 0) return { failureRate: 0, status: 'healthy' };
    
    const failureRate = (failed / total * 100).toFixed(1);
    
    if (failureRate >= this.thresholds.taskFailureRate.critical) {
      this.sendAlert('critical', 'task_failure', `任务失败率 ${failureRate}%，系统异常！`, stats);
    } else if (failureRate >= this.thresholds.taskFailureRate.warning) {
      this.sendAlert('warning', 'task_failure', `任务失败率 ${failureRate}%，需要关注`, stats);
    }
    
    return { failureRate, status: failureRate < 20 ? 'healthy' : 'warning' };
  }

  /**
   * 检查 Agent 状态
   */
  checkAgentStatus(agents) {
    const offline = agents.filter(a => a.status !== 'online').length;
    
    if (offline >= this.thresholds.agentOffline.critical) {
      this.sendAlert('critical', 'agent_offline', `${offline} 个 Agent 离线，严重影响执行！`, { offline, total: agents.length });
    } else if (offline >= this.thresholds.agentOffline.warning) {
      this.sendAlert('warning', 'agent_offline', `${offline} 个 Agent 离线`, { offline, total: agents.length });
    }
    
    return { offline, status: offline === 0 ? 'healthy' : 'warning' };
  }

  /**
   * 检查任务队列
   */
  checkQueueLength(length) {
    if (length >= this.thresholds.queueLength.critical) {
      this.sendAlert('critical', 'queue_length', `任务队列 ${length} 个任务积压！`, { length });
    } else if (length >= this.thresholds.queueLength.warning) {
      this.sendAlert('warning', 'queue_length', `任务队列 ${length} 个任务等待`, { length });
    }
    
    return { length, status: length < 50 ? 'healthy' : 'warning' };
  }

  // ============ 告警方法 ============

  /**
   * 发送告警
   */
  sendAlert(level, type, message, data) {
    const alertKey = `${level}:${type}`;
    
    // 检查冷却时间
    const lastAlert = this.lastAlerts[alertKey];
    if (lastAlert && Date.now() - lastAlert < this.alertCooldown) {
      console.log(`[Monitoring] 告警冷却中: ${alertKey}`);
      return false;
    }
    
    // 创建告警
    const alert = {
      id: `alert-${Date.now()}`,
      level,      // warning, critical
      type,       // token_usage, cache_hit_rate, task_failure, agent_offline, queue_length
      message,
      data,
      timestamp: Date.now()
    };
    
    // 记录
    this.lastAlerts[alertKey] = Date.now();
    this.saveLastAlerts();
    
    // 更新统计
    this.stats.alertsSent++;
    if (level === 'warning') this.stats.warnings++;
    if (level === 'critical') this.stats.criticals++;
    
    // 输出
    const emoji = level === 'critical' ? '🚨' : '⚠️';
    console.log(`\n${emoji} [${level.toUpperCase()}] ${message}`);
    console.log(`   类型: ${type}`);
    console.log(`   数据: ${JSON.stringify(data)}`);
    console.log(`   时间: ${new Date().toISOString()}\n`);
    
    // 持久化
    this.logAlert(alert);
    
    return true;
  }

  /**
   * 记录告警日志
   */
  logAlert(alert) {
    let alerts = [];
    if (fs.existsSync(this.logFile)) {
      try {
        alerts = JSON.parse(fs.readFileSync(this.logFile, 'utf-8'));
      } catch {}
    }
    
    alerts.push(alert);
    
    // 保留最近 1000 条
    if (alerts.length > 1000) {
      alerts = alerts.slice(-1000);
    }
    
    fs.writeFileSync(this.logFile, JSON.stringify(alerts, null, 2));
  }

  /**
   * 获取 Token 状态描述
   */
  getTokenStatus(percentage) {
    if (percentage >= 95) return 'critical';
    if (percentage >= 80) return 'warning';
    if (percentage >= 50) return 'moderate';
    return 'healthy';
  }

  // ============ 综合检查 ============

  /**
   * 执行全面健康检查
   */
  runFullCheck(data) {
    console.log('\n🔍 执行全面健康检查...');
    
    const results = {
      timestamp: Date.now(),
      checks: {}
    };
    
    // 1. Token 使用检查
    if (data.tokenUsage) {
      results.checks.token = this.checkTokenUsage(data.tokenUsage);
    }
    
    // 2. 缓存命中率检查
    if (data.cacheHitRate) {
      results.checks.cache = this.checkCacheHitRate(data.cacheHitRate);
    }
    
    // 3. 任务失败率检查
    if (data.taskStats) {
      results.checks.tasks = this.checkTaskFailureRate(data.taskStats);
    }
    
    // 4. Agent 状态检查
    if (data.agents) {
      results.checks.agents = this.checkAgentStatus(data.agents);
    }
    
    // 5. 队列长度检查
    if (data.queueLength !== undefined) {
      results.checks.queue = this.checkQueueLength(data.queueLength);
    }
    
    // 总体状态
    const statuses = Object.values(results.checks).map(c => c.status);
    results.overall = statuses.includes('critical') ? 'critical' :
                       statuses.includes('warning') ? 'warning' : 'healthy';
    
    console.log(`\n📊 检查结果: ${results.overall.toUpperCase()}`);
    console.log(JSON.stringify(results.checks, null, 2));
    
    return results;
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      ...this.stats,
      thresholds: this.thresholds,
      lastAlerts: this.lastAlerts
    };
  }
}

// CLI 入口
if (require.main === module) {
  const monitoring = new MonitoringAlertSystem();
  
  // 模拟测试
  console.log('📊 监控告警系统测试\n');
  
  // 测试 Token 使用检查
  monitoring.checkTokenUsage({ used: 85000, total: 100000 });
  
  // 测试缓存命中率检查
  monitoring.checkCacheHitRate('25%');
  
  // 执行全面检查
  monitoring.runFullCheck({
    tokenUsage: { used: 90000, total: 100000 },
    cacheHitRate: '35%',
    taskStats: { completed: 80, failed: 15 },
    agents: [
      { id: 'agent-1', status: 'online' },
      { id: 'agent-2', status: 'offline' }
    ],
    queueLength: 30
  });
}

module.exports = {
  MonitoringAlertSystem
};