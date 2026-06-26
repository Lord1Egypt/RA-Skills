#!/usr/bin/env node
/**
 * WORKSPACE_DIR 动态检测模块
 * 
 * 功能：
 * - 自动检测当前 agent 的 workspace 目录
 * - 支持多 agent（developer, ops-specialist 等）
 * - 优先级：环境变量 > PWD 匹配 > 默认 workspace
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

const { log } = require('./logger');

/**
 * 获取当前 agent 的 workspace 目录
 * @returns {string} workspace 目录路径
 */
function getWorkspaceDir() {
  const homeDir = os.homedir();
  const openclawDir = path.join(homeDir, '.openclaw');
  
  // 优先级 1：环境变量 WORKSPACE_DIR（最可靠）
  if (process.env.WORKSPACE_DIR) {
    return process.env.WORKSPACE_DIR;
  }
  
  // 优先级 2：从当前工作目录推断
  const cwd = process.cwd();
  if (cwd.includes('workspace-')) {
    const match = cwd.match(/(workspace-[a-z-]+)/);
    if (match) {
      return path.join(openclawDir, match[1]);
    }
  }
  
  // 优先级 3：从 PWD 环境变量推断
  const pwd = process.env.PWD;
  if (pwd && pwd.includes('workspace-')) {
    const match = pwd.match(/(workspace-[a-z-]+)/);
    if (match) {
      return path.join(openclawDir, match[1]);
    }
  }
  
  // 优先级 4：默认使用 workspace-developer（当前 agent）
  // 不再使用第一个 workspace 目录，避免混淆
  return path.join(openclawDir, 'workspace-developer');
}

/**
 * 获取项目输出目录
 * @returns {string} projects 目录路径
 */
function getProjectsDir() {
  return path.join(getWorkspaceDir(), 'projects');
}

/**
 * 获取 1688-to-ozon 输出目录
 * @returns {string} 1688-to-ozon 输出目录路径
 * 
 * 目录结构（v1.0.51+）：
 * {workspace}/1688-to-ozon/
 * ├── 1688-tt/               # Step 1: 商品抓取
 * ├── ozon-image-translator/ # Step 2: 图片翻译
 * ├── ozon-pricer/           # Step 3: 价格计算
 * ├── mapping_result.json    # Step 4: 映射结果
 * └── upload-request.json   # OZON 上传请求
 */
function getOutputDir() {
  return path.join(getWorkspaceDir(), '1688-to-ozon');
}

/**
 * 清空输出目录（保留目录本身）
 */
function clearOutputDir() {
  const outputDir = getOutputDir();
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
    return;
  }
  
  const items = fs.readdirSync(outputDir);
  for (const item of items) {
    const itemPath = path.join(outputDir, item);
    try {
      if (fs.statSync(itemPath).isDirectory()) {
        fs.rmSync(itemPath, { recursive: true, force: true });
      } else {
        fs.unlinkSync(itemPath);
      }
    } catch (e) {
      // 忽略删除错误
    }
  }
  log(`🗑️ 已清空输出目录: ${outputDir}`, 'info');
}

module.exports = {
  getWorkspaceDir,
  getProjectsDir,
  getOutputDir,
  clearOutputDir
};
