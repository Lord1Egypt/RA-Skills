#!/usr/bin/env node

const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  page.setDefaultTimeout(30000);
  
  const url = 'https://shop.futvortexstore.com/collections/liverpool';
  console.log(`打开页面: ${url}`);
  await page.goto(url, { waitUntil: 'domcontentloaded' });
  
  // 获取整个页面 HTML
  const html = await page.content();
  console.log('\n页面 HTML 长度: ', html.length);
  
  // 查找面包屑
  console.log('\n🔍 查找面包屑...');
  const breadcrumbs = await page.evaluate(() => {
    // 查找所有可能的面包屑元素
    const result = [];
    
    // 打印所有包含面包屑的元素
    const allElements = document.querySelectorAll('*');
    for (const el of allElements) {
      const className = el.className ? String(el.className) : '';
      const id = el.id ? String(el.id) : '';
      if (className.includes('breadcrumb') || className.includes('crumb') || 
          id.includes('breadcrumb') || id.includes('crumb')) {
        const links = Array.from(el.querySelectorAll('a')).map(a => ({
          href: a.getAttribute('href'),
          text: a.textContent.trim()
        }));
        result.push({
          tag: el.tagName,
          className: className,
          id: id,
          links: links
        });
      }
    }
    
    // 也查找导航
    const navs = Array.from(document.querySelectorAll('nav'));
    navs.forEach(nav => {
      const links = Array.from(nav.querySelectorAll('a')).map(a => ({
        href: a.getAttribute('href'),
        text: a.textContent.trim()
      }));
      if (links.length > 0) {
        result.push({
          tag: 'nav',
          className: nav.className,
          id: nav.id,
          links: links
        });
      }
    });
    
    return result;
  });
  
  console.log('\n找到面包屑容器: ', breadcrumbs.length);
  breadcrumbs.forEach((bc, i) => {
    console.log(`\n[${i+1}] ${bc.tag} .${bc.className} #${bc.id}`);
    bc.links.forEach((link, j) => {
      console.log(`   ${j+1}. ${link.text} -> ${link.href}`);
    });
  });
  
  // 截图
  await page.screenshot({ path: 'C:\\workspace\\caiji\\temp\\liverpool-screenshot.png', fullPage: true });
  console.log('\n📸 截图已保存: C:\\workspace\\caiji\\temp\\liverpool-screenshot.png');
  
  // 获取 H1
  const h1 = await page.$eval('h1', el => el.textContent.trim()).catch(() => null);
  console.log('H1: ', h1);
  
  await browser.close();
})();
