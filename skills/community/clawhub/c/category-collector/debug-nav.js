#!/usr/bin/env node

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  page.setDefaultTimeout(30000);
  
  const url = 'https://shop.futvortexstore.com/';
  console.log(`打开首页: ${url}`);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  
  // 输出导航 HTML 结构
  const navHtml = await page.evaluate(() => {
    const nav = document.querySelector('nav.t4s-navigation');
    if (!nav) return 'not found';
    
    // 输出整个 nav 的 HTML 结构
    return nav.innerHTML;
  });
  
  console.log('\n🌳 导航 HTML 结构:\n');
  console.log(navHtml.substring(0, 5000));
  
  // 统计菜单项
  const menuInfo = await page.evaluate(() => {
    const result = {
      totalLi: 0,
      liWithUl: 0,
      liWithA: 0
    };
    
    const lis = document.querySelectorAll('nav.t4s-navigation li');
    result.totalLi = lis.length;
    
    lis.forEach(li => {
      if (li.querySelector('ul')) result.liWithUl++;
      if (li.querySelector('a')) result.liWithA++;
    });
    
    return result;
  });
  
  console.log('\n📊 菜单统计:', menuInfo);
  
  // 检查 Premier League 菜单项
  const premierItem = await page.evaluate(() => {
    const items = Array.from(document.querySelectorAll('nav.t4s-navigation li a'));
    for (const a of items) {
      const text = a.textContent.trim();
      if (text.includes('Premier')) {
        const parent = a.parentElement;
        return {
          text: text,
          href: a.getAttribute('href'),
          hasUl: !!parent.querySelector('ul'),
          html: parent.innerHTML
        };
      }
    }
    return null;
  });
  
  console.log('\n⚽ Premier League 菜单项:', premierItem);
  
  await browser.close();
})();
