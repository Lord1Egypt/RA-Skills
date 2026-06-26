#!/usr/bin/env node

/**
 * 关闭 Chrome 调试模式（跨平台）
 * 
 * 用法：node scripts/stop-chrome.js
 */

const { exec } = require('child_process');
const os = require('os');

const platform = os.platform();

console.log('🛑 关闭 Chrome 浏览器...\n');

// 方法 1: 通过 CDP API 关闭浏览器（优雅关闭）
const http = require('http');
const CDP_PORT = process.argv[2] || '9222';
const CDP_URL = `http://127.0.0.1:${CDP_PORT}/json/version`;

console.log('📡 尝试通过 CDP API 关闭...');

http.get(CDP_URL, (res) => {
  let data = '';
  
  res.on('data', (chunk) => {
    data += chunk;
  });
  
  res.on('end', () => {
    if (res.statusCode === 200) {
      const info = JSON.parse(data);
      const wsUrl = info.webSocketDebuggerUrl;
      
      if (wsUrl) {
        console.log('✅ Chrome 已响应，尝试关闭所有标签页...');
        
        // 获取所有标签页并关闭
        http.get(`http://127.0.0.1:${CDP_PORT}/json`, (res2) => {
          let pages = '';
          
          res2.on('data', (chunk) => {
            pages += chunk;
          });
          
          res2.on('end', () => {
            try {
              const pageList = JSON.parse(pages);
              console.log(`   发现 ${pageList.length} 个标签页`);
              
              // 关闭所有标签页
              pageList.forEach((page, index) => {
                if (page.id) {
                  http.get(`http://127.0.0.1:${CDP_PORT}/json/close/${page.id}`, () => {});
                }
              });
              
              console.log('✅ 所有标签页已关闭');
            } catch (e) {
              console.log('⚠️  无法解析标签页列表');
            }
            
            // 强制关闭 Chrome 进程
            forceKill();
          });
        });
      }
    } else {
      console.log('⚠️  Chrome 未响应，尝试强制关闭...');
      forceKill();
    }
  });
}).on('error', (err) => {
  console.log('⚠️  无法连接到 Chrome，尝试强制关闭进程...');
  forceKill();
});

// 方法 2: 强制关闭 Chrome 进程（跨平台）
function forceKill() {
  console.log('\n🔨 强制关闭 Chrome 进程...');
  
  let command;
  let platformName;
  
  if (platform === 'win32') {
    command = 'taskkill /F /IM chrome.exe';
    platformName = 'Windows';
  } else if (platform === 'darwin') {
    command = 'killall "Google Chrome"';
    platformName = 'macOS';
  } else {
    command = 'killall -9 chrome';
    platformName = 'Linux';
  }
  
  exec(command, (error, stdout, stderr) => {
    if (error) {
      if (error.code === 128 || error.code === 1 || (stderr && stderr.includes('no process'))) {
        console.log('ℹ️  Chrome 进程未运行');
      } else {
        console.error('❌ 关闭失败:', error.message);
      }
    } else {
      console.log('✅ Chrome 已关闭');
      if (stdout) console.log(stdout);
    }
    
    // 获取用户数据目录路径
    let userDataDir;
    if (platform === 'win32') {
      userDataDir = 'C:\\chrome-debug-profile';
    } else {
      userDataDir = '~/chrome-debug-profile';
    }
    
    console.log('\n💡 提示：');
    console.log(`   - 用户数据目录：${userDataDir}`);
    console.log('   - 如需清理缓存，可删除此目录');
    console.log('   - 下次启动会自动创建新配置文件');
  });
}
