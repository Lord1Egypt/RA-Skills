const { chromium } = require('playwright');

async function inspectStudents() {
  console.log('检查学生列表页面结构...\n');
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('未找到班级小管家页面');
    await browser.close();
    return;
  }
  
  console.log('当前页面 URL:', page.url());
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 检查学生列表结构
  const students = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    const list = [];
    
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split('\n');
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          list.push({
            name,
            label: label.substring(0, 100),
            top: rect.top,
            left: rect.left,
            width: rect.width,
            height: rect.height,
            visible: rect.top > 0 && rect.top < window.innerHeight
          });
        }
      }
    }
    
    return list;
  });
  
  console.log('=== 学生列表 ===');
  students.forEach((s, i) => {
    console.log(`[${i}] ${s.name}`);
    console.log(`    位置: top=${s.top.toFixed(1)}, left=${s.left.toFixed(1)}`);
    console.log(`    尺寸: ${s.width.toFixed(1)}x${s.height.toFixed(1)}`);
    console.log(`    可见: ${s.visible}`);
    console.log(`    标签: ${s.label.substring(0, 50)}...`);
    console.log();
  });
  
  await browser.close();
}

inspectStudents().catch(console.error);
