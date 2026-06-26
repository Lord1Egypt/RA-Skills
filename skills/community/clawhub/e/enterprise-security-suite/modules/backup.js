/**
 * 自动备份模块
 */

const fs = require('fs');
const path = require('path');

function generateBackupFilename(filePath, date, sequence) {
  const dirname = path.dirname(filePath);
  const basename = path.basename(filePath);
  return path.join(dirname, `${basename}.${date}.${sequence}.bak`);
}

function getTodaySequence(dir, basename, date) {
  const pattern = new RegExp(`${basename}\\.${date}\\.(\\d{3})\\.bak`);
  const files = fs.readdirSync(dir);
  let maxSeq = 0;
  
  files.forEach(file => {
    const match = file.match(pattern);
    if (match) {
      const seq = parseInt(match[1], 10);
      if (seq > maxSeq) maxSeq = seq;
    }
  });
  
  return String(maxSeq + 1).padStart(3, '0');
}

async function autoBackup(options) {
  const { filePath, reason } = options;
  
  try {
    if (!fs.existsSync(filePath)) {
      return { success: false, error: '文件不存在' };
    }
    
    const dir = path.dirname(filePath);
    const basename = path.basename(filePath);
    const date = new Date().toISOString().slice(0, 10).replace(/-/g, '');
    const sequence = getTodaySequence(dir, basename, date);
    const backupPath = generateBackupFilename(filePath, date, sequence);
    
    fs.copyFileSync(filePath, backupPath);
    console.log(`✅ 已备份：${backupPath}`);
    if (reason) console.log(`原因：${reason}`);
    
    return { success: true, backupPath, timestamp: new Date().toISOString() };
  } catch (error) {
    console.error(`❌ 备份失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

function needsBackup(filePath, fileTypes) {
  const ext = path.extname(filePath);
  return fileTypes.includes(ext);
}

module.exports = {
  autoBackup,
  needsBackup,
  generateBackupFilename,
  getTodaySequence
};
