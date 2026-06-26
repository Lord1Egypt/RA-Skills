const { chromium } = require('playwright');

async function enterCourseAndWait() {
  console.log('========================================');
  console.log('  进入二下(第35节)课程页面');
  console.log('========================================\n');
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 1. 导航到主页
  console.log('1. 导航到主页...');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  // 2. 启用辅助功能
  console.log('2. 启用辅助功能...');
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 3. 查找二下(第35节)
  console.log('3. 查找二下(第35节)...');
  for (let i = 0; i < 15; i++) {
    const found = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('二下(第35节)')) return true;
      }
      // 滚动查找
      const all = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of all) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) last = el;
      }
      if (last) last.scrollIntoView({ block: 'start' });
      return false;
    });
    
    if (found) {
      console.log('   ✓ 找到课程');
      break;
    }
    await page.waitForTimeout(1500);
  }
  
  // 4. 点击进入课程
  console.log('4. 点击进入课程...');
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes('二下(第35节)')) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  });
  
  await page.waitForTimeout(5000);
  
  // 5. 检查当前页面
  const url = page.url();
  console.log(`\n✓ 已进入课程详情页`);
  console.log(`  URL: ${url}\n`);
  
  // 获取当前可见学生
  const students = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          list.push({ name, top: rect.top.toFixed(0) });
        }
      }
    }
    return list;
  });
  
  console.log('当前可见学生:');
  students.forEach((s, i) => {
    console.log(`  [${i}] ${s.name} (top: ${s.top})`);
  });
  
  console.log('\n========================================');
  console.log('  已进入二下(第35节)课程页面');
  console.log('  等待指令...');
  console.log('========================================');
  
  // 保持连接打开
  await new Promise(() => {});
}

enterCourseAndWait().catch(console.error);
