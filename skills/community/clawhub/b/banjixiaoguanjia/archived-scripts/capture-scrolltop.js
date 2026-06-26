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
  console.log('进入课程...');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/');
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
  
  await page.waitForTimeout(4000);
  console.log('已进入课程详情页\n');
  
  // 2. 获取所有学生及其滚动位置
  console.log('获取学生列表...');
  const studentsWithPositions = [];
  let scrollTop = 0;
  const scrollStep = 100;
  const maxScrolls = 50;
  
  for (let i = 0; i < maxScrolls; i++) {
    // 设置 scrollTop
    await page.evaluate((top) => {
      const container = document.querySelector('[style*="overflow-y: scroll"]');
      if (container) container.scrollTop = top;
    }, scrollTop);
    await page.waitForTimeout(800);
    
    // 获取当前在视口顶部的学生
    const studentAtTop = await page.evaluate(() => {
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
            // 找到在视口内且最靠上的学生
            if (rect.top >= -50 && rect.top < minTop) {
              minTop = rect.top;
              topStudent = { name, top: rect.top };
            }
          }
        }
      }
      
      return topStudent;
    });
    
    if (studentAtTop) {
      // 检查是否已记录
      const existing = studentsWithPositions.find(s => s.name === studentAtTop.name);
      if (!existing) {
        studentsWithPositions.push({
          name: studentAtTop.name,
          scrollTop: scrollTop,
          viewTop: studentAtTop.top
        });
        console.log(`  发现: ${studentAtTop.name} (scrollTop: ${scrollTop})`);
      }
    }
    
    // 检查是否到底
    const isAtBottom = await page.evaluate(() => {
      const container = document.querySelector('[style*="overflow-y: scroll"]');
      if (container) {
        return container.scrollTop + container.clientHeight >= container.scrollHeight - 10;
      }
      return false;
    });
    
    if (isAtBottom) break;
    
    scrollTop += scrollStep;
  }
  
  console.log(`✓ 共 ${studentsWithPositions.length} 个学生: ${studentsWithPositions.map(s => s.name).join(', ')}\n`);
  
  // 3. 截图每个学生
  console.log('========================================');
  console.log('  开始截图');
  console.log('========================================\n');
  
  for (let i = 0; i < studentsWithPositions.length; i++) {
    const student = studentsWithPositions[i];
    const nextStudent = studentsWithPositions[i + 1];
    
    console.log(`[${i + 1}/${studentsWithPositions.length}] ${student.name}`);
    
    // 滚动到该学生的位置
    await page.evaluate((top) => {
      const container = document.querySelector('[style*="overflow-y: scroll"]');
      if (container) container.scrollTop = top;
    }, student.scrollTop);
    await page.waitForTimeout(1500);
    
    // 获取当前学生位置
    const pos = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.indexOf(name) === 0) {
          const rect = el.getBoundingClientRect();
          return { top: rect.top };
        }
      }
      return null;
    }, student.name);
    
    if (!pos) {
      console.log(`  ⚠️ 未找到位置\n`);
      continue;
    }
    
    // 确定截图区域
    let clip;
    if (nextStudent) {
      // 滚动到下一个学生，获取其位置
      await page.evaluate((top) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) container.scrollTop = top;
      }, nextStudent.scrollTop);
      await page.waitForTimeout(1000);
      
      const nextPos = await page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && label.indexOf(name) === 0) {
            const rect = el.getBoundingClientRect();
            return { top: rect.top };
          }
        }
        return null;
      }, nextStudent.name);
      
      // 滚动回当前学生
      await page.evaluate((top) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) container.scrollTop = top;
      }, student.scrollTop);
      await page.waitForTimeout(1000);
      
      if (nextPos) {
        const height = nextPos.top - pos.top;
        clip = { 
          x: 0, 
          y: i === 0 ? -20 : pos.top, 
          width: 929, 
          height: i === 0 ? height + 20 : Math.max(100, height)
        };
        console.log(`  截图: ${student.name} → ${nextStudent.name} (${height.toFixed(0)}px)`);
      }
    }
    
    if (!clip) {
      clip = { 
        x: 0, 
        y: i === 0 ? -20 : pos.top, 
        width: 929, 
        height: i === 0 ? 820 : 800
      };
      console.log(`  截图: ${student.name} → 底部`);
    }
    
    const filepath = path.join(outputDir, `${student.name}.png`);
    await page.screenshot({ path: filepath, clip: clip });
    console.log(`  ✓ 已保存\n`);
  }
  
  console.log('========================================');
  console.log('  截图完成');
  console.log('========================================\n');
  
  await browser.close();
}

// 运行
captureHomework('二下(第31节)', 'C:\\Users\\Administrator\\Desktop\\二下(第31节)')
  .then(() => console.log('完成！'))
  .catch(console.error);
