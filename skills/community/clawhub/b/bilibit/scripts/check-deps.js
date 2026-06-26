#!/usr/bin/env node

/**
 * 依赖检查脚本
 * 安装后自动检查并安装 BBDown
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

console.log('🔍 检查 bilibit 依赖...\n');

// 检查 BBDown
function checkBBDown() {
  try {
    execSync('which bbdown', { stdio: 'ignore' });
    console.log('✅ BBDown 已安装');
    return true;
  } catch (error) {
    console.log('⚠️  BBDown 未安装');
    return false;
  }
}

// 安装 BBDown
function installBBDown() {
  const platform = process.platform;
  
  console.log('\n📦 正在安装 BBDown...\n');
  
  try {
    if (platform === 'darwin') {
      // macOS
      console.log('检测到 macOS，使用 Homebrew 安装...');
      execSync('brew install bbdown', { stdio: 'inherit' });
    } else if (platform === 'linux') {
      // Linux
      console.log('检测到 Linux，使用 apt 安装...');
      execSync('sudo apt update && sudo apt install -y bbdown', { stdio: 'inherit' });
    } else if (platform === 'win32') {
      // Windows
      console.log('检测到 Windows，请手动安装：');
      console.log('1. 访问 https://github.com/nilaoda/BBDown/releases');
      console.log('2. 下载最新版本');
      console.log('3. 解压到 PATH 目录');
      return false;
    }
    
    console.log('\n✅ BBDown 安装成功！\n');
    return true;
  } catch (error) {
    console.log('\n⚠️  BBDown 安装失败，请手动安装：');
    console.log('   macOS: brew install bbdown');
    console.log('   Linux: sudo apt install bbdown');
    console.log('   Windows: https://github.com/nilaoda/BBDown/releases\n');
    return false;
  }
}

// 检查 ffmpeg
function checkFFmpeg() {
  try {
    execSync('which ffmpeg', { stdio: 'ignore' });
    console.log('✅ ffmpeg 已安装');
    return true;
  } catch (error) {
    console.log('⚠️  ffmpeg 未安装（可选，用于音视频合并）');
    return false;
  }
}

// 主流程
console.log('════════════════════════════════════════');
console.log('🎬 bilibit 依赖检查');
console.log('════════════════════════════════════════\n');

const hasBBDown = checkBBDown();
const hasFFmpeg = checkFFmpeg();

if (!hasBBDown) {
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  rl.question('\n💡 是否自动安装 BBDown？(y/n): ', (answer) => {
    rl.close();
    
    if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
      installBBDown();
    } else {
      console.log('\n⚠️  跳过 BBDown 安装');
      console.log('   需要下载视频时，请先手动安装 BBDown\n');
    }
    
    console.log('════════════════════════════════════════');
    console.log('✅ bilibit 已就绪！');
    console.log('════════════════════════════════════════\n');
    console.log('使用示例：');
    console.log('  bilibit search "LOL 集锦"');
    console.log('  bilibit https://b23.tv/BV1xx');
    console.log('  bilibit --help\n');
  });
} else {
  console.log('\n════════════════════════════════════════');
  console.log('✅ bilibit 已就绪！');
  console.log('════════════════════════════════════════\n');
  console.log('使用示例：');
  console.log('  bilibit search "LOL 集锦"');
  console.log('  bilibit https://b23.tv/BV1xx');
  console.log('  bilibit --help\n');
}
