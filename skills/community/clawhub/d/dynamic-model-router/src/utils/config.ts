/**
 * 动态模型路由技能 - 配置管理
 */

import fs from 'fs';
import path from 'path';
import { RouterError } from '../core/types.js';
import { validateConfig, mergeConfig } from './index.js';
import { RouterLogger } from './logger.js';
import { CONSTANTS } from '../core/types.js';
import type { RouterConfig } from '../core/types.js';

const logger = new RouterLogger({ module: 'config' });

/**
 * 配置管理器
 */
export class ConfigManager {
  private config: RouterConfig;
  private configPath: string;
  private configFile: string;
  private lastModified: number = 0;
  
  constructor(configDir?: string) {
    // 确定配置目录
    const baseDir = configDir || 
      path.join(process.env.HOME || process.env.USERPROFILE || '.', '.openclaw');
    
    this.configPath = path.join(baseDir, 'dynamic-router');
    this.configFile = path.join(this.configPath, 'config.json');
    
    // 确保配置目录存在
    this.ensureConfigDir();
    
    // 加载配置
    this.config = this.loadConfig();
    
    logger.info('配置管理器初始化完成', {
      configPath: this.configPath,
      configFile: this.configFile,
    });
  }
  
  /**
   * 确保配置目录存在
   */
  private ensureConfigDir(): void {
    try {
      if (!fs.existsSync(this.configPath)) {
        fs.mkdirSync(this.configPath, { recursive: true });
        logger.debug('创建配置目录', { path: this.configPath });
      }
    } catch (error) {
      logger.error('创建配置目录失败', error as Error, { path: this.configPath });
      throw new RouterError(
        `无法创建配置目录: ${this.configPath}`,
        'CONFIG_DIR_ERROR',
        { error: (error as Error).message }
      );
    }
  }
  
  /**
   * 加载配置
   */
  private loadConfig(): RouterConfig {
    try {
      // 检查配置文件是否存在
      if (!fs.existsSync(this.configFile)) {
        logger.info('配置文件不存在，使用默认配置', { file: this.configFile });
        return this.createDefaultConfig();
      }
      
      // 读取配置文件
      const configContent = fs.readFileSync(this.configFile, 'utf-8');
      const userConfig = JSON.parse(configContent);
      
      // 记录最后修改时间
      const stats = fs.statSync(this.configFile);
      this.lastModified = stats.mtimeMs;
      
      // 合并配置
      const mergedConfig = mergeConfig(userConfig, CONSTANTS.DEFAULT_CONFIG);
      
      // 验证配置
      validateConfig(mergedConfig);
      
      logger.info('配置文件加载成功', { file: this.configFile });
      return mergedConfig;
      
    } catch (error) {
      logger.error('加载配置文件失败', error as Error, { file: this.configFile });
      
      // 如果是JSON解析错误，尝试修复或使用默认配置
      if (error instanceof SyntaxError) {
        logger.warn('配置文件JSON格式错误，使用默认配置', { error: error.message });
        return this.createDefaultConfig();
      }
      
      // 其他错误，抛出
      throw new RouterError(
        `加载配置文件失败: ${(error as Error).message}`,
        'CONFIG_LOAD_ERROR',
        { file: this.configFile }
      );
    }
  }
  
  /**
   * 创建默认配置
   */
  private createDefaultConfig(): RouterConfig {
    const defaultConfig = { ...CONSTANTS.DEFAULT_CONFIG };
    
    // 保存默认配置到文件
    this.saveConfig(defaultConfig);
    
    return defaultConfig;
  }
  
