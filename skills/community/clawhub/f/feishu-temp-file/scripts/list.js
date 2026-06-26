#!/usr/bin/env node

/**
 * 飞书文件发送列表 - 查看临时文件
 * 
 * 用法: node list.js
 */

const { listTempFiles, getTempDir } = require('./shared');

function main() {
  const result = listTempFiles();
  
  console.log(JSON.stringify({
    success: true,
    tempDir: getTempDir(),
    count: result.count,
    files: result.files.map(f => ({
      name: f.name,
      path: f.path,
      url: f.url,
      size: f.size,
      created: f.created
    }))
  }, null, 2));
}

main();
