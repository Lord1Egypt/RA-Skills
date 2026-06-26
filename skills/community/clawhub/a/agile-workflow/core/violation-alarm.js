#!/usr/bin/env node
/**
 * 违规告警系统 v7.20
 * 
 * 核心功能:
 * 1. 记录数据真实性违规
 * 2. 触发告警（控制台 + 日志）
 * 3. 统计违规次数
 */

const fs = require('fs');
const path = require('path');

class ViolationAlarm {
  constructor(config = {}) {
    this.alarmLog = config.alarmLog || '/home/ubutu/.openclaw/workspace/logs/violations.log';
    this.violations = [];
    this.alertCallbacks = config.alertCallbacks || [];
    
    // 确保日志目录存在
    const logDir = path.dirname(this.alarmLog);
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
  }

  /**
   * 记录违规
   */
  recordViolation(type, details, severity = 'medium') {
    const violation = {
      id: this.generateId(),
      timestamp: new Date().toISOString(),
      type,
      details,
      severity: this.getSeverity(type, severity),
      handled: false
    };

    this.violations.push(violation);
    this.logViolation(violation);
    this.triggerAlarm(violation);

    return violation;
  }

  /**
   * 生成违规 ID
   */
  generateId() {
    return `V${Date.now()}-${Math.random().toString(36).substr(2, 6)}`;
  }

  /**
   * 获取违规严重程度
   */
  getSeverity(type, custom) {
    if (custom) return custom;
    
    const severityMap = {
      'fabrication': 'critical',  // 编造数据
      'no-source': 'high',        // 无来源
      'estimation': 'high',       // 预估数据
      'unverified': 'medium',     // 未验证
      'no-verification': 'medium' // 缺少验证
    };
    
    return severityMap[type] || 'medium';
  }

  /**
   * 记录到日志
   */
  logViolation(violation) {
    const log = `[${violation.timestamp}] ${violation.severity.toUpperCase()}: ${violation.type} - ${JSON.stringify(violation.details)}\n`;
    
    try {
      fs.appendFileSync(this.alarmLog, log);
    } catch (error) {
      console.error('记录违规日志失败:', error.message);
    }
  }

  /**
   * 触发告警
   */
  triggerAlarm(violation) {
    const emoji = {
      'critical': '🚨',
      'high': '⚠️',
      'medium': '⚡',
      'low': 'ℹ️'
    };
    
    console.error(`\n${emoji[violation.severity] || '⚠️'} 数据真实性违规告警`);
    console.error(`ID: ${violation.id}`);
    console.error(`类型：${violation.type}`);
    console.error(`严重程度：${violation.severity}`);
    console.error(`详情：${JSON.stringify(violation.details)}`);
    console.error(`时间：${violation.timestamp}`);
    console.error(`日志：${this.alarmLog}\n`);

    // 触发回调
    for (const callback of this.alertCallbacks) {
      try {
        callback(violation);
      } catch (error) {
        console.error('告警回调失败:', error.message);
      }
    }
  }

  /**
   * 添加告警回调
   */
  onAlert(callback) {
    this.alertCallbacks.push(callback);
  }

  /**
   * 获取违规统计
   */
  getStats() {
    const stats = {
      total: this.violations.length,
      byType: {},
      bySeverity: {},
      unhandled: this.violations.filter(v => !v.handled).length
    };

    for (const v of this.violations) {
      stats.byType[v.type] = (stats.byType[v.type] || 0) + 1;
      stats.bySeverity[v.severity] = (stats.bySeverity[v.severity] || 0) + 1;
    }

    return stats;
  }

  /**
   * 从日志文件加载历史违规
   */
  loadFromLog() {
    if (!fs.existsSync(this.alarmLog)) {
      return [];
    }

    const log = fs.readFileSync(this.alarmLog, 'utf8');
    const lines = log.split('\n').filter(l => l.trim());
    const violations = [];

    for (const line of lines) {
      const match = line.match(/\[(.*?)\] (\w+): (\w+) - (.+)/);
      if (match) {
        violations.push({
          timestamp: match[1],
          severity: match[2],
          type: match[3],
          details: JSON.parse(match[4])
        });
      }
    }

    return violations;
  }

  /**
   * 标记违规为已处理
   */
  markHandled(violationId) {
    const violation = this.violations.find(v => v.id === violationId);
    if (violation) {
      violation.handled = true;
    }
  }

  /**
   * 清除历史违规
   */
  clearHistory() {
    this.violations = [];
    if (fs.existsSync(this.alarmLog)) {
      fs.writeFileSync(this.alarmLog, '');
    }
  }
}

module.exports = ViolationAlarm;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [command] = args;
  
  const alarm = new ViolationAlarm();
  
  if (command === 'test') {
    // 测试告警
    console.log('测试：记录编造数据违规');
    alarm.recordViolation('fabrication', {
      data: 'Kimi 有 256K 上下文',
      source: '编造'
    }, 'critical');
    
    console.log('\n违规统计:');
    const stats = alarm.getStats();
    console.log(`总次数：${stats.total}`);
    console.log(`未处理：${stats.unhandled}`);
    console.log('按类型:');
    for (const [type, count] of Object.entries(stats.byType)) {
      console.log(`  ${type}: ${count}`);
    }
  }
  
  if (command === 'stats') {
    const violations = alarm.loadFromLog();
    console.log(`历史违规：${violations.length} 次`);
    
    const stats = alarm.getStats();
    console.log('\n违规统计:');
    console.log(`总次数：${stats.total}`);
    console.log(`未处理：${stats.unhandled}`);
  }
  
  if (command === 'clear') {
    alarm.clearHistory();
    console.log('✅ 违规历史已清除');
  }
}
