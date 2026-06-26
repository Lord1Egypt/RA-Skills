/**
 * 路径管理模块
 * 统一管理 1688-to-ozon 所有路径配置
 */

const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(__dirname, '..', 'config');
const PATHS_CONFIG = path.join(CONFIG_DIR, 'paths.json');

let pathsConfig = null;

/**
 * 加载路径配置
 */
function loadPathsConfig() {
  if (pathsConfig) return pathsConfig;
  
  try {
    const configContent = fs.readFileSync(PATHS_CONFIG, 'utf-8');
    pathsConfig = JSON.parse(configContent);
    return pathsConfig;
  } catch (error) {
    console.warn(`⚠️  加载路径配置失败：${error.message}，使用默认值`);
    return getDefaultPaths();
  }
}

/**
 * 获取工作目录（从环境变量或默认为当前目录）
 */
function getBaseDir() {
  return process.env.WORKSPACE_DIR || process.cwd();
}

/**
 * 解析路径模板
 * @param {string} template - 路径模板，如 "{WORKSPACE}/1688-to-ozon"
 * @returns {string} - 解析后的实际路径
 */
function resolvePath(template) {
  const baseDir = getBaseDir();
  return template
    .replace(/\{WORKSPACE\}/g, baseDir)
    .replace(/\{CONFIG\}/g, CONFIG_DIR);
}

/**
 * 获取目录路径
 * @param {string} key - 目录键名，如 "step1_1688"
 * @returns {string} - 解析后的实际路径
 */
function getDir(key) {
  const config = loadPathsConfig();
  const template = config.dirs?.[key];
  if (!template) {
    throw new Error(`未知的目录键：${key}`);
  }
  return resolvePath(template);
}

/**
 * 获取文件路径
 * @param {string} key - 文件键名，如 "mapping_result"
 * @param {Object} params - 替换参数，如 { category: "toy_set" }
 * @returns {string} - 解析后的实际路径
 */
function getFile(key, params = {}) {
  const config = loadPathsConfig();
  let template = config.files?.[key];
  if (!template) {
    throw new Error(`未知的文件键：${key}`);
  }
  
  // 替换参数
  for (const [paramKey, paramValue] of Object.entries(params)) {
    template = template.replace(new RegExp(`\\{${paramKey}\\}`, 'g'), paramValue);
  }
  
  return resolvePath(template);
}

/**
 * 获取图片相关路径
 * @param {string} key - 图片路径键名
 * @returns {string} - 解析后的实际路径
 */
function getImagePath(key) {
  const config = loadPathsConfig();
  const template = config.images?.[key];
  if (!template) {
    throw new Error(`未知的图片路径键：${key}`);
  }
  return resolvePath(template);
}

/**
 * 获取所有路径配置（用于调试）
 */
function getAllPaths() {
  const config = loadPathsConfig();
  return {
    baseDir: getBaseDir(),
    dirs: {
      root: getDir('root'),
      step1_1688: getDir('step1_1688'),
      step2_translator: getDir('step2_translator'),
      step3_pricer: getDir('step3_pricer'),
      step4_publisher: getDir('step4_publisher')
    },
    files: {
      mapping_config: getFile('mapping_config', { category: 'toy_set' }),
      mapping_result: getFile('mapping_result'),
      upload_request: getFile('upload_request'),
      upload_result: getFile('upload_result')
    },
    images: {
      step1_input: getImagePath('step1_input'),
      step2_output: getImagePath('step2_output'),
      step2_images_json: getImagePath('step2_images_json')
    }
  };
}

/**
 * 默认路径（当配置文件不存在时使用）
 */
function getDefaultPaths() {
  const base = process.cwd();
  return {
    dirs: {
      root: path.join(base, '1688-to-ozon'),
      step1_1688: path.join(base, '1688-to-ozon', '1688-tt'),
      step2_translator: path.join(base, '1688-to-ozon', 'ozon-image-translator'),
      step3_pricer: path.join(base, '1688-to-ozon', 'ozon-pricer'),
      step4_publisher: path.join(base, '1688-to-ozon', 'ozon-publisher')
    },
    files: {},
    images: {}
  };
}

module.exports = {
  loadPathsConfig,
  getBaseDir,
  getDir,
  getFile,
  getImagePath,
  getAllPaths,
  resolvePath
};