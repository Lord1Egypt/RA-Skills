const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const SKILL_ROOT = path.resolve(__dirname, '..');
const CONFIG_PATH = path.join(SKILL_ROOT, 'config.json');
const TEMP_DIR = 'temp_uploads';

// 默认候选目录
const DEFAULT_MEDIA_DIRS = [
  '/home/admin/.openclaw/media',
  '/tmp/openclaw-media',
  process.cwd() + '/media'
];

/**
 * 解析配置中的候选目录列表
 */
function resolveMediaDirs() {
  if (fs.existsSync(CONFIG_PATH)) {
    try {
      const cfg = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
      if (cfg.mediaDirs && Array.isArray(cfg.mediaDirs)) {
        return cfg.mediaDirs;
      }
      if (cfg.mediaDir) {
        return [cfg.mediaDir];
      }
    } catch (e) {
      // ignore
    }
  }
  
  // 检查环境变量
  const envDirs = process.env.FEISHU_MEDIA_DIRS;
  if (envDirs) {
    return envDirs.split(',').map(d => d.trim());
  }
  
  return DEFAULT_MEDIA_DIRS;
}

/**
 * 测试目录是否可写
 */
function testDirWritable(dir) {
  try {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    // 测试写入权限
    const testFile = path.join(dir, '.write_test_' + Date.now());
    fs.writeFileSync(testFile, 'test');
    fs.unlinkSync(testFile);
    return true;
  } catch (e) {
    return false;
  }
}

/**
 * 获取可用的临时目录
 */
function getAvailableMediaDir() {
  const dirs = resolveMediaDirs();
  
  for (const dir of dirs) {
    if (testDirWritable(dir)) {
      return dir;
    }
  }
  
  return null;
}

/**
 * 获取临时目录路径
 */
function getTempDir() {
  const mediaDir = getAvailableMediaDir();
  if (!mediaDir) {
    throw new Error(`无可用的临时目录。请在 config.json 中配置有效的目录路径。可选: ${DEFAULT_MEDIA_DIRS.join(', ')}`);
  }
  return path.join(mediaDir, TEMP_DIR);
}

/**
 * 获取所有候选目录及状态
 */
function getMediaDirStatus() {
  const dirs = resolveMediaDirs();
  const results = dirs.map(dir => ({
    path: dir,
    exists: fs.existsSync(dir),
    writable: testDirWritable(dir)
  }));
  
  const available = results.find(r => r.writable);
  
  return {
    candidates: results,
    available: available ? available.path : null,
    recommended: available ? available.path : dirs[0]
  };
}

/**
 * 确保临时目录存在
 */
function ensureTempDir() {
  const tempDir = getTempDir();
  if (!fs.existsSync(tempDir)) {
    fs.mkdirSync(tempDir, { recursive: true });
  }
  return tempDir;
}

/**
 * 生成唯一文件名
 */
function generateUniqueFilename(originalPath) {
  const ext = path.extname(originalPath);
  const basename = path.basename(originalPath, ext);
  const timestamp = Date.now();
  const random = crypto.randomBytes(4).toString('hex');
  
  // 使用安全的字符，只保留英文数字和下划线
  const safeBasename = basename.replace(/[^a-zA-Z0-9]/g, '_');
  
  return `${safeBasename}_${timestamp}_${random}${ext}`;
}

/**
 * 复制文件到临时目录
 */
function copyToTemp(sourcePath) {
  const tempDir = ensureTempDir();
  const filename = generateUniqueFilename(sourcePath);
  const destPath = path.join(tempDir, filename);
  
  fs.copyFileSync(sourcePath, destPath);
  
  return {
    success: true,
    originalPath: sourcePath,
    tempPath: destPath,
    filename: filename,
    url: `file://${destPath}`
  };
}

/**
 * 删除临时文件
 */
function deleteTempFile(tempPath) {
  try {
    if (fs.existsSync(tempPath)) {
      fs.unlinkSync(tempPath);
      return { success: true, path: tempPath };
    }
    return { success: false, error: '文件不存在' };
  } catch (e) {
    return { success: false, error: e.message };
  }
}

/**
 * 清理所有临时文件
 */
function cleanTempDir() {
  const tempDir = getTempDir();
  let deleted = 0;
  let failed = 0;
  
  if (!fs.existsSync(tempDir)) {
    return { success: true, deleted: 0, message: '临时目录不存在' };
  }
  
  const files = fs.readdirSync(tempDir);
  for (const file of files) {
    try {
      const filePath = path.join(tempDir, file);
      const stat = fs.statSync(filePath);
      if (stat.isFile()) {
        fs.unlinkSync(filePath);
        deleted++;
      }
    } catch (e) {
      failed++;
    }
  }
  
  return { success: true, deleted, failed };
}

/**
 * 列出临时文件
 */
function listTempFiles() {
  const tempDir = getTempDir();
  
  if (!fs.existsSync(tempDir)) {
    return { success: true, files: [] };
  }
  
  const files = fs.readdirSync(tempDir)
    .map(file => {
      const filePath = path.join(tempDir, file);
      const stat = fs.statSync(filePath);
      return {
        name: file,
        path: filePath,
        size: stat.size,
        created: stat.birthtime,
        url: `file://${filePath}`
      };
    })
    .filter(f => f.size > 0);
  
  return { success: true, files, count: files.length };
}

module.exports = {
  resolveMediaDirs,
  getAvailableMediaDir,
  getMediaDirStatus,
  getTempDir,
  ensureTempDir,
  generateUniqueFilename,
  copyToTemp,
  deleteTempFile,
  cleanTempDir,
  listTempFiles
};
