#!/usr/bin/env node

/**
 * 启动 Chrome 调试模式（跨平台）
 * 
 * 用法：node scripts/start-chrome.js [端口]
 * 示例：node scripts/start-chrome.js 9222
 */

const { exec } = require('child_process');
const path = require('path');
const os = require('os');

const CDP_PORT = process.argv[2] || '9222';
const platform = os.platform();

// 跨平台路径配置
const CONFIG = {
  win32: {
    userDataDir: 'C:\\chrome-debug-profile',
    chromePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
  },
  darwin: {
    userDataDir: '~/chrome-debug-profile',
    chromePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
  },
  linux: {
    userDataDir: '~/chrome-debug-profile',
    chromePath: '/usr/bin/google-chrome'
  }
};

const config = CONFIG[platform] || CONFIG.linux;
const USER_DATA_DIR = config.userDataDir;
const CHROME_PATH = config.chromePath;

console.log('🚀 启动 Chrome 调试模式...');
console.log(`   平台：${platform}`);
console.log(`   端口：${CDP_PORT}`);
console.log(`   用户数据目录：${USER_DATA_DIR}`);
console.log(`   Chrome 路径：${CHROME_PATH}`);

const args = [
  `--remote-debugging-port=${CDP_PORT}`,
  `--user-data-dir="${USER_DATA_DIR}"`,
  '--no-first-run',
  '--no-default-browser-check'
].join(' ');

const command = `"${CHROME_PATH}" ${args}`;

exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error('❌ 启动失败:', error.message);
    console.error('\n💡 提示：');
    if (platform === 'win32') {
      console.error('   确认 Chrome 已安装到默认路径');
      console.error('   或修改 _meta.json 中的 chromePath');
    } else if (platform === 'darwin') {
      console.error('   确认 Chrome 已安装：/Applications/Google Chrome.app');
      console.error('   或使用：which "Google Chrome"');
    } else {
      console.error('   确认 Chrome 已安装：which google-chrome');
      console.error('   或使用：sudo apt install google-chrome-stable');
    }
    process.exit(1);
  }
  
  console.log('✅ Chrome 已启动！');
  console.log(`   CDP 地址：http://127.0.0.1:${CDP_PORT}`);
  console.log(`   验证命令：curl http://127.0.0.1:${CDP_PORT}/json/version`);
});
