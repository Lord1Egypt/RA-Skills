/**
 * Dreaming Guard Pro - Protector Module (Phase 4)
 * 
 * 进程保护：监控进程内存，危险时主动干预
 * 内存阈值分级：warning(70%) → critical(85%) → emergency(95%)
 * 干预措施：压缩 → 归档 → 重启gateway
 * 
 * 纯Node.js实现，零外部依赖
 */

const EventEmitter = require('events');
const Compressor = require('./compressor');
const Archiver = require('./archiver');
const Logger = require('./logger');

// 干预级别定义
const INTERVENTION_LEVELS = {
  NORMAL: 'normal',      // 内存正常
  WARNING: 'warning',    // 70% - 预警，触发压缩
  CRITICAL: 'critical',  // 85% - 严重，触发归档+压缩
  EMERGENCY: 'emergency' // 95% - 紧急，重启gateway
};

// 内存阈值（百分比）
const MEMORY_THRESHOLDS = {
  warning: 0.70,
  critical: 0.85,
  emergency: 0.95
};

// 默认配置
const DEFAULT_CONFIG = {
  checkInterval: 10000,    // 10秒检查间隔
  maxMemoryMB: 512,        // 默认最大内存512MB
  thresholds: MEMORY_THRESHOLDS,
  actions: {
    warning: ['compress'],
    critical: ['compress', 'archive'],
    emergency: ['compress', 'archive', 'restart']
  },
  cooldown: 60000          // 干预冷却时间60秒
};

/**
 * Protector类 - 进程保护器
 */
class Protector extends EventEmitter {
  constructor(options = {}) {
    super();
    
    // 合并配置
    this.config = { ...DEFAULT_CONFIG, ...options };
    
    // 初始化模块
    this.logger = options.logger || new Logger({ module: 'protector' });
    this.compressor = options.compressor || new Compressor({ 
      logger: this.logger.child('compressor') 
    });
    this.archiver = options.archiver || new Archiver({
      logger: this.logger.child('archiver')
    });
    
    // 状态
    this.running = false;
    this.timer = null;
    this.lastIntervention = null;
    this.lastInterventionTime = 0;
    this.stats = {
      checks: 0,
      interventions: 0,
      warnings: 0,
      criticals: 0,
      emergencies: 0
    };
  }

  /**
   * 开始保护监控
   */
  async start() {
    if (this.running) return;
    
    this.running = true;
    this.logger.info('Protector started', { interval: this.config.checkInterval });
    
    this.timer = setInterval(() => {
      this.check().catch(err => {
        this.logger.error('Check failed', { error: err.message });
        this.emit('error', err);
      });
    }, this.config.checkInterval);
    
    this.emit('started');
  }

  /**
   * 停止保护监控
   */
  async stop() {
    if (!this.running) return;
    
    this.running = false;
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    
    this.logger.info('Protector stopped');
    this.emit('stopped');
  }

  /**
   * 检查当前内存状态
   * @returns {object} 检查结果
   */
  async check() {
    this.stats.checks++;
    
    // 获取进程内存使用
    const memoryUsage = process.memoryUsage();
    const rssMB = memoryUsage.rss / (1024 * 1024);
    const heapUsedMB = memoryUsage.heapUsed / (1024 * 1024);
    const heapTotalMB = memoryUsage.heapTotal / (1024 * 1024);
    
    // 计算使用率
    const maxMemoryMB = this.config.maxMemoryMB;
    const usagePercent = rssMB / maxMemoryMB;
    
    // 确定干预级别
    const intervention = this.getIntervention(usagePercent);
    
    // 构建检查结果
    const result = {
      timestamp: Date.now(),
      memory: {
        rssMB: Math.round(rssMB * 100) / 100,
        heapUsedMB: Math.round(heapUsedMB * 100) / 100,
        heapTotalMB: Math.round(heapTotalMB * 100) / 100,
        usagePercent: Math.round(usagePercent * 100) / 100
      },
      intervention,
      maxMemoryMB,
      stats: this.stats
    };
    
    // 触发事件
    this.emit('check', result);
    
    // 执行干预（如果需要且不在冷却期）
    if (intervention.level !== INTERVENTION_LEVELS.NORMAL) {
      const cooldownElapsed = Date.now() - this.lastInterventionTime;
      if (cooldownElapsed >= this.config.cooldown) {
        await this.executeIntervention(intervention.level);
      } else {
        this.logger.debug('Intervention in cooldown', {
          remaining: Math.round((this.config.cooldown - cooldownElapsed) / 1000) + 's'
        });
      }
    }
    
    return result;
  }

