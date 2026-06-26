/**
 * 回滚机制模块
 */

const fs = require('fs');
const path = require('path');
const backup = require('./backup');
const changelog = require('./changelog');

function findBackups(filePath, targetVersion) {
  const dir = path.dirname(filePath);
  const basename = path.basename(filePath);
  const files = fs.readdirSync(dir);
  const backups = [];
  
  files.forEach(file => {
    if (file.startsWith(basename + '.') && file.endsWith('.bak')) {
      const parts = file.split('.');
      if (parts.length >= 4) {
        const date = parts[parts.length - 3];
        const sequence = parts[parts.length - 2];
        backups.push({
          file,
          path: path.join(dir, file),
          date,
          sequence,
          version: `${date}.${sequence}`
        });
      }
    }
  });
  
  backups.sort((a, b) => {
    if (b.date !== a.date) return b.date.localeCompare(a.date);
    return parseInt(b.sequence) - parseInt(a.sequence);
  });
  
  if (targetVersion) {
    return backups.filter(b => b.version === targetVersion);
  }
  
  return backups;
}

async function rollback(options) {
  const { filePath, targetVersion, reason = '用户要求回滚' } = options;
  
  try {
    const backups = findBackups(filePath, targetVersion);
    
    if (backups.length === 0) {
      throw new Error(`未找到备份文件：${filePath}`);
    }
    
    const backupFile = targetVersion ? backups[0] : backups[0];
    
    await backup.autoBackup({
      filePath,
      reason: `回滚前备份（目标版本：${backupFile.version}）`
    });
    
    fs.copyFileSync(backupFile.path, filePath);
    
    console.log(`✅ 回滚完成：${filePath}`);
    console.log(`目标版本：${backupFile.version}`);
    
    await changelog.logChange({
      file: filePath,
      type: '回滚',
      reason,
      executor: '用户'
    });
    
    return {
      success: true,
      filePath,
      targetVersion: backupFile.version,
      backupFile: backupFile.path
    };
  } catch (error) {
    console.error(`❌ 回滚失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

module.exports = {
  rollback,
  findBackups
};
