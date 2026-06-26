/**
 * lib/file_utils.js - 文件操作工具
 */
const fs = require('fs');
const path = require('path');
const config = require('./config');

/**
 * 确保目录存在
 * @param {string} dirPath 
 */
function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

/**
 * 递归删除目录
 * @param {string} dirPath 
 */
function removeDir(dirPath) {
  if (fs.existsSync(dirPath)) {
    fs.rmSync(dirPath, { recursive: true, force: true });
  }
}

/**
 * 读取 JSON 文件
 * @param {string} filePath 
 * @returns {object}
 */
function readJson(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(content);
}

/**
 * 写入 JSON 文件
 * @param {string} filePath 
 * @param {object} data 
 * @param {boolean} pretty 是否格式化
 */
function writeJson(filePath, data, pretty = true) {
  const content = pretty ? JSON.stringify(data, null, 2) : JSON.stringify(data);
  fs.writeFileSync(filePath, content, 'utf-8');
}

/**
 * 读取 Markdown 文件
 * @param {string} filePath 
 * @returns {string}
 */
function readMd(filePath) {
  return fs.readFileSync(filePath, 'utf-8');
}

/**
 * 写入 Markdown 文件
 * @param {string} filePath 
 * @param {string} content 
 */
function writeMd(filePath, content) {
  fs.writeFileSync(filePath, content, 'utf-8');
}

/**
 * 列出目录中的所有文件
 * @param {string} dirPath 
 * @param {string} extension 扩展名过滤 (如 '.md')
 * @returns {string[]}
 */
function listFiles(dirPath, extension = null) {
  if (!fs.existsSync(dirPath)) return [];
  
  const files = fs.readdirSync(dirPath);
  if (extension) {
    return files.filter(f => f.endsWith(extension));
  }
  return files;
}

/**
 * 复制文件
 * @param {string} src 
 * @param {string} dest 
 */
function copyFile(src, dest) {
  ensureDir(path.dirname(dest));
  fs.copyFileSync(src, dest);
}

/**
 * 获取文件大小
 * @param {string} filePath 
 * @returns {number} bytes
 */
function getFileSize(filePath) {
  const stats = fs.statSync(filePath);
  return stats.size;
}

/**
 * 格式化文件大小
 * @param {number} bytes 
 * @returns {string}
 */
function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

/**
 * 创建会话目录结构
 * @param {string} sessionId 
 * @returns {object} 各目录路径
 */
function createSessionDirs(sessionId) {
  const baseDir = config.getSessionDir(sessionId);
  const dirs = {
    base: baseDir,
    collected: path.join(baseDir, 'collected'),
    webPages: path.join(baseDir, 'collected', 'web_pages'),
    papers: path.join(baseDir, 'collected', 'papers'),
    insights: path.join(baseDir, 'insights'),
    content: path.join(baseDir, 'content'),
    slides: path.join(baseDir, 'content', 'slides'),
    optimizedSlides: path.join(baseDir, 'content', 'optimized_slides'),
    output: path.join(baseDir, 'output'),
    temp: path.join(baseDir, 'temp')
  };

  // 创建所有目录
  Object.values(dirs).forEach(dir => ensureDir(dir));

  return dirs;
}

/**
 * 生成安全的文件名
 * @param {string} name 
 * @returns {string}
 */
function safeFileName(name) {
  return name.replace(/[<>:"/\\|?*\x00-\x1f]/g, '_').substring(0, 100);
}

/**
 * 从 URL 提取域名作为来源标识
 * @param {string} url 
 * @returns {string}
 */
function extractDomain(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname.replace('www.', '');
  } catch {
    return 'unknown';
  }
}

module.exports = {
  ensureDir,
  removeDir,
  readJson,
  writeJson,
  readMd,
  writeMd,
  listFiles,
  copyFile,
  getFileSize,
  formatFileSize,
  createSessionDirs,
  safeFileName,
  extractDomain
};
