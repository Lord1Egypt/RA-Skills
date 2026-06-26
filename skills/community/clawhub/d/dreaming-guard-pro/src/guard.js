/**
 * Dreaming Guard Pro - Guard Module (Phase 5)
 * 
 * 主入口：协调所有模块
 * 主循环：monitor → analyzer → decision → execute
 * 提供统一的启动/停止/状态查询接口
 * 
 * 纯Node.js实现，零外部依赖
 */

const EventEmitter = require('events');
const os = require('os');
const path = require('path');

// 模块导入
const Logger = require('./logger');
const Config = require('./config');
const StateManager = require('./state-manager');
const Monitor = require('./monitor');
const Archiver = require('./archiver');
const Compressor = require('./compressor');
const Analyzer = require('./analyzer');
const Decision = require('./decision');
const Protector = require('./protector');
const Healer = require('./healer');
const Reporter = require('./reporter');

// 运行状态
const RUN_STATUS = {
  IDLE: 'idle',
  STARTING: 'starting',
  RUNNING: 'running',
  STOPPING: 'stopping',
  STOPPED: 'stopped',
  ERROR: 'error'
};

// 默认配置
const DEFAULT_CONFIG = {
  loopInterval: 30000,      // 主循环间隔30秒
  reportInterval: 3600000,  // 报告间隔1小时
  autoStart: true,          // 自动启动监控
  enableProtector: true,    // 启用进程保护
  enableHealer: true,       // 启用崩溃自愈
  enableReporter: true,     // 启用报告生成
  watchPath: path.join(os.homedir(), '.openclaw', 'workspace', 'memory', '.dreams')
};

/**
 * Guard类 - 主控制器
 */
class Guard extends EventEmitter {
  constructor(options = {}) {
    super();
    
    // 合并配置
    this.config = { ...DEFAULT_CONFIG, ...options };
    
    // 初始化状态
    this.status = RUN_STATUS.IDLE;
    this.loopTimer = null;
    this.reportTimer = null;
    this.startTime = null;
    this.lastLoopTime = null;
    this.loopCount = 0;
    
    // 初始化模块
    this._initModules(options);
    
    // 绑定事件
    this._bindEvents();
  }

  /**
   * 初始化所有模块
   * @param {object} options - 配置选项
   */
  _initModules(options) {
    // 日志器
    this.logger = options.logger || new Logger({
      module: 'guard',
      level: options.logLevel || 'info'
    });
    
    // 配置管理器
    this.configManager = options.configManager || new Config();
    this.configManager.loadSync();
    
    // 状态管理器
    this.stateManager = options.stateManager || new StateManager({
      logger: this.logger.child('state')
    });
    this.stateManager.loadSync();
    
    // 监控器
    this.monitor = options.monitor || new Monitor({
      watchPath: this.config.watchPath,
      interval: this.config.loopInterval,
      logger: this.logger.child('monitor')
    });
    
    // 归档器
    this.archiver = options.archiver || new Archiver({
      logger: this.logger.child('archiver')
    });
    
    // 压缩器
    this.compressor = options.compressor || new Compressor({
      logger: this.logger.child('compressor')
    });
    
    // 分析器
    this.analyzer = options.analyzer || new Analyzer({
      logger: this.logger.child('analyzer')
    });
    
    // 决策引擎
    this.decision = options.decision || new Decision({
      logger: this.logger.child('decision'),
      actionHandlers: this._createActionHandlers()
    });
    
    // 进程保护器
    if (this.config.enableProtector) {
      this.protector = options.protector || new Protector({
        logger: this.logger.child('protector'),
        compressor: this.compressor,
        archiver: this.archiver
      });
    }
    
    // 崩溃自愈器
    if (this.config.enableHealer) {
      this.healer = options.healer || new Healer({
        logger: this.logger.child('healer'),
        stateManager: this.stateManager,
        archiver: this.archiver
      });
    }
    
    // 报告生成器
    if (this.config.enableReporter) {
      this.reporter = options.reporter || new Reporter({
        logger: this.logger.child('reporter'),
        monitor: this.monitor,
        analyzer: this.analyzer,
        decision: this.decision,
        protector: this.protector,
        healer: this.healer,
        stateManager: this.stateManager
      });
    }
    
    this.logger.debug('Modules initialized');
  }

