#!/usr/bin/env node

/**
 * 一键配置浏览器自动化
 * 
 * 用法：node scripts/setup.js
 */

const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const CDP_PORT = '9222';
const SCRIPTS_DIR = path.join(__dirname);

console.log('🦞 浏览器自动化一键配置\n');
console.log('=' .repeat(50));

// 步骤 1: 启动 Chrome
console.log('\n📌 步骤 1/4: 启动 Chrome 调试模式...');
exec(`node "${path.join(SCRIPTS_DIR, 'start-chrome.js')}" ${CDP_PORT}`, (error) => {
  if (error) {
    console.error('❌ 启动失败:', error.message);
  } else {
    console.log('✅ Chrome 已启动');
  }
  
  // 等待 3 秒让 Chrome 完全启动
  setTimeout(() => {
    // 步骤 2: 配置 OpenClaw
    console.log('\n📌 步骤 2/4: 配置 OpenClaw...');
    exec(`node "${path.join(SCRIPTS_DIR, 'configure-browser.js')}" ${CDP_PORT}`, (error, stdout) => {
      if (error) {
        console.error('❌ 配置失败:', error.message);
      } else {
        console.log(stdout);
      }
      
      // 步骤 3: 检查状态
      console.log('\n📌 步骤 3/4: 检查浏览器状态...');
      exec(`node "${path.join(SCRIPTS_DIR, 'check-status.js')}" ${CDP_PORT}`, (error, stdout, stderr) => {
        if (error) {
          console.log('⚠️  浏览器未运行，需要手动启动');
          console.log('   命令：node scripts/start-chrome.js');
        } else {
          console.log(stdout);
        }
        
        // 步骤 4: 提示重启 Gateway
        console.log('\n📌 步骤 4/4: 重启 Gateway');
        console.log('⚠️  请手动执行以下命令使配置生效：');
        console.log('   openclaw gateway restart\n');
        
        console.log('=' .repeat(50));
        console.log('✅ 配置完成！\n');
        console.log('📖 使用说明:');
        console.log('   - 启动浏览器：node scripts/start-chrome.js');
        console.log('   - 检查状态：node scripts/check-status.js');
        console.log('   - 重新配置：node scripts/configure-browser.js');
        console.log('\n🎉 现在可以使用浏览器工具访问任何网站了！\n');
      });
    });
  }, 3000);
});
