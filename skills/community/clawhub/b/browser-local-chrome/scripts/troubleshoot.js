#!/usr/bin/env node

/**
 * 浏览器故障排查工具
 * 
 * 用法：node scripts/troubleshoot.js
 */

const http = require('http');
const { exec } = require('child_process');

const OFFICIAL_PORT = '18800';
const LOCAL_PORT = '9222';

console.log('🔍 浏览器故障排查工具\n');
console.log('=' .repeat(50));

// 检查官方 Browser
function checkOfficialBrowser() {
  return new Promise((resolve) => {
    const url = `http://127.0.0.1:${OFFICIAL_PORT}/json/version`;
    http.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          const info = JSON.parse(data);
          console.log(`✅ 官方 Browser 运行中 (端口 ${OFFICIAL_PORT})`);
          console.log(`   版本：${info.Browser}`);
          resolve(true);
        } else {
          console.log(`❌ 官方 Browser 未响应 (端口 ${OFFICIAL_PORT})`);
          resolve(false);
        }
      });
    }).on('error', () => {
      console.log(`❌ 官方 Browser 未运行 (端口 ${OFFICIAL_PORT})`);
      resolve(false);
    });
  });
}

// 检查本地 Chrome
function checkLocalChrome() {
  return new Promise((resolve) => {
    const url = `http://127.0.0.1:${LOCAL_PORT}/json/version`;
    http.get(url, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          const info = JSON.parse(data);
          console.log(`✅ 本地 Chrome 运行中 (端口 ${LOCAL_PORT})`);
          console.log(`   版本：${info.Browser}`);
          resolve(true);
        } else {
          console.log(`❌ 本地 Chrome 未响应 (端口 ${LOCAL_PORT})`);
          resolve(false);
        }
      });
    }).on('error', () => {
      console.log(`❌ 本地 Chrome 未运行 (端口 ${LOCAL_PORT})`);
      resolve(false);
    });
  });
}

// 启动官方 Browser
function startOfficialBrowser() {
  return new Promise((resolve) => {
    console.log('\n🚀 尝试启动官方 Browser...');
    exec('openclaw browser --browser-profile openclaw start', (error, stdout, stderr) => {
      if (error) {
        console.log('❌ 启动失败:', error.message);
        resolve(false);
      } else {
        console.log('✅ 官方 Browser 已启动');
        resolve(true);
      }
    });
  });
}

// 启动本地 Chrome
function startLocalChrome() {
  return new Promise((resolve) => {
    console.log('\n🚀 尝试启动本地 Chrome...');
    exec('node scripts/start-chrome.js', { cwd: 'C:\\Users\\Admin\\.openclaw\\workspace\\skills\\browser-local-chrome' }, (error, stdout, stderr) => {
      if (error) {
        console.log('❌ 启动失败:', error.message);
        resolve(false);
      } else {
        console.log('✅ 本地 Chrome 已启动');
        resolve(true);
      }
    });
  });
}

// 主流程
async function main() {
  console.log('📌 步骤 1/3: 检查浏览器状态...\n');
  
  const officialRunning = await checkOfficialBrowser();
  const localRunning = await checkLocalChrome();
  
  console.log('\n📌 步骤 2/3: 分析结果...\n');
  
  if (officialRunning) {
    console.log('✅ 推荐：使用官方 Browser (默认配置)');
    console.log('\n💡 使用命令:');
    console.log('   openclaw browser --browser-profile openclaw open <URL>');
    console.log('   openclaw browser --browser-profile openclaw stop  (完成后关闭)');
  } else if (localRunning) {
    console.log('⚠️  官方 Browser 未运行，使用本地 Chrome (备用方案)');
    console.log('\n💡 使用命令:');
    console.log('   node scripts/start-chrome.js  (启动)');
    console.log('   node scripts/stop-chrome.js   (完成后关闭)');
  } else {
    console.log('❌ 两个浏览器都未运行，尝试启动...\n');
    
    console.log('📌 步骤 3/3: 启动浏览器...\n');
    
    // 尝试启动官方 Browser
    const started = await startOfficialBrowser();
    
    if (started) {
      setTimeout(async () => {
        const check = await checkOfficialBrowser();
        if (check) {
          console.log('\n✅ 启动成功！现在可以使用官方 Browser 了');
          console.log('\n💡 提示：');
          console.log('   - 如果官方 Browser 失败，运行：node scripts/start-chrome.js');
          console.log('   - 使用完成后记得关闭浏览器！');
        } else {
          console.log('\n⚠️  官方 Browser 启动失败，尝试本地 Chrome...');
          await startLocalChrome();
        }
      }, 3000);
    } else {
      // 官方失败，尝试本地 Chrome
      await startLocalChrome();
    }
  }
  
  console.log('\n' + '=' .repeat(50));
  console.log('✅ 排查完成！\n');
}

main();
