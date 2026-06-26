/**
 * chrome-cdp-skill
 * 
 * 让AI agent访问已打开的Chrome标签页
 * 
 * 依赖: Node.js 22+, Chrome远程调试已启用
 */

const { execSync, spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

const CDP_SCRIPT = path.join(__dirname, 'scripts', 'cdp.mjs');
const CDP_DIR = path.join(__dirname);

// 检查CDP脚本是否存在
function checkCDP() {
  if (!fs.existsSync(CDP_SCRIPT)) {
    return { installed: false, message: '请先克隆 https://github.com/pasky/chrome-cdp-skill' };
  }
  return { installed: true };
}

// 执行CDP命令
function cdp(command, args = []) {
  const check = checkCDP();
  if (!check.installed) {
    return { error: check.message };
  }
  
  try {
    const cmd = ['node', CDP_SCRIPT, command, ...args];
    const output = execSync(cmd.join(' '), { 
      cwd: CDP_DIR,
      encoding: 'utf8',
      timeout: 30000
    });
    return { success: true, output };
  } catch (e) {
    return { error: e.message, output: e.stdout };
  }
}

/**
 * 列出所有打开的标签页
 */
async function listTabs() {
  const result = cdp('list');
  if (result.error) return { error: result.error };
  
  // 解析输出
  const lines = result.output.trim().split('\n');
  const tabs = [];
  
  for (let i = 1; i < lines.length; i++) { // 跳过表头
    const line = lines[i].trim();
    if (!line) continue;
    
    const parts = line.split(/\s{2,}/);
    if (parts.length >= 3) {
      tabs.push({
        targetId: parts[0].trim(),
        title: parts[1].trim(),
        url: parts[2].trim()
      });
    }
  }
  
  return { tabs };
}

/**
 * 获取标签页截图
 */
async function screenshot(targetId) {
  if (!targetId) return { error: '缺少targetId参数' };
  const result = cdp('shot', [targetId]);
  if (result.error) return { error: result.error };
  
  // 截图保存在 /tmp/screenshot.png
  return { success: true, path: '/tmp/screenshot.png' };
}

/**
 * 获取可访问性树
 */
async function accessibilitySnapshot(targetId) {
  if (!targetId) return { error: '缺少targetId参数' };
  const result = cdp('snap', [targetId]);
  if (result.error) return { error: result.error };
  return { success: true, tree: result.output };
}

/**
 * 获取HTML
 */
async function getHtml(targetId, selector = '') {
  if (!targetId) return { error: '缺少targetId参数' };
  const args = selector ? [targetId, selector] : [targetId];
  const result = cdp('html', args);
  if (result.error) return { error: result.error };
  return { success: true, html: result.output };
}

/**
 * 点击元素
 */
async function click(targetId, selector) {
  if (!targetId || !selector) return { error: '缺少参数: targetId, selector' };
  const result = cdp('click', [targetId, selector]);
  if (result.error) return { error: result.error };
  return { success: true };
}

/**
 * 输入文字
 */
async function type(targetId, text) {
  if (!targetId || !text) return { error: '缺少参数: targetId, text' };
  const result = cdp('type', [targetId, text]);
  if (result.error) return { error: result.error };
  return { success: true };
}

/**
 * 导航到URL
 */
async function navigate(targetId, url) {
  if (!targetId || !url) return { error: '缺少参数: targetId, url' };
  const result = cdp('nav', [targetId, url]);
  if (result.error) return { error: result.error };
  return { success: true };
}

/**
 * 执行JavaScript
 */
async function evaluate(targetId, expression) {
  if (!targetId || !expression) return { error: '缺少参数: targetId, expression' };
  const result = cdp('eval', [targetId, expression]);
  if (result.error) return { error: result.error };
  return { success: true, result: result.output };
}

/**
 * 获取网络资源信息
 */
async function networkInfo(targetId) {
  if (!targetId) return { error: '缺少targetId参数' };
  const result = cdp('net', [targetId]);
  if (result.error) return { error: result.error };
  return { success: true, info: result.output };
}

// 导出函数
module.exports = {
  // 检查
  checkCDP,
  
  // 基础操作
  listTabs,
  screenshot,
  accessibilitySnapshot: accessibilitySnapshot,
  getHtml,
  click,
  type,
  navigate,
  evaluate,
  networkInfo,
  
  // 快捷方法
  snap: accessibilitySnapshot,
  html: getHtml,
  eval: evaluate,
  net: networkInfo
};