  /**
   * 创建动作处理器
   * @returns {object} 处理器映射
   */
  _createActionHandlers() {
    return {
      no_action: async (ctx) => ({ success: true, message: 'No action needed' }),
      
      notify: async (ctx) => {
        this.logger.info('Notification triggered', ctx);
        this.emit('notify', ctx);
        return { success: true, notified: true };
      },
      
      archive: async (ctx) => {
        this.logger.info('Archive triggered', ctx);
        const result = await this.archiver.archive({
          sourcePath: this.config.watchPath,
          level: 'warm'
        });
        this.stateManager.recordAction({
          action: 'archive',
          result,
          timestamp: Date.now()
        });
        return result;
      },
      
      compress: async (ctx) => {
        this.logger.info('Compress triggered', ctx);
        const result = await this.compressor.compress(
          this.config.watchPath,
          'lossy'
        );
        this.stateManager.recordAction({
          action: 'compress',
          result,
          timestamp: Date.now()
        });
        return result;
      },
      
      emergency: async (ctx) => {
        this.logger.warn('Emergency action triggered', ctx);
        this.emit('emergency', ctx);
        
        // 先压缩
        const compressResult = await this.compressor.compress(
          this.config.watchPath,
          'aggressive'
        );
        
        // 再归档
        const archiveResult = await this.archiver.archive({
          sourcePath: this.config.watchPath,
          level: 'cold'
        });
        
        this.stateManager.recordAction({
          action: 'emergency',
          results: { compress: compressResult, archive: archiveResult },
          timestamp: Date.now()
        });
        
        return {
          success: true,
          compress: compressResult,
          archive: archiveResult
        };
      }
    };
  }

  /**
   * 绑定模块事件
   */
  _bindEvents() {
    // Monitor事件
    this.monitor.on('collect', (snapshot) => {
      this.emit('monitor:collect', snapshot);
    });
    
    this.monitor.on('status', (status) => {
      this.emit('monitor:status', status);
    });
    
    this.monitor.on('error', (err) => {
      this.logger.error('Monitor error', { error: err.message });
      this.emit('error', { source: 'monitor', error: err });
    });
    
    // Protector事件
    if (this.protector) {
      this.protector.on('intervention', (data) => {
        this.emit('protector:intervention', data);
      });
      
      this.protector.on('restart-required', () => {
        this.logger.warn('Gateway restart required by protector');
        this.emit('restart-required', { source: 'protector' });
      });
    }
    
    // Healer事件
    if (this.healer) {
      this.healer.on('crash-detected', (data) => {
        this.logger.warn('Crash detected by healer', data);
        this.emit('crash-detected', data);
      });
      
      this.healer.on('recovery-completed', (data) => {
        this.logger.info('Recovery completed', data);
        this.emit('recovery-completed', data);
      });
      
      this.healer.on('recovery-failed', (data) => {
        this.logger.error('Recovery failed', data);
        this.emit('recovery-failed', data);
      });
    }
    
    this.logger.debug('Events bound');
  }

  /**
   * 启动Guard
   * @returns {Promise<object>} 启动结果
   */
  async start() {
    if (this.status !== RUN_STATUS.IDLE && this.status !== RUN_STATUS.STOPPED) {
      this.logger.warn('Guard already running or transitioning');
      return { success: false, reason: 'already_running' };
    }
    
    this.status = RUN_STATUS.STARTING;
    this.startTime = Date.now();
    this.logger.info('Starting Dreaming Guard Pro');
    this.emit('starting');
    
    try {
      // 启动监控器
      await this.monitor.start();
      this.logger.debug('Monitor started');
      
      // 启动保护器
      if (this.protector) {
        await this.protector.start();
        this.logger.debug('Protector started');
      }
      
      // 启动自愈器
      if (this.healer) {
        await this.healer.start();
        this.logger.debug('Healer started');
      }
      
      // 启动报告定时器
      if (this.reporter && this.config.reportInterval > 0) {
        this.reportTimer = setInterval(() => {
          this._generateReport();
        }, this.config.reportInterval);
        this.logger.debug('Report timer started');
      }
      
      // 启动主循环
      this.loopTimer = setInterval(() => {
        this.runOnce().catch(err => {
          this.logger.error('Loop error', { error: err.message });
        });
      }, this.config.loopInterval);
      
      // 立即执行一次
      await this.runOnce();
      
      this.status = RUN_STATUS.RUNNING;
      this.logger.info('Guard started successfully');
      this.emit('started', { timestamp: this.startTime });
      
      // 保存状态
      this.stateManager.update('guard.status', 'running');
      this.stateManager.update('guard.startTime', this.startTime);
      await this.stateManager.save();
      
      return { success: true, startTime: this.startTime };
      
    } catch (err) {
      this.status = RUN_STATUS.ERROR;
      this.logger.error('Start failed', { error: err.message });
      this.emit('error', { source: 'start', error: err });
      
      return { success: false, error: err.message };
    }
  }

