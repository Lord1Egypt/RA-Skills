const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureVisibleArea() {
  console.log('========================================');
  console.log('  截图浏览器可见区域');
  console.log('========================================\n');
  
  const outputDir = 'C:\\Users\\Administrator\\Desktop\\二下(第31节)';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 获取当前可见学生
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
  
  console.log('当前可见学生:');
  visibleStudents.forEach((s, i) => {
    console.log(`  [${i}] ${s.name} (top: ${s.top})`);
  });
  
  // 截图浏览器可见区域（全屏截图）
  const filepath = path.join(outputDir, '截图1-可见区域.png');
  await page.screenshot({ path: filepath, fullPage: false });
  console.log(`\n✓ 已保存: ${filepath}`);
  console.log('  截图范围: 浏览器可见区域');
  
  await browser.close();
  console.log('\n完成！');
}

captureVisibleArea().catch(console.error);
