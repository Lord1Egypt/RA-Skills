const { chromium } = require('playwright');

async function refreshAndCheck() {
  console.log('刷新页面并检查学生...\n');
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('未找到班级小管家页面');
    await browser.close();
    return;
  }
  
  // 导航到主页
  console.log('导航到主页...');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/');
  await page.waitForTimeout(3000);
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 查找二下第31节
  console.log('查找二下第31节...');
  let found = false;
  for (let i = 0; i < 10; i++) {
    const result = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('二下(第31节)')) {
          return { found: true, label: label.substring(0, 50) };
        }
      }
      // 滚动查找
      const allElements = document.querySelectorAll('flt-semantics[aria-label]');
      let lastEl = null;
      for (const el of allElements) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) {
          lastEl = el;
        }
      }
      if (lastEl) lastEl.scrollIntoView({ block: 'start' });
      return { found: false };
    });
    
    if (result.found) {
      console.log('找到课程:', result.label);
      found = true;
      break;
    }
    await page.waitForTimeout(1500);
  }
  
  if (!found) {
    console.log('未找到课程');
    await browser.close();
    return;
  }
  
  // 点击进入课程
  console.log('点击进入课程...');
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes('二下(第31节)')) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  });
  
  await page.waitForTimeout(4000);
  console.log('当前URL:', page.url());
  
  // 检查学生列表
  console.log('检查学生列表...');
  
  // 多次检查，看是否会动态加载
  for (let check = 0; check < 3; check++) {
    await page.waitForTimeout(2000);
    
    const students = await page.evaluate(() => {
      const list = [];
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.length > 20) {
          const lines = label.split('\n');
          const name = lines[0].trim();
          if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
            const rect = el.getBoundingClientRect();
            list.push({
              name,
              top: rect.top,
              label: label.substring(0, 60)
            });
          }
        }
      }
      return list;
    });
    
    console.log(`第 ${check + 1} 次检查: 找到 ${students.length} 个学生`);
    students.forEach((s, i) => {
      console.log(`  [${i}] ${s.name} (top: ${s.top.toFixed(1)})`);
    });
  }
  
  await browser.close();
}

refreshAndCheck().catch(console.error);
