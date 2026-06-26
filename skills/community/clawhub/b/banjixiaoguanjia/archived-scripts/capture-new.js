const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureHomework(courseName, outputDir) {
  console.log('========================================');
  console.log(`  作业截图 - ${courseName}`);
  console.log('========================================\n');
  
  // 清理目录
  if (fs.existsSync(outputDir)) {
    fs.rmSync(outputDir, { recursive: true });
  }
  fs.mkdirSync(outputDir, { recursive: true });
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 1. 进入课程
  console.log('1. 进入课程...');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 查找课程
  for (let i = 0; i < 15; i++) {
    const found = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) return true;
      }
      const all = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of all) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) last = el;
      }
      if (last) last.scrollIntoView({ block: 'start' });
      return false;
    }, courseName);
    
    if (found) break;
    await page.waitForTimeout(1500);
  }
  
  // 点击进入
  await page.evaluate((name) => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes(name)) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  }, courseName);
  
  await page.waitForTimeout(5000);
  console.log('   ✓ 已进入课程详情页\n');
  
  // 2. 获取"已提交"数量
  console.log('2. 获取已提交数量...');
  const submittedCount = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes('已提交')) {
        const match = label.match(/(\d+)/);
        if (match) return parseInt(match[0]);
      }
    }
    return null;
  });
  
  if (submittedCount) {
    console.log(`   ✓ 已提交: ${submittedCount} 人\n`);
  } else {
    console.log('   ⚠️ 未获取到已提交数量，默认截图3人\n');
  }
  
  const targetCount = submittedCount || 5;
  
  // 3. 截图每个学生
  console.log('3. 开始截图...\n');
  console.log('========================================');
  
  const screenshots = [];
  const scrollStep = 400;
  
  while (screenshots.length < targetCount) {
    // 获取当前在视口顶部的学生
    const currentTopStudent = await page.evaluate(() => {
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
    
    if (!currentTopStudent) {
      console.log('   未找到学生，结束截图');
      break;
    }
    
    // 【关键】每次滚动后都截图，使用序号命名避免覆盖
    // 这样确保不会遗漏任何学生的作业
    const screenshotName = `截图${screenshots.length + 1}_${currentTopStudent.name}`;
    console.log(`\n[${screenshots.length + 1}] ${screenshotName}`);
    
    // 截图浏览器可见区域
    const filepath = path.join(outputDir, `${screenshotName}.png`);
    await page.screenshot({ path: filepath, fullPage: false, timeout: 60000 });
    console.log(`   ✓ 已保存: ${screenshotName}.png`);
    
    screenshots.push({ name: screenshotName, filepath });
    
    // 检查是否已截图数量达到已提交数量
    if (screenshots.length >= targetCount) {
      console.log('\n   已截图数量达到已提交数量，结束\n');
      break;
    }
    
    // 向下滚动400
    console.log(`   滚动: scrollTop += ${scrollStep}`);
    await page.evaluate((step) => {
      const container = document.querySelector('[style*="overflow-y: scroll"]');
      if (container) {
        container.scrollTop += step;
      }
    }, scrollStep);
    
    await page.waitForTimeout(1500);
  }
  
  console.log('========================================');
  console.log(`\n✓ 截图完成，共 ${screenshots.length} 个学生:`);
  screenshots.forEach((s, i) => console.log(`   ${i + 1}. ${s.name}`));
  console.log(`\n输出目录: ${outputDir}\n`);
  
  await browser.close();
  
  return {
    course: courseName,
    submittedCount,
    screenshotCount: screenshots.length,
    students: screenshots.map(s => s.name),
    outputDir
  };
}

// 运行
captureHomework('二下(第31节)', 'C:\\Users\\Administrator\\Desktop\\二下(第31节)')
  .then(result => {
    console.log('========================================');
    console.log('  批改结果');
    console.log('========================================');
    console.log(`课程: ${result.course}`);
    console.log(`已提交: ${result.submittedCount} 人`);
    console.log(`已截图: ${result.screenshotCount} 人`);
    console.log(`学生: ${result.students.join(', ')}`);
    console.log(`目录: ${result.outputDir}`);
    console.log('========================================');
  })
  .catch(console.error);
