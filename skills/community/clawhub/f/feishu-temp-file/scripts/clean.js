#!/usr/bin/env node

/**
 * 飞书文件发送清理 - 删除临时文件
 * 
 * 用法: 
 *   node clean.js              # 清理所有临时文件
 *   node clean.js <文件路径>  # 删除指定临时文件
 * 
 * 示例:
 *   node clean.js
 *   node clean.js /home/admin/.openclaw/media/temp_uploads/photo_123.png
 */

const fs = require('fs');
const path = require('path');
const { deleteTempFile, cleanTempDir, listTempFiles, getTempDir } = require('./shared');

function main() {
  const args = process.argv.slice(2);
  const specificFile = args[0];
  
  // 如果指定了具体文件，删除该文件
  if (specificFile) {
    // 支持 file:// 前缀
    let filePath = specificFile;
    if (filePath.startsWith('file://')) {
      filePath = filePath.replace('file://', '');
    }
    
    const result = deleteTempFile(filePath);
    
    console.log(JSON.stringify({
      success: result.success,
      operation: 'delete',
      path: filePath,
      message: result.success ? '临时文件已删除' : result.error
    }, null, 2));
    return;
  }
  
  // 否则列出临时文件
  const listResult = listTempFiles();
  
  if (listResult.count === 0) {
    console.log(JSON.stringify({
      success: true,
      message: '临时目录为空，无需清理',
      tempDir: getTempDir()
    }, null, 2));
    return;
  }
  
  // 清理所有临时文件
  const cleanResult = cleanTempDir();
  
  console.log(JSON.stringify({
    success: true,
    operation: 'clean',
    message: `清理完成，删除了 ${cleanResult.deleted} 个临时文件`,
    tempDir: getTempDir(),
    deleted: cleanResult.deleted,
    failed: cleanResult.failed,
    remainingBeforeClean: listResult.count
  }, null, 2));
}

main();
