#!/usr/bin/env node
/**
 * check-status.js
 * 
 * 检查所有编程助手平台的凭据配置状态
 */

const path = require('path');
const { getAllPlatformsStatus, maskKey } = require('../index.js');

function checkStatus() {
  console.log('🔐 编程助手凭据配置状态检查\n');
  console.log('='.repeat(50));
  
  const statuses = getAllPlatformsStatus();
  const configured = statuses.filter(s => s.configured);
  const notConfigured = statuses.filter(s => !s.configured);

  console.log(`\n📊 总览：${configured.length}/${statuses.length} 已配置\n`);

  if (configured.length > 0) {
    console.log('✅ 已配置的平台:\n');
    configured.forEach(s => {
      console.log(`  • ${s.platform.name}`);
      console.log(`    Key: ${s.keyPreview}`);
      console.log(`    注册：${s.platform.registerUrl}`);
      console.log('');
    });
  }

  if (notConfigured.length > 0) {
    console.log('⬜ 未配置的平台:\n');
    notConfigured.forEach(s => {
      console.log(`  • ${s.platform.name}`);
      console.log(`    注册：${s.platform.registerUrl}`);
      console.log(`    免费：${s.platform.freeTier || '无'}`);
      console.log('');
    });
  }

  console.log('='.repeat(50));
  console.log('\n💡 提示：使用 "配置 <平台名>" 来添加新的 API Key');
  console.log('   例如：配置 GitHub Copilot\n');
}

// 运行检查
checkStatus();
