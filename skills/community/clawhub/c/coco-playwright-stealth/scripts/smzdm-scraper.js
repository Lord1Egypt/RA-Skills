#!/usr/bin/env node
/**
 * SMZDM Scraper - 高级反反爬版本
 * 使用更真实的浏览器环境
 */

const { chromium } = require('playwright');
const fs = require('fs');

const url = process.argv[2] || 'https://www.smzdm.com/fenlei/nas/';

async function scrape() {
  console.log('🕷️ 启动SMZDM爬虫...');
  
  const browser = await chromium.launch({
    headless: false,
    args: [
      '--disable-blink-features=AutomationControlled',
      '--disable-dev-shm-usage',
      '--no-sandbox',
    ]
  });
  
  // 创建更真实的上下文
  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
    permissions: ['geolocation'],
  });
  
  // 注入stealth脚本
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
    Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
    Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en'] });
  });
  
  const page = await context.newPage();
  
  console.log('📱 导航到:', url);
  
  try {
    await page.goto(url, { 
      waitUntil: 'networkidle',
      timeout: 60000 
    });
    
    // 等待页面加载
    await page.waitForTimeout(10000);
    
    // 获取内容
    const title = await page.title();
    const content = await page.content();
    
    console.log('📄 标题:', title);
    console.log('📊 内容长度:', content.length);
    
    // 截图
    await page.screenshot({ path: './smzdm-screenshot.png', fullPage: true });
    console.log('📸 截图保存: ./smzdm-screenshot.png');
    
    // 尝试提取商品信息
    const items = await page.evaluate(() => {
      const results = [];
      // 尝试多种选择器
      const selectors = [
        '.feed-link-outer',
        '.z-tagContent', 
        '.goods-list-item',
        '.feed-row',
        'article'
      ];
      
      for (const sel of selectors) {
        const els = document.querySelectorAll(sel);
        if (els.length > 0) {
          console.log('找到选择器:', sel, els.length);
          els.forEach(el => {
            const title = el.textContent.substring(0, 100);
            results.push(title);
          });
          break;
        }
      }
      return results;
    });
    
    console.log('📦 商品数量:', items.length);
    items.slice(0, 5).forEach((item, i) => {
      console.log(`${i+1}. ${item}...`);
    });
    
  } catch (e) {
    console.error('❌ 错误:', e.message);
  }
  
  await browser.close();
}

scrape();
