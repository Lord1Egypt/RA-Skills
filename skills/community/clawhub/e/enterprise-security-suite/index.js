/**
 * Enterprise Security - 主入口
 */

const confirm = require('./modules/confirm');
const backup = require('./modules/backup');
const changelog = require('./modules/changelog');
const rollback = require('./modules/rollback');
const securityCheck = require('./modules/security-check');

module.exports = {
  // 高危操作确认
  confirmHighRisk: confirm.confirmHighRisk,
  isHighRisk: confirm.isHighRisk,
  
  // 自动备份
  autoBackup: backup.autoBackup,
  needsBackup: backup.needsBackup,
  
  // 变更日志
  logChange: changelog.logChange,
  
  // 回滚机制
  rollback: rollback.rollback,
  findBackups: rollback.findBackups,
  
  // 技能安检
  checkSkill: securityCheck.securityCheck,
  generateReport: securityCheck.generateReport,
  
  // 常量
  HIGH_RISK_OPERATIONS: confirm.HIGH_RISK_OPERATIONS,
  RISK_LEVELS: securityCheck.RISK_LEVELS
};

console.log('🛡️ Enterprise Security v1.0.0 已加载');
