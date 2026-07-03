/**
 * ============================================
 * 类型: 核心框架
 * 模块: utils.logging
 * 说明: 日志配置
 * 修改建议: 如需扩展，修改日志格式或添加新的handler
 * ============================================

const fs = require('fs');
const path = require('path');

function setupLogging(level = 'info') {
  const logDir = path.join(process.cwd(), 'logs');
  if (!fs.existsSync(logDir)) {
    fs.mkdirSync(logDir, { recursive: true });
  }
  
  // 简单的日志实现
  const levels = {
    debug: 0,
    info: 1,
    warn: 2,
    error: 3
  };
  
  const currentLevel = levels[level] || 1;
  
  return {
    debug: (...args) => {
      if (currentLevel <= 0) {
        console.log(`[DEBUG] ${new Date().toISOString()} -`, ...args);
      }
    },
    info: (...args) => {
      if (currentLevel <= 1) {
        console.log(`[INFO] ${new Date().toISOString()} -`, ...args);
      }
    },
    warn: (...args) => {
      if (currentLevel <= 2) {
        console.warn(`[WARN] ${new Date().toISOString()} -`, ...args);
      }
    },
    error: (...args) => {
      if (currentLevel <= 3) {
        console.error(`[ERROR] ${new Date().toISOString()} -`, ...args);
      }
    }
  };
}

module.exports = { setupLogging };