  /**
   * 停止Guard
   * @returns {Promise<object>} 停止结果
   */
  async stop() {
    if (this.status !== RUN_STATUS.RUNNING) {
      return { success: false, reason: 'not_running' };
    }
    
    this.status = RUN_STATUS.STOPPING;
    this.logger.info('Stopping Dreaming Guard Pro');
    this.emit('stopping');
    
    try {
      // 停止主循环
      if (this.loopTimer) {
        clearInterval(this.loopTimer);
        this.loopTimer = null;
      }
      
      // 停止报告定时器
      if (this.reportTimer) {
        clearInterval(this.reportTimer);
        this.reportTimer = null;
      }
      
      // 停止监控器
      await this.monitor.stop();
      this.logger.debug('Monitor stopped');
      
      // 停止保护器
      if (this.protector) {
        await this.protector.stop();
        this.logger.debug('Protector stopped');
      }
      
      // 停止自愈器
      if (this.healer) {
        await this.healer.stop();
        this.logger.debug('Healer stopped');
      }
      
      // 保存最终状态
      this.stateManager.update('guard.status', 'stopped');
      this.stateManager.update('guard.stopTime', Date.now());
      this.stateManager.update('guard.loopCount', this.loopCount);
      await this.stateManager.save();
      
      this.status = RUN_STATUS.STOPPED;
      this.logger.info('Guard stopped', { loopCount: this.loopCount });
      this.emit('stopped', { 
        startTime: this.startTime,
        stopTime: Date.now(),
        duration: Date.now() - this.startTime,
        loopCount: this.loopCount
      });
      
      return { success: true, loopCount: this.loopCount };
      
    } catch (err) {
      this.status = RUN_STATUS.ERROR;
      this.logger.error('Stop failed', { error: err.message });
      this.emit('error', { source: 'stop', error: err });
      
      return { success: false, error: err.message };
    }
  }

  /**
   * 执行一次完整循环
   * @returns {Promise<object>} 循环结果
   */
  async runOnce() {
    this.loopCount++;
    this.lastLoopTime = Date.now();
    
    this.logger.debug('Running loop', { count: this.loopCount });
    this.emit('loop:start', { count: this.loopCount });
    
    const result = {
      loopCount: this.loopCount,
      timestamp: this.lastLoopTime,
      steps: {}
    };
    
    try {
      // Step 1: Monitor - 获取最新数据
      const snapshot = this.monitor.getLatestSnapshot();
      const history = this.monitor.getHistory(60);
      result.steps.monitor = {
        success: true,
        currentSize: snapshot?.totalSize || 0,
        currentFiles: snapshot?.totalFiles || 0
      };
      
      // Step 2: Analyzer - 分析趋势
      const analysis = this.analyzer.analyze(history);
      result.steps.analyzer = {
        success: analysis.valid,
        riskLevel: analysis.riskLevel,
        growthRateKB: analysis.growthRateKB
      };
      
      // Step 3: Decision - 决策
      const decisionResult = this.decision.decide(analysis);
      result.steps.decision = {
        success: true,
        action: decisionResult.action,
        reason: decisionResult.reason
      };
      
      // Step 4: Execute - 执行动作
      if (decisionResult.action !== 'no_action') {
        const actionPlan = this.decision.getActionPlan(decisionResult.action);
        const executeResult = await this.decision.executeAction(
          decisionResult.action,
          { analysis, decision: decisionResult, plan: actionPlan }
        );
        result.steps.execute = {
          success: executeResult.success,
          action: decisionResult.action,
          result: executeResult.result
        };
        
        if (executeResult.success) {
          this.emit('action:executed', { action: decisionResult.action, result: executeResult });
        }
      } else {
        result.steps.execute = { success: true, action: 'no_action' };
      }
      
      this.emit('loop:complete', result);
      return result;
      
    } catch (err) {
      result.error = err.message;
      this.logger.error('Loop failed', { error: err.message, loop: this.loopCount });
      this.emit('loop:error', { count: this.loopCount, error: err });
      return result;
    }
  }