  /**
   * 根据内存使用率确定干预级别
   * @param {number} usagePercent - 内存使用率 (0-1)
   * @returns {object} 干预决策
   */
  getIntervention(usagePercent) {
    const thresholds = this.config.thresholds;
    let level = INTERVENTION_LEVELS.NORMAL;
    let actions = [];
    
    if (usagePercent >= thresholds.emergency) {
      level = INTERVENTION_LEVELS.EMERGENCY;
      actions = this.config.actions.emergency;
      this.stats.emergencies++;
    } else if (usagePercent >= thresholds.critical) {
      level = INTERVENTION_LEVELS.CRITICAL;
      actions = this.config.actions.critical;
      this.stats.criticals++;
    } else if (usagePercent >= thresholds.warning) {
      level = INTERVENTION_LEVELS.WARNING;
      actions = this.config.actions.warning;
      this.stats.warnings++;
    }
    
    return {
      level,
      actions,
      usagePercent,
      thresholds,
      reason: this._getInterventionReason(level, usagePercent)
    };
  }

  /**
   * 获取干预原因描述
   */
  _getInterventionReason(level, usagePercent) {
    const percent = Math.round(usagePercent * 100);
    switch (level) {
      case INTERVENTION_LEVELS.EMERGENCY:
        return `Memory usage ${percent}% exceeds emergency threshold ${Math.round(this.config.thresholds.emergency * 100)}%`;
      case INTERVENTION_LEVELS.CRITICAL:
        return `Memory usage ${percent}% exceeds critical threshold ${Math.round(this.config.thresholds.critical * 100)}%`;
      case INTERVENTION_LEVELS.WARNING:
        return `Memory usage ${percent}% exceeds warning threshold ${Math.round(this.config.thresholds.warning * 100)}%`;
      default:
        return 'Memory usage normal';
    }
  }

  /**
   * 执行干预措施
   * @param {string} level - 干预级别
   * @returns {object} 执行结果
   */
  async executeIntervention(level) {
    if (level === INTERVENTION_LEVELS.NORMAL) {
      return { success: true, actions: [], reason: 'No intervention needed' };
    }
    
    this.stats.interventions++;
    this.lastIntervention = level;
    this.lastInterventionTime = Date.now();
    
    this.logger.warn('Executing intervention', { level });
    this.emit('intervention', { level, timestamp: Date.now() });
    
    const intervention = this.getIntervention(
      process.memoryUsage().rss / (this.config.maxMemoryMB * 1024 * 1024)
    );
    const actions = intervention.actions;
    const results = [];
    
    for (const action of actions) {
      try {
        const result = await this._executeAction(action);
        results.push({ action, success: true, result });
        this.logger.info('Action completed', { action });
      } catch (err) {
        results.push({ action, success: false, error: err.message });
        this.logger.error('Action failed', { action, error: err.message });
      }
    }
    
    const success = results.every(r => r.success);
    
    return {
      success,
      level,
      actions: results,
      timestamp: Date.now()
    };
  }

  /**
   * 执行单个干预动作
   * @param {string} action - 动作类型
   */
  async _executeAction(action) {
    switch (action) {
      case 'compress':
        // 触发压缩
        const compressResult = await this.compressor.compress(
          this._getDreamingPath(),
          'lossy'
        );
        return { compressed: compressResult.reduction };
        
      case 'archive':
        // 触发归档
        const archiveResult = await this.archiver.archive({
          sourcePath: this._getDreamingPath(),
          level: 'warm'
        });
        return { archived: archiveResult.totalFiles };
        
      case 'restart':
        // 重启gateway（模拟，不实际执行）
        this.logger.warn('Gateway restart triggered (simulated)');
        this.emit('restart-required');
        return { restart: 'triggered' };
        
      default:
        throw new Error(`Unknown action: ${action}`);
    }
  }

  /**
   * 获取dreaming路径
   */
  _getDreamingPath() {
    const os = require('os');
    const path = require('path');
    return path.join(os.homedir(), '.openclaw', 'workspace', 'memory', '.dreams');
  }

  /**
   * 获取当前状态
   */
  getStatus() {
    return {
      running: this.running,
      stats: this.stats,
      lastIntervention: this.lastIntervention,
      lastInterventionTime: this.lastInterventionTime,
      config: {
        maxMemoryMB: this.config.maxMemoryMB,
        thresholds: this.config.thresholds
      }
    };
  }

  /**
   * 重置统计
   */
  resetStats() {
    this.stats = {
      checks: 0,
      interventions: 0,
      warnings: 0,
      criticals: 0,
      emergencies: 0
    };
  }
}

module.exports = Protector;
module.exports.INTERVENTION_LEVELS = INTERVENTION_LEVELS;
module.exports.MEMORY_THRESHOLDS = MEMORY_THRESHOLDS;