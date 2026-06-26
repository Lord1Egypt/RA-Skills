const { chromium } = require('playwright');

async function scrollToNextStudent() {
  console.log('========================================');
  console.log('  滚动到下一个学生');
  console.log('========================================\n');
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 获取当前在视口顶部的学生
  const beforeScroll = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    let topStudent = null;
    let minTop = Infinity;
    
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          if (rect.top >= -50 && rect.top < minTop) {
            minTop = rect.top;
            topStudent = { name, top: rect.top.toFixed(0) };
          }
        }
      }
    }
    return topStudent;
  });
  
  console.log(`滚动前顶部学生: ${beforeScroll ? beforeScroll.name : '无'} (top: ${beforeScroll ? beforeScroll.top : 'N/A'})`);
  
  // 向下滚动约400px
  console.log('\n执行滚动: scrollTop += 400');
  await page.evaluate(() => {
    const container = document.querySelector('[style*="overflow-y: scroll"]');
    if (container) {
      container.scrollTop += 400;
    }
  });
  await page.waitForTimeout(1500);
  
  // 获取滚动后在视口顶部的学生
  const afterScroll = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    let topStudent = null;
    let minTop = Infinity;
    
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          if (rect.top >= -50 && rect.top < minTop) {
            minTop = rect.top;
            topStudent = { name, top: rect.top.toFixed(0) };
          }
        }
      }
    }
    return topStudent;
  });
  
  console.log(`滚动后顶部学生: ${afterScroll ? afterScroll.name : '无'} (top: ${afterScroll ? afterScroll.top : 'N/A'})`);
  
  // 获取所有可见学生
  const visibleStudents = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          if (rect.top >= -50 && rect.top < window.innerHeight) {
            list.push({ name, top: rect.top.toFixed(0) });
          }
        }
      }
    }
    return list;
  });
  
  console.log('\n当前可见学生:');
  visibleStudents.forEach((s, i) => {
    console.log(`  [${i}] ${s.name} (top: ${s.top})`);
  });
  
  await browser.close();
  console.log('\n完成！');
}

scrollToNextStudent().catch(console.error);
