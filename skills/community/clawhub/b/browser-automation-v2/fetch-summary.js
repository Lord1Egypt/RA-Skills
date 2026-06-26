#!/usr/bin/env node

/**
 * 网页内容获取与摘要自动化（自动清理）- v2
 * 用法: node fetch-summary.js "https://example.com"
 */

const BrowserManager = require('./browser-manager.v2');

const url = process.argv[2];

if (!url) {
  console.error('❌ 请提供URL: node fetch-summary.js "https://example.com"');
  process.exit(1);
}

async function main() {
  const browser = new BrowserManager();
  
  try {
    console.log(`🌐 获取网页: ${url}`);
    
    // 优先使用 web_fetch（不启动浏览器）
    try {
      const { exec } = require('child_process');
      const result = await new Promise((resolve, reject) => {
        exec(`openclaw web_fetch "${url}" --max-chars 10000`, { timeout: 15000 }, (err, stdout, stderr) => {
          if (err) reject(err);
          else resolve(stdout);
        });
      });
      
      console.log('✅ 成功获取网页内容（静态）');
      const content = result.substring(0, 2000);
      console.log('\n📝 内容预览:\n', content.substring(0, 500) + '...\n');
      console.log('💡 提示: 可以使用 agent 对以上内容进行摘要分析');
      return;
    } catch (e) {
      console.log('⚠️ web_fetch 失败，切换到浏览器模式...');
    }
    
    // 备用方案：使用浏览器（带智能等待）
    await browser.start();
    await browser.open(url);
    await browser.waitForLoadState('domcontentloaded', 10000);
    
    // 截图
    const screenshotPath = await browser.screenshot();
    console.log('📸 截图:', screenshotPath);
    
    // 提取页面文本
    const textRes = await browser.runCommand(`openclaw browser --browser-profile ${browser.profile} evaluate --fn "document.body.innerText"`);
    if (textRes && textRes.stdout) {
      const preview = textRes.stdout.trim().substring(0, 2000);
      console.log('\n📄 页面文本预览:\n', preview.substring(0, 500) + '...');
    }
    
    await browser.cleanup();
    
  } catch (e) {
    browser.logger.error('获取网页失败', { error: e.message });
    await browser.cleanup();
    process.exit(1);
  }
}

main();

function fallbackToBrowser(url) {
  console.log('🔄 切换到浏览器模式...');
  
  // 导航到页面
  exec(`openclaw browser --browser-profile openclaw open "${url}"`, (err) => {
    if (err) return console.error('打开失败:', err);
    
    setTimeout(() => {
      // 截图
      exec('openclaw browser --browser-profile openclaw screenshot', (err, stdout) => {
        if (!err) console.log('📸 截图:', stdout.trim());
      });
      
      // 获取文本内容
      exec('openclaw browser --browser-profile openclaw evaluate --fn "document.body.innerText"', (err, stdout) => {
        if (!err) {
          const text = stdout.substring(0, 2000);
          console.log('📄 页面文本预览:\n', text.substring(0, 500) + '...');
        }
      });
    }, 2000);
  });
}
