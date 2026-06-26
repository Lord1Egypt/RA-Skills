/**
 * 清理模块
 * 负责清理旧备份文件
 * v1.0.2 - 只处理本 skill 产生的备份文件
 */

const fs = require('fs-extra');
const path = require('path');
const dayjs = require('dayjs');
const { info, warn, error, debug } = require('./logger');

/**
 * 创建清理器实例
 */
class Cleaner {
  constructor(config) {
    this.config = config;
  }

  /**
   * 执行清理
   */
  async execute() {
    try {
      if (!this.config.retention.enabled) {
        await info('Cleaner', '保留策略未启用，跳过清理');
        return { deleted: 0, kept: 0, skipped: true };
      }
      
      await info('Cleaner', '开始清理旧备份...');
      
      // 获取本 skill 的备份文件
      const backups = await this.getBackupFiles();
      
      if (backups.length === 0) {
        await info('Cleaner', '没有找到本 skill 的备份文件');
        return { deleted: 0, kept: 0, skipped: false };
      }
      
      await info('Cleaner', `当前备份数: ${backups.length} 个`);
      
      // 选择要删除的文件
      const toDelete = this.selectToDelete(backups);
      
      if (toDelete.length === 0) {
        await info('Cleaner', '无需清理，当前备份数未超出保留策略');
        return { deleted: 0, kept: backups.length, skipped: false };
      }
      
      await info('Cleaner', `准备删除 ${toDelete.length} 个旧备份`);
      
      // 执行删除
      let deletedCount = 0;
      for (const file of toDelete) {
        try {
          await fs.remove(file.path);
          deletedCount++;
          await debug('Cleaner', `已删除: ${file.name}`);
        } catch (err) {
          await warn('Cleaner', `删除失败 ${file.name}: ${err.message}`);
        }
      }
      
      const keptCount = backups.length - deletedCount;
      
      await info('Cleaner', `清理完成: 删除 ${deletedCount} 个，保留 ${keptCount} 个`);
      
      return {
        deleted: deletedCount,
        kept: keptCount,
        skipped: false
      };
    } catch (err) {
      await error('Cleaner', `清理失败: ${err.message}`);
      return { deleted: 0, kept: 0, error: err.message };
    }
  }

  /**
   * 获取本 skill 的备份文件
   * 只返回文件名以配置的前缀开头的备份文件
   */
  async getBackupFiles() {
    try {
      const outputDir = this.config.output.path;
      const prefix = this.config.output.naming.prefix || 'auto-backup-openclaw-user-data';
      
      if (!(await fs.pathExists(outputDir))) {
        return [];
      }
      
      const files = await fs.readdir(outputDir);
      const backups = [];
      
      for (const file of files) {
        // 只处理 .zip 文件
        if (!file.endsWith('.zip')) continue;
        
        // 只处理以本 skill 前缀开头的文件
        if (!file.startsWith(prefix)) continue;
        
        const filePath = path.join(outputDir, file);
        
        try {
          const stats = await fs.stat(filePath);
          
          backups.push({
            name: file,
            path: filePath,
            size: stats.size,
            modifiedTime: stats.mtime.getTime(),
            modifiedDate: dayjs(stats.mtime).format('YYYY-MM-DD HH:mm:ss')
          });
        } catch (err) {
          // 忽略无法访问的文件
        }
      }
      
      // 按修改时间排序（最新的在前）
      backups.sort((a, b) => b.modifiedTime - a.modifiedTime);
      
      return backups;
    } catch (err) {
      await error('Cleaner', `获取备份文件列表失败: ${err.message}`);
      return [];
    }
  }

  /**
   * 选择要删除的备份
   */
  selectToDelete(backups) {
    if (this.config.retention.mode === 'days') {
      return this.selectByDays(backups);
    } else {
      return this.selectByCount(backups);
    }
  }

  /**
   * 按天数选择
   */
  selectByDays(backups) {
    const cutoff = Date.now() - this.config.retention.days * 24 * 60 * 60 * 1000;
    
    return backups.filter(b => b.modifiedTime < cutoff);
  }

  /**
   * 按份数选择
   */
  selectByCount(backups) {
    const keepCount = this.config.retention.count;
    
    // 已经按时间排序，保留最新的 N 个，删除其余的
    if (backups.length <= keepCount) {
      return [];
    }
    
    return backups.slice(keepCount);
  }

  /**
   * 获取清理预览
   */
  async getPreview() {
    const backups = await this.getBackupFiles();
    const toDelete = this.selectToDelete(backups);
    
    return {
      total: backups.length,
      toDeleteCount: toDelete.length,
      toKeepCount: backups.length - toDelete.length,
      toDeleteFiles: toDelete.map(f => ({
        name: f.name,
        size: this.formatSize(f.size),
        date: f.modifiedDate
      })),
      policy: {
        mode: this.config.retention.mode,
        days: this.config.retention.days,
        count: this.config.retention.count
      }
    };
  }

  /**
   * 格式化文件大小
   */
  formatSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }

  /**
   * 获取备份统计
   */
  async getStats() {
    const backups = await this.getBackupFiles();
    
    const totalSize = backups.reduce((sum, b) => sum + b.size, 0);
    
    return {
      count: backups.length,
      totalSize: this.formatSize(totalSize),
      totalSizeBytes: totalSize,
      oldestBackup: backups.length > 0 ? backups[backups.length - 1].modifiedDate : null,
      newestBackup: backups.length > 0 ? backups[0].modifiedDate : null,
      files: backups.slice(0, 20).map(b => ({
        name: b.name,
        size: this.formatSize(b.size),
        date: b.modifiedDate
      }))
    };
  }
}

module.exports = { Cleaner };