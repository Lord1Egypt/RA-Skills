#!/usr/bin/env node
/**
 * rotate-key.js
 * 
 * 轮换指定平台的 API Key
 * 
 * 用法：node scripts/rotate-key.js <platform-id>
 */

const path = require('path');
const { checkPlatformStatus, saveCredential } = require('../index.js');
const CONFIG = require('../config.json');

function rotateKey(platformId) {
  console.log(`🔄 轮换 API Key: ${platformId}\n`);
  console.log('='.repeat(50));

  const status = checkPlatformStatus(platformId);
  
  if (!status.exists) {
    console.log(`❌ 错误：未找到平台 "${platformId}"`);
    console.log('\n可用平台:');
    Object.keys(CONFIG.platforms).forEach(id => {
      console.log(`  - ${id}`);
    });
    return;
  }

  console.log(`平台：${status.platform.name}`);
  console.log(`当前状态：${status.configured ? '已配置' : '未配置'}`);
  
  if (status.configured) {
    console.log(`当前 Key: ${status.keyPreview}`);
  }

  console.log('\n⚠️  轮换步骤:\n');
  console.log('1. 登录对应平台的控制台');
  console.log('2. 删除/撤销旧的 API Key');
  console.log('3. 生成新的 API Key');
  console.log('4. 将新 Key 提供给本技能进行保存');
  console.log('5. 验证新 Key 是否正常工作\n');

  console.log('💡 提示：');
  console.log(`   请访问：${status.platform.registerUrl}`);
  console.log(`   生成新 Key 后，使用 "配置 ${platformId} <新 Key>" 保存\n`);

  console.log('='.repeat(50));
}

// 获取命令行参数
const platformId = process.argv[2];

if (!platformId) {
  console.log('❌ 用法：node scripts/rotate-key.js <platform-id>\n');
  console.log('可用平台:');
  Object.keys(CONFIG.platforms).forEach(id => {
    const platform = CONFIG.platforms[id];
    console.log(`  - ${id} (${platform.name})`);
  });
  console.log('\n示例：node scripts/rotate-key.js openai');
} else {
  rotateKey(platformId);
}