  /**
   * 保存配置
   */
  private saveConfig(config: RouterConfig): void {
    try {
      const configContent = JSON.stringify(config, null, 2);
      fs.writeFileSync(this.configFile, configContent, 'utf-8');
      
      // 更新最后修改时间
      const stats = fs.statSync(this.configFile);
      this.lastModified = stats.mtimeMs;
      
      logger.info('配置文件保存成功', { file: this.configFile });
    } catch (error) {
      logger.error('保存配置文件失败', error as Error, { file: this.configFile });
      throw new RouterError(
        `保存配置文件失败: ${(error as Error).message}`,
        'CONFIG_SAVE_ERROR',
        { file: this.configFile }
      );
    }
  }
  
  /**
   * 获取配置
   */
  getConfig(): RouterConfig {
    // 检查配置文件是否被外部修改
    if (fs.existsSync(this.configFile)) {
      const stats = fs.statSync(this.configFile);
      if (stats.mtimeMs > this.lastModified + 1000) { // 1秒缓冲
        logger.debug('检测到配置文件变更，重新加载');
        this.config = this.loadConfig();
      }
    }
    
    return { ...this.config }; // 返回副本，防止直接修改
  }
  
  /**
   * 更新配置
   */
  updateConfig(updates: Partial<RouterConfig>): RouterConfig {
    logger.info('更新配置', { updates });
    
    // 合并更新
    const newConfig = mergeConfig(updates, this.config);
    
    // 验证新配置
    validateConfig(newConfig);
    
    // 保存配置
    this.saveConfig(newConfig);
    
    // 更新内存中的配置
    this.config = newConfig;
    
    // 记录配置变更
    Object.keys(updates).forEach(key => {
      const oldValue = (this.config as any)[key];
      const newValue = (updates as any)[key];
      
      if (JSON.stringify(oldValue) !== JSON.stringify(newValue)) {
        logger.logConfigChange(
          key,
          oldValue,
          newValue,
          '用户手动更新'
        );
      }
    });
    
    return this.getConfig();
  }
  
  /**
   * 重置配置为默认值
   */
  resetConfig(): RouterConfig {
    logger.info('重置配置为默认值');
    this.config = this.createDefaultConfig();
    return this.getConfig();
  }
  
  /**
   * 获取配置路径
   */
  getConfigPath(): string {
    return this.configPath;
  }
  
  /**
   * 获取配置文件路径
   */
  getConfigFilePath(): string {
    return this.configFile;
  }
  
  /**
   * 导出当前配置
   */
  exportConfig(): string {
    return JSON.stringify(this.config, null, 2);
  }
  
  /**
   * 导入配置
   */
  importConfig(configJson: string): RouterConfig {
    try {
      const importedConfig = JSON.parse(configJson);
      return this.updateConfig(importedConfig);
    } catch (error) {
      logger.error('导入配置失败', error as Error);
      throw new RouterError(
        `导入配置失败: ${(error as Error).message}`,
        'CONFIG_IMPORT_ERROR'
      );
    }
  }
  
  /**
   * 备份当前配置
   */
  backupConfig(): string {
    const backupFile = path.join(
      this.configPath,
      `config.backup.${Date.now()}.json`
    );
    
    try {
      const configContent = this.exportConfig();
      fs.writeFileSync(backupFile, configContent, 'utf-8');
      
      logger.info('配置备份创建成功', { backupFile });
      return backupFile;
    } catch (error) {
      logger.error('配置备份失败', error as Error, { backupFile });
      throw new RouterError(
        `配置备份失败: ${(error as Error).message}`,
        'CONFIG_BACKUP_ERROR',
        { backupFile }
      );
    }
  }
  
  /**
   * 从备份恢复配置
   */
  restoreFromBackup(backupFile: string): RouterConfig {
    try {
      if (!fs.existsSync(backupFile)) {
        throw new Error(`备份文件不存在: ${backupFile}`);
      }
      
      const backupContent = fs.readFileSync(backupFile, 'utf-8');
      const backupConfig = JSON.parse(backupContent);
      
      logger.info('从备份恢复配置', { backupFile });
      return this.updateConfig(backupConfig);
    } catch (error) {
      logger.error('从备份恢复配置失败', error as Error, { backupFile });
      throw new RouterError(
        `从备份恢复配置失败: ${(error as Error).message}`,
        'CONFIG_RESTORE_ERROR',
        { backupFile }
      );
    }
  }
  
