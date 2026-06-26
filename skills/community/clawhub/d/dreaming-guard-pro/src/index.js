/**
 * Dreaming Guard Pro - Entry Point
 * 
 * Phase 1 基础模块导出
 * Phase 2 核心功能模块导出
 * Phase 3 决策引擎导出
 * Phase 4 保护与自愈模块导出
 */

const Logger = require('./logger');
const Config = require('./config');
const StateManager = require('./state-manager');
const Monitor = require('./monitor');
const Archiver = require('./archiver');
const Compressor = require('./compressor');
const Decision = require('./decision');
const Protector = require('./protector');
const Healer = require('./healer');

module.exports = {
  // Phase 1 基础模块
  Logger,
  Config,
  StateManager,
  
  // Phase 2 核心功能模块
  Monitor,
  Archiver,
  Compressor,
  
  // Phase 3 决策引擎
  Decision,
  
  // Phase 4 保护与自愈模块
  Protector,
  Healer,
  
  // 版本信息
  version: '1.0.0',
  
  // 快捷创建实例
  createLogger: (options) => new Logger(options),
  createConfig: (path) => new Config(path),
  createStateManager: (options) => new StateManager(options),
  createMonitor: (options) => new Monitor(options),
  createArchiver: (options) => new Archiver(options),
  createCompressor: (options) => new Compressor(options),
  createDecision: (options) => new Decision(options),
  createProtector: (options) => new Protector(options),
  createHealer: (options) => new Healer(options)
};