/**
 * 调试当前页面
 */

const { chromium } = require('playwright');

const CONFIG = {
  cdpUrl: 'http://127.0.0.1:9222',
};

async function main() {
  let browser = null;
  let context = null;
  let page = null;
  
  try {
    browser = await chromium.connectOverCDP(CONFIG.cdpUrl);
    context = browser.contexts()[0];
    page = context.pages()[0] || await context.newPage();
    
    console.log('✅ 浏览器连接成功');
    console.log(`📍 当前 URL: ${page.url()}`);
    console.log(`📄 当前标题: ${await page.title()}`);
    console.log('\n📄 页面 body 前 1000 字符:');
    
    const body = await page.innerHTML('body');
    console.log(body.substring(0, 1000));
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  }
}

main();