  /**
   * 列出所有备份文件
   */
  listBackups(): string[] {
    try {
      if (!fs.existsSync(this.configPath)) {
        return [];
      }
      
      const files = fs.readdirSync(this.configPath);
      return files
        .filter(file => file.startsWith('config.backup.') && file.endsWith('.json'))
        .map(file => path.join(this.configPath, file))
        .sort((a, b) => {
          // 按时间排序，最新的在前面
          const timeA = this.extractBackupTime(a);
          const timeB = this.extractBackupTime(b);
          return timeB - timeA;
        });
    } catch (error) {
      logger.error('列出备份文件失败', error as Error);
      return [];
    }
  }
  
  /**
   * 从备份文件名中提取时间戳
   */
  private extractBackupTime(filePath: string): number {
    const fileName = path.basename(filePath);
    const match = fileName.match(/config\.backup\.(\d+)\.json/);
    if (match && match[1]) {
      return parseInt(match[1], 10);
    }
    return 0;
  }
  
  /**
   * 清理旧的备份文件
   */
  cleanupOldBackups(maxBackups = 10): void {
    try {
      const backups = this.listBackups();
      
      if (backups.length <= maxBackups) {
        return;
      }
      
      const toDelete = backups.slice(maxBackups);
      toDelete.forEach(backupFile => {
        try {
          fs.unlinkSync(backupFile);
          logger.debug('删除旧备份文件', { backupFile });
        } catch (error) {
          logger.warn('删除备份文件失败', { backupFile, error: (error as Error).message });
        }
      });
      
      logger.info('清理旧备份文件完成', {
        totalBackups: backups.length,
        deleted: toDelete.length,
        remaining: maxBackups,
      });
    } catch (error) {
      logger.error('清理备份文件失败', error as Error);
    }
  }
}

// 默认配置管理器实例
let defaultConfigManager: ConfigManager | null = null;

/**
 * 获取默认配置管理器
 */
export function getConfigManager(configDir?: string): ConfigManager {
  if (!defaultConfigManager) {
    defaultConfigManager = new ConfigManager(configDir);
  }
  return defaultConfigManager;
}

/**
 * 重新初始化配置管理器
 */
export function reinitializeConfigManager(configDir?: string): ConfigManager {
  defaultConfigManager = new ConfigManager(configDir);
  return defaultConfigManager;
}

/**
 * 环境变量配置覆盖
 */
export function applyEnvOverrides(config: RouterConfig): RouterConfig {
  const envConfig: Partial<RouterConfig> = {};
  
  // 从环境变量读取配置覆盖
  if (process.env.DYNAMIC_ROUTER_STRATEGY) {
    const strategy = process.env.DYNAMIC_ROUTER_STRATEGY;
    if (strategy === 'cost' || strategy === 'quality' || strategy === 'balanced') {
      envConfig.defaultStrategy = strategy;
      logger.debug('从环境变量设置默认策略', { strategy });
    }
  }
  
  if (process.env.LEARNING_ENABLED !== undefined) {
    envConfig.learningEnabled = process.env.LEARNING_ENABLED.toLowerCase() === 'true';
    logger.debug('从环境变量设置学习启用', { enabled: envConfig.learningEnabled });
  }
  
  if (process.env.DATA_DIR) {
    // DATA_DIR环境变量由ConfigManager在构造时使用
    logger.debug('从环境变量设置数据目录', { dataDir: process.env.DATA_DIR });
  }
  
  // 应用覆盖
  if (Object.keys(envConfig).length > 0) {
    const mergedConfig = mergeConfig(envConfig, config);
    logger.info('应用环境变量配置覆盖', { overrides: envConfig });
    return mergedConfig;
  }
  
  return config;
}