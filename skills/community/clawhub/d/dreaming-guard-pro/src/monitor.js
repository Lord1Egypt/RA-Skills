/**
 * Dreaming Guard Pro - Monitor Module
 * 
 * 实时监控dreaming目录和进程内存
 * 周期性采集数据，计算增长速率
 * 纯Node.js实现，零外部依赖
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const EventEmitter = require('events');

// 默认配置
const DEFAULT_CONFIG = {
  watchPath: null,  // 默认使用workspace的memory/.dreams
  interval: 30000,   // 30秒采集间隔
  historySize: 60,   // 保留60个历史快照（30分钟）
  memoryCheck: true  // 是否检查进程内存
};

/**
 * Monitor类 - 监控器
 * 监控文件大小、数量、增长速率和进程内存
 */
class Monitor extends EventEmitter {
  constructor(options = {}) {
    super();
    
    // 合并配置
    this.config = { ...DEFAULT_CONFIG, ...options };
    
    // 监控状态
    this.running = false;
    this.timer = null;
    
    // 历史数据
    this.history = [];
    this.lastSnapshot = null;
    
    // 绑定日志器
    this.logger = options.logger || {
      debug: (...args) => console.debug('[Monitor]', ...args),
      info: (...args) => console.info('[Monitor]', ...args),
      warn: (...args) => console.warn('[Monitor]', ...args),
      error: (...args) => console.error('[Monitor]', ...args)
    };
    
    // 确定监控路径
    if (!this.config.watchPath) {
      this.config.watchPath = this._detectDreamingPath();
    }
  }

  /**
   * 自动检测dreaming路径
   * @returns {string} dreaming目录路径
   */
  _detectDreamingPath() {
    const homeDir = os.homedir();
    const workspacePath = path.join(homeDir, '.openclaw', 'workspace', 'memory', '.dreams');
    
    // 如果默认路径不存在，尝试查找其他workspace
    if (!fs.existsSync(workspacePath)) {
      const openclawDir = path.join(homeDir, '.openclaw');
      if (fs.existsSync(openclawDir)) {
        const dirs = fs.readdirSync(openclawDir).filter(d => d.startsWith('workspace'));
        for (const dir of dirs) {
          const dreamPath = path.join(openclawDir, dir, 'memory', '.dreams');
          if (fs.existsSync(dreamPath)) {
            return dreamPath;
          }
        }
      }
    }
    
    return workspacePath;
  }

  /**
   * 开始监控
   * @returns {Promise<void>}
   */
  async start() {
    if (this.running) {
      this.logger.warn('Monitor already running');
      return;
    }

    this.running = true;
    this.logger.info('Starting monitor', { path: this.config.watchPath, interval: this.config.interval });

    // 立即执行一次采集
    await this._collect();

    // 启动定时器
    this.timer = setInterval(() => {
      this._collect().catch(err => {
        this.logger.error('Collection error:', err.message);
        this.emit('error', err);
      });
    }, this.config.interval);

    this.emit('started', { path: this.config.watchPath });
  }

  /**
   * 停止监控
   * @returns {Promise<void>}
   */
  async stop() {
    if (!this.running) {
      return;
    }

    this.running = false;
    
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }

