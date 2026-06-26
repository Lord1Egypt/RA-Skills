#!/usr/bin/env node

/**
 * 飞书文件发送权限检查 - 检查临时目录访问权限
 * 
 * 用法: node check-perm.js
 */

const { getMediaDirStatus, getAvailableMediaDir, resolveMediaDirs } = require('./shared');

function main() {
  const status = getMediaDirStatus();
  
  console.log(JSON.stringify({
    success: true,
    message: status.available 
      ? `✅ 临时目录可用: ${status.available}`
      : '❌ 没有可用的临时目录',
    currentStatus: {
      availableDir: status.available,
      recommendedDir: status.recommended
    },
    candidates: status.candidates.map(c => ({
      path: c.path,
      exists: c.exists,
      writable: c.writable,
      status: c.writable ? '✅ 可用' : (c.exists ? '❌ 无写权限' : '❌ 不存在')
    })),
    solution: status.available ? null : {
      step1: '在技能目录下创建 config.json',
      step2: '配置有效的目录路径:',
      example: {
        "mediaDirs": [
          "/home/admin/.openclaw/media",
          "/tmp/openclaw-media",
          "/你的工作目录/media"
        ]
      },
      note: '确保运行 OpenClaw 的用户对该目录有写权限'
    }
  }, null, 2));
}

main();
