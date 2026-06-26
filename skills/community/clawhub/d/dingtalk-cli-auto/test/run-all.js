#!/usr/bin/env node

/**
 * 统一测试入口
 * Usage: node test/run-all.js
 */

const { DWSClient } = require('../lib/dws');

console.log('🔧 钉钉 CLI 自动化 Skill - 测试套件\n');

// 1. 检查 dws CLI 安装
async function testDwsInstalled() {
  console.log('📋 测试 1: 检查 dws CLI 安装');
  const client = new DWSClient();
  const installed = client.checkInstalled();
  
  if (installed) {
    console.log('  ✅ dws CLI 已安装');
  } else {
    console.log('  ⚠️  dws CLI 未安装');
    console.log('  💡 请运行: curl -fsSL https://raw.githubusercontent.com/DingTalk-Real-AI/dingtalk-workspace-cli/main/scripts/install.sh | sh');
  }
  return installed;
}

// 2. 检查认证状态
async function testAuth() {
  console.log('\n📋 测试 2: 检查认证状态');
  const client = new DWSClient();
  
  if (!client.checkInstalled()) {
    console.log('  ⏭️  跳过: dws CLI 未安装');
    return null;
  }
  
  const authenticated = client.checkAuth();
  
  if (authenticated) {
    console.log('  ✅ 已认证');
  } else {
    console.log('  ⚠️  未认证');
    console.log('  💡 请运行: dws auth login');
  }
  return authenticated;
}

// 3. 检查环境变量
function testEnvVars() {
  console.log('\n📋 测试 3: 检查环境变量');
  
  const appKey = process.env.DWS_CLIENT_ID || process.env.DINGTALK_APP_KEY;
  const appSecret = process.env.DWS_CLIENT_SECRET || process.env.DINGTALK_APP_SECRET;
  
  if (appKey) {
    console.log('  ✅ DWS_CLIENT_ID 已配置');
  } else {
    console.log('  ⚠️  DWS_CLIENT_ID 未配置');
  }
  
  if (appSecret) {
    console.log('  ✅ DWS_CLIENT_SECRET 已配置');
  } else {
    console.log('  ⚠️  DWS_CLIENT_SECRET 未配置');
  }
  
  return { appKey: !!appKey, appSecret: !!appSecret };
}

// 4. 检查模块加载
function testModules() {
  console.log('\n📋 测试 4: 检查模块加载');
  
  const modules = [
    { name: 'DWS Client', path: '../lib/dws' },
    { name: 'Message Client', path: '../lib/message' },
    { name: 'Calendar Client', path: '../lib/calendar' },
    { name: 'Todo Client', path: '../lib/todo' },
    { name: 'Contact Client', path: '../lib/contact' }
  ];
  
  let allLoaded = true;
  
  for (const mod of modules) {
    try {
      require(mod.path);
      console.log(`  ✅ ${mod.name}`);
    } catch (e) {
      console.log(`  ❌ ${mod.name}: ${e.message}`);
      allLoaded = false;
    }
  }
  
  return allLoaded;
}

// 5. 检查脚本文件
function testScripts() {
  console.log('\n📋 测试 5: 检查脚本文件');
  
  const fs = require('fs');
  const path = require('path');
  
  const scripts = [
    'scripts/message.js',
    'scripts/calendar.js',
    'scripts/todo.js',
    'scripts/contact.js',
    'scripts/robot.js'
  ];
  
  let allExist = true;
  
  for (const script of scripts) {
    const scriptPath = path.join(__dirname, '..', script);
    if (fs.existsSync(scriptPath)) {
      console.log(`  ✅ ${script}`);
    } else {
      console.log(`  ❌ ${script} 不存在`);
      allExist = false;
    }
  }
  
  return allExist;
}

// 运行所有测试
async function runAllTests() {
  await testDwsInstalled();
  await testAuth();
  testEnvVars();
  testModules();
  testScripts();
  
  console.log('\n' + '='.repeat(50));
  console.log('⚠️  注意: 完整功能测试需要:');
  console.log('  1. 安装 dws CLI');
  console.log('  2. 完成 dws auth login');
  console.log('  3. 配置 DWS_CLIENT_ID 和 DWS_CLIENT_SECRET');
  console.log('='.repeat(50));
}

runAllTests().catch(console.error);