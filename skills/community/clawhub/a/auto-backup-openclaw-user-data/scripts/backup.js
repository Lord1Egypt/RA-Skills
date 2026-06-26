/**
 * 主备份模块
 * 负责协调整个备份流程
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const dayjs = require('dayjs');

const { loadConfig, saveConfig, ensureConfigDir, BACKUPS_DIR } = require('./config');
const { Compressor } = require('./compressor');
const { Scheduler, describeCron } = require('./scheduler');
const { Cleaner } = require('./cleaner');
const { Notifier } = require('./notifier');
const { info, warn, error, debug, cleanOldLogs } = require('./logger');

// OpenClaw 根目录
const OPENCLAW_ROOT = path.join(os.homedir(), '.openclaw');

/**
 * 创建备份管理器实例
 */
class BackupManager {
  constructor(config) {
    this.config = config;
    this.compressor = new Compressor(config);
    this.scheduler = new Scheduler(config);
    this.cleaner = new Cleaner(config);
    this.notifier = new Notifier(config);
    this.isRunning = false;
  }

  /**
   * 执行备份
   * @param {Object} options 选项
   * @returns {Promise<Object>} 备份结果
   */
  async execute(options = {}) {
    const startTime = Date.now();
    const result = {
      success: false,
      filesTotal: 0,
      filesSkipped: 0,
      sizeBytes: 0,
      outputPath: null,
      errors: [],
      duration: 0,
      timestamp: new Date().toISOString()
    };

    try {
      // 检查是否正在运行
      if (this.isRunning) {
        result.errors.push('备份任务正在执行中，请稍后再试');
        return result;
      }

      this.isRunning = true;
      
      await info('Backup', '='.repeat(50));
      await info('Backup', '开始执行备份任务');
      await info('Backup', '='.repeat(50));

      // 1. 准备备份目标
      const targets = await this.prepareTargets(options);
      await info('Backup', `备份目标: ${targets.length} 个目录`);
      
      // 2. 收集文件列表
      await info('Backup', '正在收集文件列表...');
      const files = await this.collectFiles(targets);
      result.filesTotal = files.length;
      await info('Backup', `共收集到 ${files.length} 个文件`);
      
      if (files.length === 0) {
        result.errors.push('没有找到需要备份的文件');
        this.isRunning = false;
        return result;
      }
      
      // 3. 执行压缩
      await info('Backup', '正在压缩文件...');
      const zipPath = await this.compressor.compress(files, this.config.output);
      result.outputPath = zipPath;
      
      // 4. 获取文件大小
      const stats = await fs.stat(zipPath);
      result.sizeBytes = stats.size;
      
      await info('Backup', `备份文件: ${path.basename(zipPath)}`);
      await info('Backup', `文件大小: ${this.formatSize(stats.size)}`);
      
      // 5. 记录执行时间
      await this.scheduler.recordRun();
      
      // 6. 执行保留策略清理
      if (this.config.retention.enabled) {
        await info('Backup', '执行保留策略清理...');
        const cleanResult = await this.cleaner.execute();
        result.cleanResult = cleanResult;
      }
      
      // 7. 清理旧日志
      await cleanOldLogs(this.config.logging.maxSize, this.config.logging.maxFiles);
      
      result.success = true;
      result.duration = Date.now() - startTime;
      
      await info('Backup', '='.repeat(50));
      await info('Backup', `备份完成！耗时: ${this.formatDuration(result.duration)}`);
      await info('Backup', '='.repeat(50));
      
      // 8. 发送成功通知
      await this.notifier.notifySuccess(result);
      
    } catch (err) {
      result.errors.push(err.message);
      result.duration = Date.now() - startTime;
      
      await error('Backup', `备份失败: ${err.message}`);
      await error('Backup', err.stack);
      
      // 发送失败通知
      await this.notifier.notifyFailure(result);
    } finally {
      this.isRunning = false;
    }

    return result;
  }

