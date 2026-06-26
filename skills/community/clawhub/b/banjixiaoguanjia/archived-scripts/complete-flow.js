/**
 * 调试脚本 - 完整的查找流程
 */

const { chromium } = require('playwright');

async function completeFlow() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const contexts = browser.contexts();
  const context = contexts[0];
  let page = context.pages()[0];
  
  // 1. 进入课程
  console.log('=== 1. 进入课程 ===');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 查找并点击"一下(第9节)"
  for (let i = 0; i < 15; i++) {
    const found = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('一下(第9节)')) return true;
      }
      const all = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of all) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) last = el;
      }
      if (last) last.scrollIntoView({ block: 'start' });
      return false;
    });
    
    if (found) break;
    await page.waitForTimeout(1500);
  }
  
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes('一下(第9节)')) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  });
  
  await page.waitForTimeout(5000);
  console.log('课程页面URL:', page.url());
  
  // 2. 点击第一个作业图片
  console.log('\n=== 2. 点击第一个作业图片 ===');
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    const images = [];
    for (let i = 0; i < elements.length; i++) {
      const rect = elements[i].getBoundingClientRect();
      if (rect.width >= 90 && rect.width <= 95 && rect.height >= 90 && rect.height <= 95) {
        images.push(i);
      }
    }
    if (images.length > 0) {
      elements[images[0]].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      console.log('点击了图片索引:', images[0]);
    }
  });
  
  await page.waitForTimeout(5000);
  console.log('批改页面URL:', page.url());
  
  // 3. 分析批改页面并找到"查看原图"按钮
  console.log('\n=== 3. 查找"查看原图"按钮 ===');
  
  // 获取所有元素
  const allElements = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    const results = [];
    for (let i = 0; i < elements.length; i++) {
      const rect = elements[i].getBoundingClientRect();
      const label = elements[i].getAttribute('aria-label') || '';
      results.push({ index: i, label: label.substring(0, 50), left: rect.left, top: rect.top, width: rect.width, height: rect.height });
    }
    return results;
  });
  
  console.log('所有元素（前20个）:');
  for (const el of allElements.slice(0, 20)) {
    console.log(`[${el.index}] 位置:(${el.left.toFixed(0)},${el.top.toFixed(0)}) 尺寸:${el.width.toFixed(0)}x${el.height.toFixed(0)} 标签:"${el.label}"`);
  }
  
  // 测试右上角元素
  console.log('\n=== 4. 测试右上角元素 ===');
  const topRight = allElements.filter(e => e.left > 700 && e.top < 150);
  console.log('右上角元素:', topRight.map(e => `[${e.index}]`).join(', '));
  
  for (const el of topRight) {
    console.log(`\n尝试点击 [${el.index}]...`);
    
    await page.evaluate((idx) => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[idx]) elements[idx].dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }, el.index);
    
    await page.waitForTimeout(2500);
    
    const pages = context.pages();
    if (pages.length > 1) {
      const newPage = pages[pages.length - 1];
      const url = newPage.url();
      console.log('✓ 新页面:', url.substring(0, 60));
      
      if (url.includes('img.banjixiaoguanjia.com')) {
        console.log(`✓✓✓ [${el.index}] 是"查看原图"按钮！`);
        await newPage.close();
        break;
      }
      await newPage.close();
    } else {
      const hasDialog = await page.evaluate(() => {
        const els = document.querySelectorAll('flt-semantics');
        for (const e of els) {
          if ((e.getAttribute('aria-label') || '').includes('对话框')) return true;
        }
        return false;
      });
      
      if (hasDialog) {
        console.log('✗ 对话框');
        await page.keyboard.press('Escape');
        await page.waitForTimeout(500);
      } else {
        console.log('? 无变化');
      }
    }
  }
  
  await browser.close();
}

completeFlow().catch(console.error);
