/**
 * 入口模块
 * 完整导出所有接口，确保兼容性
 * v1.1.0 - 脚本入口改进，消除"可疑技能"标记
 */

const { BackupManager, initBackupManager, OPENCLAW_ROOT } = require('./scripts/backup');
const { CLI, runCommand } = require('./scripts/cli');  // ← 关键：必须导出runCommand
const {
  loadConfig,
  saveConfig,
  resetConfig,
  getConfigPaths,
  detectWorkspaces
} = require('./scripts/config');

/**
 * 模块导出
 * OpenClaw通过此接口调用技能功能
 */
module.exports = {
  // 核心类（向后兼容）
  BackupManager,
  OPENCLAW_ROOT,

  // 命令执行接口（新增，关键）
  CLI,
  runCommand,  // ← OpenClaw通过此函数调用命令

  // 初始化函数
  initBackupManager,

  // 配置管理函数
  loadConfig,
  saveConfig,
  resetConfig,
  getConfigPaths,
  detectWorkspaces,  // ← 新增：工作空间动态检测函数

  // 版本信息
  version: '1.1.0',
  name: 'auto-backup-openclaw-user-data'
};