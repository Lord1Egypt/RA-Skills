/**
 * templates/index.js — 模板管理
 *
 * 职责：管理 HTML 模板的加载、保存、版本历史和回滚
 *
 * 模板路径优先级：
 *   1. workspace/templates/{name}_current.html  — 用户当前版本
 *   2. templates/{name}_template.html           — 技能基线模板
 */
const fs = require('fs');
const path = require('path');
const config = require('../core/config.js');

// 模板目录配置
const TEMPLATE_DIRS = {
  base: path.join(__dirname, '../../templates'),
  user: path.join(config.workspace, 'templates'),
  history: path.join(config.workspace, 'templates', 'history')
};

// 确保目录存在
function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

// 初始化目录
function initDirectories() {
  Object.values(TEMPLATE_DIRS).forEach(dir => ensureDir(dir));
}

// 加载模板
function loadTemplate(name, options = {}) {
  const { version = 'current' } = options;
  
  if (version === 'current' && fs.existsSync(path.join(TEMPLATE_DIRS.user, `${name}_current.html`))) {
    return fs.readFileSync(path.join(TEMPLATE_DIRS.user, `${name}_current.html`), 'utf-8');
  }
  
  if (fs.existsSync(path.join(TEMPLATE_DIRS.base, `${name}_template.html`))) {
    return fs.readFileSync(path.join(TEMPLATE_DIRS.base, `${name}_template.html`), 'utf-8');
  }
  
  throw new Error(`模板 ${name} 不存在`);
}

// 保存模板
function saveTemplate(name, content, options = {}) {
  const { version = 'current', comment = '' } = options;
  
  initDirectories();
  
  // 保存当前版本
  const currentPath = path.join(TEMPLATE_DIRS.user, `${name}_current.html`);
  fs.writeFileSync(currentPath, content, 'utf-8');
  
  // 保存历史版本
  if (version === 'current') {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const historyPath = path.join(TEMPLATE_DIRS.history, `${name}_${timestamp}.html`);
    fs.writeFileSync(historyPath, content, 'utf-8');
    
    // 保存版本信息
    const versionInfo = {
      timestamp,
      comment,
      path: path.basename(historyPath)
    };
    const versionFile = path.join(TEMPLATE_DIRS.history, `${name}_versions.json`);
    let versions = [];
    if (fs.existsSync(versionFile)) {
      versions = JSON.parse(fs.readFileSync(versionFile, 'utf-8'));
    }
    versions.unshift(versionInfo);
    // 只保留最近 10 个版本
    if (versions.length > 10) {
      versions = versions.slice(0, 10);
    }
    fs.writeFileSync(versionFile, JSON.stringify(versions, null, 2), 'utf-8');
  }
  
  return currentPath;
}

// 列出模板版本
function listTemplateVersions(name) {
  const versionFile = path.join(TEMPLATE_DIRS.history, `${name}_versions.json`);
  if (fs.existsSync(versionFile)) {
    return JSON.parse(fs.readFileSync(versionFile, 'utf-8'));
  }
  return [];
}

// 回滚模板
function rollbackTemplate(name, version) {
  const versionFile = path.join(TEMPLATE_DIRS.history, `${name}_versions.json`);
  if (!fs.existsSync(versionFile)) {
    throw new Error(`模板 ${name} 没有历史版本`);
  }
  
  const versions = JSON.parse(fs.readFileSync(versionFile, 'utf-8'));
  const targetVersion = versions.find(v => v.timestamp === version || v.path === version);
  
  if (!targetVersion) {
    throw new Error(`版本 ${version} 不存在`);
  }
  
  const historyPath = path.join(TEMPLATE_DIRS.history, targetVersion.path);
  if (!fs.existsSync(historyPath)) {
    throw new Error(`版本文件不存在: ${targetVersion.path}`);
  }
  
  const content = fs.readFileSync(historyPath, 'utf-8');
  return saveTemplate(name, content, { comment: `回滚到版本 ${version}` });
}

// 验证模板
function validateTemplate(content) {
  // 检查必需的占位符
  const requiredPlaceholders = ['{{PAGE_TITLE}}', '{{CHART_CONFIG}}', '{{ENCRYPTED_SQL}}'];
  for (const placeholder of requiredPlaceholders) {
    if (!content.includes(placeholder)) {
      throw new Error(`模板缺少必需的占位符: ${placeholder}`);
    }
  }
  
  // 检查 HTML 语法
  // 这里可以添加更复杂的 HTML 验证逻辑
  
  return true;
}

initDirectories();

module.exports = {
  loadTemplate,
  saveTemplate,
  listTemplateVersions,
  rollbackTemplate,
  validateTemplate,
  TEMPLATE_DIRS
};