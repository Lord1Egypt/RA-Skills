#!/usr/bin/env node

/**
 * 配置 OpenClaw 浏览器设置
 * 
 * 用法：node scripts/configure-browser.js [端口]
 */

const fs = require('fs');
const path = require('path');

const CDP_PORT = process.argv[2] || '9222';
const CONFIG_PATH = path.join(process.env.USERPROFILE, '.openclaw', 'openclaw.json');

console.log('⚙️  配置 OpenClaw 浏览器...');

// 读取配置文件
let config;
try {
  const content = fs.readFileSync(CONFIG_PATH, 'utf-8');
  config = JSON.parse(content);
} catch (error) {
  console.error('❌ 读取配置文件失败:', error.message);
  process.exit(1);
}

// 配置浏览器
config.browser = {
  enabled: true,
  defaultProfile: 'local-chrome',
  attachOnly: true,
  ssrfPolicy: {
    dangerouslyAllowPrivateNetwork: true
  },
  profiles: {
    'local-chrome': {
      cdpUrl: `http://127.0.0.1:${CDP_PORT}`,
      color: '#00AA00'
    }
  }
};

// 写回配置文件
try {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf-8');
  console.log('✅ 配置已更新！');
  console.log(`   配置文件：${CONFIG_PATH}`);
  console.log(`   CDP 地址：http://127.0.0.1:${CDP_PORT}`);
  console.log('\n⚠️  请重启 Gateway 使配置生效：');
  console.log('   openclaw gateway restart');
} catch (error) {
  console.error('❌ 写入配置文件失败:', error.message);
  process.exit(1);
}
