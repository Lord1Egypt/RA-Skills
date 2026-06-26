#!/usr/bin/env node

/**
 * 飞书文件发送准备 - 复制文件到临时目录
 * 
 * 用法: node prepare.js <源文件路径>
 * 
 * 示例:
 *   node prepare.js /home/admin/images/照片.png
 *   node prepare.js /home/admin/documents/报告.pdf
 * 
 * 返回临时文件路径，用于飞书发送
 */

const fs = require('fs');
const path = require('path');
const { copyToTemp, getTempDir, getMediaDirStatus } = require('./shared');

function main() {
  const args = process.argv.slice(2);
  const sourcePath = args[0];
  
  // 首先检查目录权限状态
  const dirStatus = getMediaDirStatus();
  
  if (!dirStatus.available) {
    console.log(JSON.stringify({
      error: '无可用临时目录',
      message: '配置的候选目录都不可访问',
      candidates: dirStatus.candidates,
      solution: `请在 config.json 中配置有效的目录路径，或确保以下目录可写: ${dirStatus.candidates.map(c => c.path).join(', ')}`,
      example: {
        "mediaDirs": [
          "/home/admin/.openclaw/media",
          "/tmp/openclaw-media", 
          "/你的工作目录/media"
        ]
      }
    }, null, 2));
    process.exit(1);
  }
  
  if (!sourcePath) {
    console.log(JSON.stringify({
      error: '请指定源文件路径',
      usage: 'node prepare.js <源文件路径>',
      example: 'node prepare.js /home/admin/images/photo.png',
      availableDir: dirStatus.available,
      tip: `当前使用临时目录: ${dirStatus.available}`
    }, null, 2));
    process.exit(1);
  }
  
  // 检查源文件是否存在
  if (!fs.existsSync(sourcePath)) {
    console.log(JSON.stringify({
      error: '源文件不存在',
      path: sourcePath
    }, null, 2));
    process.exit(1);
  }
  
  const stat = fs.statSync(sourcePath);
  if (!stat.isFile()) {
    console.log(JSON.stringify({
      error: '源路径不是文件',
      path: sourcePath
    }, null, 2));
    process.exit(1);
  }
  
  // 复制文件到临时目录
  const result = copyToTemp(sourcePath);
  
  console.log(JSON.stringify({
    success: true,
    message: '文件已复制到临时目录，可用于飞书发送',
    originalPath: sourcePath,
    tempPath: result.tempPath,
    fileUrl: result.url,
    fileSize: stat.size,
    tempDir: getTempDir(),
    tip: '发送成功后请使用 clean.js 清理临时文件'
  }, null, 2));
}

main();
