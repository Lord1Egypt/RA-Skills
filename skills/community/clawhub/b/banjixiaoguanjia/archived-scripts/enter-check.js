const { chromium } = require('playwright');

async function enterAndCheck() {
  console.log('进入课程并检查学生\n');
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 强制重新导航到主页
  console.log('1. 重新导航到主页...');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  console.log(`   URL: ${page.url()}`);
  
  // 启用辅助功能
  console.log('2. 启用辅助功能...');
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 查找课程
  console.log('3. 查找二下(第31节)...');
  let courseFound = false;
  for (let i = 0; i < 15; i++) {
    const result = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('二下(第31节)')) {
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
    
    if (result.found) {
      console.log(`   ✓ 找到: ${result.label}`);
      courseFound = true;
      break;
    }
    await page.waitForTimeout(1500);
  }
  
  if (!courseFound) {
    console.log('   ✗ 未找到课程');
    await browser.close();
    return;
  }
  
  // 点击进入课程
  console.log('4. 点击进入课程...');
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
  
  // 等待页面跳转
  console.log('5. 等待页面跳转...');
  await page.waitForTimeout(5000);
  
  // 检查URL
  const url = page.url();
  console.log(`   URL: ${url}`);
  
  if (!url.includes('task_detail')) {
    console.log('   ✗ 未进入课程详情页');
    await browser.close();
    return;
  }
  
  console.log('   ✓ 已进入课程详情页\n');
  
  // 获取学生列表
  console.log('6. 获取学生列表...');
  const students = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          list.push(name);
        }
      }
    }
    return list;
  });
  
  console.log(`   学生列表 (${students.length}人):`);
  students.forEach((s, i) => console.log(`     [${i}] ${s}`));
  
  await browser.close();
  console.log('\n完成！');
}

enterAndCheck().catch(console.error);