  /**
   * 准备备份目标路径
   */
  async prepareTargets(options) {
    const openclawRoot = OPENCLAW_ROOT;
    const targets = [];
    
    // 检查备份模式
    if (this.config.backup.mode === 'full' || options.full) {
      // 全量备份
      targets.push({
        path: openclawRoot,
        name: '.openclaw',
        isRoot: true
      });
    } else {
      // 选择性备份
      const targetNames = options.targets || this.config.backup.targets || [];
      
      for (const name of targetNames) {
        const targetPath = path.join(openclawRoot, name);
        
        if (await fs.pathExists(targetPath)) {
          targets.push({
            path: targetPath,
            name: name,
            isRoot: false
          });
        } else {
          await warn('Backup', `目标目录不存在，跳过: ${name}`);
        }
      }
    }
    
    return targets;
  }

  /**
   * 收集待备份文件
   */
  async collectFiles(targets) {
    const allFiles = [];
    const exclude = this.config.backup.exclude || [];
    const excludePatterns = this.config.backup.excludePatterns || [];
    
    for (const target of targets) {
      await debug('Backup', `扫描目录: ${target.name}`);
      
      const files = await this.walkDirectory(
        target.path,
        target.isRoot ? exclude : [],
        excludePatterns,
        target.isRoot ? '' : target.name
      );
      
      allFiles.push(...files);
    }
    
    return allFiles;
  }

  /**
   * 遍历目录收集文件
   */
  async walkDirectory(dirPath, excludeDirs, excludePatterns, relativeBase) {
    const files = [];
    const openclawRoot = OPENCLAW_ROOT;
    
    async function walk(currentPath, self) {
      try {
        const entries = await fs.readdir(currentPath, { withFileTypes: true });
        
        for (const entry of entries) {
          const fullPath = path.join(currentPath, entry.name);
          const relativePath = relativeBase 
            ? path.join(relativeBase, path.relative(dirPath, fullPath))
            : path.relative(openclawRoot, fullPath);
          
          // 检查是否在排除目录中
          if (excludeDirs.includes(entry.name)) {
            continue;
          }
          
          // 检查是否匹配排除模式
          if (excludePatterns.some(pattern => this.matchPattern(entry.name, pattern))) {
            continue;
          }
          
          if (entry.isDirectory()) {
            await walk.call(self, fullPath, self);
          } else if (entry.isFile()) {
            // 检查文件是否可读
            try {
              await fs.access(fullPath, fs.constants.R_OK);
              files.push({
                path: fullPath,
                relativePath: relativePath
              });
            } catch (accessErr) {
              if (accessErr.code === 'EBUSY') {
                // 文件被占用，跳过
                continue;
              }
            }
          }
        }
      } catch (err) {
        // 忽略无法访问的目录
      }
    }
    
    await walk.call(this, dirPath, this);
    return files;
  }

  /**
   * 简单的模式匹配
   */
  matchPattern(filename, pattern) {
    const regex = new RegExp('^' + pattern
      .replace(/\./g, '\\.')
      .replace(/\*/g, '.*')
      .replace(/\?/g, '.') + '$');
    
    return regex.test(filename);
  }

  /**
   * 格式化文件大小
   */
  formatSize(bytes) {
    if (!bytes || bytes === 0) return '0 B';
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }

  /**
   * 格式化执行时长
   */
  formatDuration(ms) {
    if (!ms) return '0ms';
    if (ms < 1000) return `${ms}ms`;
    if (ms < 60000) return `${(ms / 1000).toFixed(1)} 秒`;
    return `${Math.floor(ms / 60000)} 分 ${Math.floor((ms % 60000) / 1000)} 秒`;
  }

  /**
   * 获取备份状态
   */
  async getStatus() {
    const schedulerStatus = this.scheduler.getStatus();
    const backupStats = await this.cleaner.getStats();
    
    return {
      schedule: schedulerStatus,
      backups: backupStats,
      config: {
        mode: this.config.backup.mode,
        targets: this.config.backup.targets,
        retention: this.config.retention,
        notification: this.config.notification.channels
      }
    };
  }

  /**
   * 检查是否应该执行备份（HEARTBEAT 调用）
   */
  async checkAndRun() {
    const shouldRun = await this.scheduler.shouldRun();
    
    if (shouldRun) {
      await info('Backup', 'HEARTBEAT 触发定时备份');
      return this.execute();
    }
    
    return null;
  }
}

/**
 * 初始化备份管理器
 */
async function initBackupManager() {
  const config = await loadConfig();
  return new BackupManager(config);
}

module.exports = {
  BackupManager,
  initBackupManager,
  OPENCLAW_ROOT
};