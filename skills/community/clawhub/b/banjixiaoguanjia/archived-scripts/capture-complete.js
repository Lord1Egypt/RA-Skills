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
  
  // ========== 第一阶段：进入课程并收集学生列表 ==========
  console.log('【第一阶段】收集学生列表\n');
  
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
    console.log('   ⚠️ 未获取到已提交数量\n');
  }
  
  const targetCount = submittedCount || 3;
  
  // 3. 收集学生列表
  console.log('3. 收集学生列表...');
  const studentList = [];
  const scrollStep = 400;
  
  while (studentList.length < targetCount) {
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
              list.push({ name, top: rect.top });
            }
          }
        }
      }
      return list;
    });
    
    // 记录新学生
    for (const student of visibleStudents) {
      if (!studentList.find(s => s.name === student.name)) {
        studentList.push(student);
        console.log(`   [${studentList.length}] ${student.name}`);
      }
    }
    
    // 检查是否已收集足够学生
    if (studentList.length >= targetCount) {
      console.log(`   ✓ 已收集 ${studentList.length} 个学生\n`);
      break;
    }
    
    // 向下滚动
    console.log(`   滚动查找更多学生...`);
    await page.evaluate((step) => {
      const container = document.querySelector('[style*="overflow-y: scroll"]');
      if (container) {
        container.scrollTop += step;
      }
    }, scrollStep);
    
    await page.waitForTimeout(1500);
  }
  
  console.log('   学生列表:');
  studentList.forEach((s, i) => console.log(`     ${i + 1}. ${s.name}`));
  console.log();
  
  // ========== 第二阶段：截图 ==========
  console.log('【第二阶段】截图\n');
  console.log('========================================');
  
  // 4. 重新进入页面（从第一个学生开始）
  console.log('4. 重新进入页面...');
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
  console.log('   ✓ 已重新进入课程详情页\n');
  
  // 5. 截图每个学生
  console.log('5. 截图每个学生...\n');
  
  const screenshots = [];
  
  for (let i = 0; i < studentList.length; i++) {
    const studentName = studentList[i].name;
    
    console.log(`[${i + 1}] ${studentName}`);
    
    // 截图
    const filepath = path.join(outputDir, `${studentName}.png`);
    await page.screenshot({ path: filepath, fullPage: false, timeout: 60000 });
    console.log(`   ✓ 已保存: ${studentName}.png`);
    
    screenshots.push({ name: studentName, filepath });
    
    // 如果不是最后一个学生，滚动到下一个
    if (i < studentList.length - 1) {
      console.log(`   滚动: scrollTop += ${scrollStep}`);
      await page.evaluate((step) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) {
          container.scrollTop += step;
        }
      }, scrollStep);
      
      await page.waitForTimeout(1500);
    }
  }
  
  console.log('\n========================================');
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
captureHomework('二下(第36节)', 'C:\\Users\\Administrator\\Desktop\\二下(第36节)')
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