  /**
   * 生成报告
   */
  _generateReport() {
    if (!this.reporter) return;
    
    const report = this.reporter.generate('text');
    this.reporter.saveReport(report);
    
    this.emit('report:generated', report);
    this.logger.info('Report generated', { timestamp: report.timestamp });
  }

  /**
   * 获取当前状态
   * @returns {object} 状态对象
   */
  getStatus() {
    return {
      status: this.status,
      startTime: this.startTime,
      lastLoopTime: this.lastLoopTime,
      loopCount: this.loopCount,
      uptime: this.startTime ? Date.now() - this.startTime : 0,
      
      monitor: this.monitor.getStatus(),
      protector: this.protector?.getStatus() || null,
      healer: this.healer?.getStatus() || null,
      
      config: {
        loopInterval: this.config.loopInterval,
        reportInterval: this.config.reportInterval,
        watchPath: this.config.watchPath,
        enableProtector: this.config.enableProtector,
        enableHealer: this.config.enableHealer
      },
      
      summary: this.reporter?.getSummary() || null
    };
  }

  /**
   * 获取健康报告
   * @param {string} format - 报告格式
   * @returns {object} 报告对象
   */
  getHealthReport(format = 'text') {
    if (!this.reporter) {
      return { error: 'Reporter not enabled' };
    }
    return this.reporter.generate(format);
  }

  /**
   * 手动触发动作
   * @param {string} action - 动作类型
   * @param {object} context - 上下文
   * @returns {Promise<object>} 执行结果
   */
  async triggerAction(action, context = {}) {
    this.logger.info('Manual action triggered', { action });
    
    const result = await this.decision.executeAction(action, {
      ...context,
      manual: true,
      timestamp: Date.now()
    });
    
    this.emit('action:manual', { action, result });
    
    return result;
  }

  /**
   * 手动触发归档
   * @param {object} options - 归档选项
   * @returns {Promise<object>} 归档结果
   */
  async triggerArchive(options = {}) {
    return await this.triggerAction('archive', options);
  }

  /**
   * 手动触发压缩
   * @param {string} strategy - 压缩策略
   * @returns {Promise<object>} 压缩结果
   */
  async triggerCompress(strategy = 'lossy') {
    const result = await this.compressor.compress(this.config.watchPath, strategy);
    
    this.stateManager.recordAction({
      action: 'manual_compress',
      strategy,
      result,
      timestamp: Date.now()
    });
    
    return result;
  }

  /**
   * 手动触发健康检查
   * @returns {object} 检查结果
   */
  async healthCheck() {
    const result = await this.runOnce();
    
    return {
      healthy: result.steps.execute?.success !== false,
      status: this.status,
      riskLevel: result.steps.analyzer?.riskLevel,
      details: result
    };
  }

  /**
   * 重置所有统计
   */
  resetStats() {
    this.loopCount = 0;
    this.monitor?.clearHistory();
    this.protector?.resetStats();
    this.healer?.resetStats();
    this.decision?.resetState();
    
    this.logger.info('Stats reset');
    this.emit('stats:reset');
  }
}

// 导出
module.exports = Guard;
module.exports.RUN_STATUS = RUN_STATUS;

// 也导出所有子模块，方便独立使用
module.exports.Logger = Logger;
module.exports.Config = Config;
module.exports.StateManager = StateManager;
module.exports.Monitor = Monitor;
module.exports.Archiver = Archiver;
module.exports.Compressor = Compressor;
module.exports.Analyzer = Analyzer;
module.exports.Decision = Decision;
module.exports.Protector = Protector;
module.exports.Healer = Healer;
module.exports.Reporter = Reporter;