    this.logger.info('Monitor stopped');
    this.emit('stopped');
  }

  /**
   * 采集数据
   * @returns {Promise<void>}
   */
  async _collect() {
    const timestamp = Date.now();
    
    try {
      // 采集文件系统数据
      const filesData = this._collectFilesData();
      
      // 采集进程内存数据
      const memoryData = this.config.memoryCheck ? this._collectMemoryData() : null;
      
      // 构建快照
      const snapshot = {
        timestamp,
        files: filesData.files,
        totalSize: filesData.totalSize,
        totalFiles: filesData.totalFiles,
        growthRate: 0, // 稍后计算
        memory: memoryData
      };
      
      // 计算增长速率
      if (this.lastSnapshot) {
        const timeDiff = (timestamp - this.lastSnapshot.timestamp) / 1000; // 秒
        if (timeDiff > 0) {
          const sizeDiff = filesData.totalSize - this.lastSnapshot.totalSize;
          snapshot.growthRate = (sizeDiff / timeDiff) * 60; // bytes/sec -> bytes/min
        }
      }
      
      // 更新历史
      this.history.push(snapshot);
      if (this.history.length > this.config.historySize) {
        this.history.shift();
      }
      
      this.lastSnapshot = snapshot;
      
      // 触发事件
      this.emit('collect', snapshot);
      
      // 检查阈值
      this._checkThresholds(snapshot);
      
    } catch (err) {
      this.logger.error('Collection failed:', err.message);
      this.emit('error', err);
    }
  }

  /**
   * 采集文件数据
   * @returns {object} 文件数据
   */
  _collectFilesData() {
    const watchPath = this.config.watchPath;
    const files = [];
    let totalSize = 0;
    let totalFiles = 0;
    
    if (!fs.existsSync(watchPath)) {
      this.logger.debug('Watch path does not exist:', watchPath);
      return { files, totalSize, totalFiles };
    }
    
    // 递归扫描目录
    const scanDir = (dir) => {
      try {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        
        for (const entry of entries) {
          const fullPath = path.join(dir, entry.name);
          
          if (entry.isDirectory()) {
            scanDir(fullPath);
          } else if (entry.isFile()) {
            try {
              const stats = fs.statSync(fullPath);
              
              // 只监控JSON和JSONL文件
              if (entry.name.endsWith('.json') || entry.name.endsWith('.jsonl')) {
                let lines = 0;
                let entries = 0;
                
                // 计算行数/条目数
                try {
                  const content = fs.readFileSync(fullPath, 'utf-8');
                  if (entry.name.endsWith('.jsonl')) {
                    lines = content.split('\n').filter(l => l.trim()).length;
                  } else {
                    const parsed = JSON.parse(content);
                    entries = Array.isArray(parsed) ? parsed.length : 1;
                  }
                } catch (parseErr) {
                  // 解析失败，跳过
                }
                
                files.push({
                  path: fullPath,
                  name: entry.name,
                  size: stats.size,
                  lines,
                  entries,
                  modified: stats.mtimeMs
                });
                
                totalSize += stats.size;
                totalFiles++;
              }
            } catch (statErr) {
              // 无法访问文件，跳过
            }
          }
        }
      } catch (err) {
        this.logger.debug('Failed to scan directory:', dir, err.message);
      }
    };
    
    scanDir(watchPath);
    
    return { files, totalSize, totalFiles };
  }

  /**
   * 采集内存数据
   * @returns {object} 内存数据
   */
  _collectMemoryData() {
    // 获取进程内存使用
    const processMemory = process.memoryUsage();
    
    // 获取系统内存
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const usedMem = totalMem - freeMem;
    
    return {
      process: {
        rss: processMemory.rss,           // 常驻内存集
        heapTotal: processMemory.heapTotal, // 堆总量
        heapUsed: processMemory.heapUsed,   // 堆使用
        external: processMemory.external    // 外部内存
      },
      system: {
        total: totalMem,
        free: freeMem,
        used: usedMem,
        percent: (usedMem / totalMem) * 100
      }
    };
  }

  /**
   * 检查阈值
   * @param {object} snapshot - 快照数据
   */
  _checkThresholds(snapshot) {
    // 发射状态更新事件
    this.emit('status', this.getStatus());
  }

  /**
   * 获取当前状态
   * @returns {object} 状态对象
   */
  getStatus() {
    return {
      running: this.running,
      path: this.config.watchPath,
      interval: this.config.interval,
      currentSize: this.lastSnapshot?.totalSize || 0,
      currentFiles: this.lastSnapshot?.totalFiles || 0,
      growthRate: this.lastSnapshot?.growthRate || 0,
      memory: this.lastSnapshot?.memory || null,
      historyLength: this.history.length
    };
  }

  /**
   * 获取趋势数据
   * @param {number} minutes - 过去N分钟
   * @returns {object} 趋势数据
   */
  getTrend(minutes = 30) {
    const cutoff = Date.now() - (minutes * 60 * 1000);
    const recentHistory = this.history.filter(h => h.timestamp >= cutoff);
    
    if (recentHistory.length < 2) {
      return {
        available: false,
        reason: 'Not enough data points'
      };
    }
    
    // 计算平均增长率
    const totalGrowthRate = recentHistory.reduce((sum, h) => sum + h.growthRate, 0);
    const avgGrowthRate = totalGrowthRate / recentHistory.length;
    
    // 计算大小变化
    const firstSize = recentHistory[0].totalSize;
    const lastSize = recentHistory[recentHistory.length - 1].totalSize;
    const sizeChange = lastSize - firstSize;
    const sizeChangePercent = firstSize > 0 ? (sizeChange / firstSize) * 100 : 0;
    
    // 计算文件数量变化
    const firstFiles = recentHistory[0].totalFiles;
    const lastFiles = recentHistory[recentHistory.length - 1].totalFiles;
    const filesChange = lastFiles - firstFiles;
    
    // 判断趋势方向
    let direction = 'stable';
    if (avgGrowthRate > 1024) { // > 1KB/min
      direction = 'growing';
    } else if (avgGrowthRate < -1024) { // < -1KB/min
      direction = 'shrinking';
    }
    
    return {
      available: true,
      minutes,
      samples: recentHistory.length,
      avgGrowthRate,         // bytes/min
      sizeChange,            // bytes
      sizeChangePercent,     // percent
      filesChange,           // count
      direction,
      startSize: firstSize,
      endSize: lastSize,
      startFiles: firstFiles,
      endFiles: lastFiles
    };
  }

  /**
   * 获取最新快照
   * @returns {object|null} 快照数据
   */
  getLatestSnapshot() {
    return this.lastSnapshot;
  }

  /**
   * 获取历史数据
   * @param {number} count - 数量
   * @returns {array} 历史数据
   */
  getHistory(count = 10) {
    return this.history.slice(-count);
  }

  /**
   * 清空历史数据
   */
  clearHistory() {
    this.history = [];
    this.lastSnapshot = null;
  }
}

module.exports = Monitor;