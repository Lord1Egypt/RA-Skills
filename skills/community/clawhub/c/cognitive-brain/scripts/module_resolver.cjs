/**
 * Cognitive Brain - 模块解析器
 * 解决脚本在不同目录运行时的模块解析问题
 */

const path = require('path');

function resolveModule(moduleName) {
  const skillDir = path.join(__dirname, '..');
  const modulePath = path.join(skillDir, 'node_modules', moduleName);
  
  try {
    return require(modulePath);
  } catch (e) {
    // 回退到全局 require
    return require(moduleName);
  }
}

function resolveConfig() {
  const skillDir = path.join(__dirname, '..');
  const configPath = path.join(skillDir, 'config.json');
  return JSON.parse(require('fs').readFileSync(configPath, 'utf8'));
}

module.exports = { resolveModule, resolveConfig };
