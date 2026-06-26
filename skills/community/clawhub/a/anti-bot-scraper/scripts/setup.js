#!/usr/bin/env node
/**
 * setup.js - 自动安装 Chromium 并检查依赖
 */

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

async function main() {
  console.log('🔧 Stealth Scraper - 环境检查与安装\n');

  // 1. 检查 Node.js 版本
  const nodeVersion = process.version;
  const major = parseInt(nodeVersion.slice(1).split('.')[0], 10);
  if (major < 16) {
    console.error(`❌ Node.js 版本过低: ${nodeVersion}，需要 >= 16`);
    process.exit(1);
  }
  console.log(`✅ Node.js 版本: ${nodeVersion}`);

  // 2. 检查 node_modules
  const nmPath = path.join(__dirname, '..', 'node_modules');
  if (!fs.existsSync(nmPath)) {
    console.log('📦 未找到 node_modules，正在安装依赖...');
    try {
      execSync('npm install', {
        cwd: path.join(__dirname, '..'),
        stdio: 'inherit',
      });
      console.log('✅ 依赖安装完成');
    } catch (e) {
      console.error('❌ 依赖安装失败:', e.message);
      process.exit(1);
    }
  } else {
    console.log('✅ node_modules 已存在');
  }

  // 3. 检查 Playwright
  try {
    require.resolve('playwright');
    console.log('✅ Playwright 已安装');
  } catch {
    console.error('❌ Playwright 未找到，请运行 npm install');
    process.exit(1);
  }

  // 4. 安装 Chromium
  console.log('\n🌐 正在安装/检查 Chromium 浏览器...');
  try {
    execSync('npx playwright install chromium', {
      cwd: path.join(__dirname, '..'),
      stdio: 'inherit',
    });
    console.log('✅ Chromium 浏览器就绪');
  } catch (e) {
    console.error('❌ Chromium 安装失败:', e.message);
    console.log('💡 尝试手动运行: npx playwright install chromium');
    process.exit(1);
  }

  // 5. 验证启动
  console.log('\n🧪 验证浏览器启动...');
  try {
    const { chromium } = require('playwright');
    const browser = await chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto('about:blank');
    const title = await page.title();
    await browser.close();
    console.log('✅ 浏览器启动验证通过');
  } catch (e) {
    console.error('❌ 浏览器启动失败:', e.message);
    console.log('💡 可能需要安装系统依赖: npx playwright install-deps chromium');
    process.exit(1);
  }

  console.log('\n🎉 所有检查通过！Stealth Scraper 已就绪。');
}

main().catch((e) => {
  console.error('Fatal error:', e);
  process.exit(1);
});
