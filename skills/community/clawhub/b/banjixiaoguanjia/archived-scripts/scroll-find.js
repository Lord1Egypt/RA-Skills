const { chromium } = require('playwright');

async function scrollAndFind() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  console.log('当前页面URL:', page.url());
  console.log('\n开始滚动查找更多学生...\n');
  
  const allStudents = [];
  
  for (let i = 0; i < 10; i++) {
    // 获取当前可见学生
    const students = await page.evaluate(() => {
      const list = [];
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.length > 20 && label.includes('2026-')) {
          const lines = label.split(/\r?\n/);
          const name = lines[0].trim();
          if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
            list.push(name);
          }
        }
      }
      return list;
    });
    
    // 记录新学生
    for (const name of students) {
      if (!allStudents.includes(name)) {
        allStudents.push(name);
        console.log(`[${allStudents.length}] 发现学生: ${name}`);
      }
    }
    
    // 滚动
    console.log(`  第 ${i + 1} 次滚动...`);
    await page.evaluate(() => {
      const container = document.querySelector('[style*="overflow-y: scroll"]');
      if (container) {
        container.scrollTop += 300;
      }
    });
    
    await page.waitForTimeout(1000);
    
    // 检查是否还有更多
    const hasMore = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('没有更多')) {
          return false;
        }
      }
      return true;
    });
    
    if (!hasMore) {
      console.log('  已到达底部 (没有更多)');
      break;
    }
  }
  
  console.log(`\n总共找到 ${allStudents.length} 个学生:`);
  allStudents.forEach((name, i) => {
    console.log(`  ${i + 1}. ${name}`);
  });
  
  await browser.close();
}

scrollAndFind().catch(console.error);
