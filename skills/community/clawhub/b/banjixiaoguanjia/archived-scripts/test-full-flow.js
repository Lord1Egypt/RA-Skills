/**
 * 调试脚本 - 完整流程测试
 */

const { chromium } = require('playwright');

async function testFullFlow() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const contexts = browser.contexts();
  const context = contexts[0];
  let page = context.pages()[0];
  
  console.log('=== 步骤1: 进入课程列表 ===');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  console.log('当前URL:', page.url());
  
  // 查找"一下(第9节)"课程
  console.log('\n=== 步骤2: 查找课程 ===');
  for (let i = 0; i < 15; i++) {
    const found = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('一下(第9节)')) {
          return { found: true, label: label.substring(0, 50) };
        }
      }
      // 滚动查找
      const all = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of all) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) last = el;
      }
      if (last) last.scrollIntoView({ block: 'start' });
      return { found: false };
    });
    
    if (found.found) {
      console.log('找到课程:', found.label);
      break;
    }
    await page.waitForTimeout(1500);
  }
  
  // 点击进入课程
  console.log('\n=== 步骤3: 点击进入课程 ===');
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
  console.log('进入课程后URL:', page.url());
  
  // 获取页面所有带标签的元素
  console.log('\n=== 步骤4: 分析课程详情页 ===');
  const elements = await page.evaluate(() => {
    const allElements = document.querySelectorAll('flt-semantics');
    const results = [];
    
    for (let i = 0; i < allElements.length; i++) {
      const el = allElements[i];
      const label = el.getAttribute('aria-label') || '';
      
      if (label) {
        const rect = el.getBoundingClientRect();
        results.push({
          index: i,
          label: label.substring(0, 100),
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height
        });
      }
    }
    
    return results;
  });
  
  console.log('带标签的元素:');
  for (const el of elements.slice(0, 20)) {
    console.log(`[${el.index}] "${el.label}" 位置:(${el.left.toFixed(0)},${el.top.toFixed(0)})`);
  }
  
  // 查找92x92的图片元素
  console.log('\n=== 步骤5: 查找作业图片缩略图 ===');
  const images = await page.evaluate(() => {
    const allElements = document.querySelectorAll('flt-semantics');
    const results = [];
    
    for (let i = 0; i < allElements.length; i++) {
      const el = allElements[i];
      const rect = el.getBoundingClientRect();
      
      // 查找92x92左右的元素
      if (rect.width >= 85 && rect.width <= 100 && 
          rect.height >= 85 && rect.height <= 100) {
        const label = el.getAttribute('aria-label') || '';
        results.push({
          index: i,
          label: label.substring(0, 50),
          top: rect.top,
          left: rect.left,
          width: rect.width,
          height: rect.height
        });
      }
    }
    
    return results;
  });
  
  console.log('找到的图片元素:');
  for (const img of images.slice(0, 10)) {
    console.log(`[${img.index}] 位置:(${img.left.toFixed(0)},${img.top.toFixed(0)}) 尺寸:${img.width.toFixed(0)}x${img.height.toFixed(0)} 标签:"${img.label}"`);
  }
  
  // 点击第一个图片
  if (images.length > 0) {
    console.log('\n=== 步骤6: 点击第一个作业图片 ===');
    const firstImageIndex = images[0].index;
    
    await page.evaluate((index) => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[index]) {
        elements[index].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    }, firstImageIndex);
    
    await page.waitForTimeout(4000);
    console.log('点击后URL:', page.url());
    
    // 检查所有页面
    const allPages = context.pages();
    console.log('\n当前所有页面:');
    for (const p of allPages) {
      console.log('  -', p.url());
    }
    
    // 获取当前页面的所有标签
    console.log('\n=== 步骤7: 分析新页面 ===');
    const newElements = await page.evaluate(() => {
      const allElements = document.querySelectorAll('flt-semantics');
      const results = [];
      
      for (let i = 0; i < allElements.length; i++) {
        const el = allElements[i];
        const label = el.getAttribute('aria-label') || '';
        
        if (label) {
          results.push({
            index: i,
            label: label.substring(0, 100)
          });
        }
      }
      
      return results;
    });
    
    console.log('新页面的标签:');
    for (const el of newElements) {
      console.log(`[${el.index}] "${el.label}"`);
    }
  }
  
  await browser.close();
}

testFullFlow().catch(console.error);
