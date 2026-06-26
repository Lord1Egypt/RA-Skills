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
  
  // 2. 获取学生列表（滚动加载所有）
  console.log('获取学生列表...');
  const allStudents = new Map();
  
  for (let i = 0; i < 5; i++) {
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
            list.push({ name, top: rect.top });
          }
        }
      }
      return list;
    });
    
    let newCount = 0;
    for (const s of students) {
      if (!allStudents.has(s.name)) {
        allStudents.set(s.name, s);
        newCount++;
      }
    }
    
    if (newCount === 0 && i > 0) break;
    
    // 滚动到最后一个学生
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.length > 20) {
          const lines = label.split(/\r?\n/);
          const name = lines[0].trim();
          if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
            last = el;
          }
        }
      }
      if (last) last.scrollIntoView({ block: 'start', behavior: 'instant' });
    });
    
    await page.waitForTimeout(1500);
  }
  
  const students = Array.from(allStudents.values());
  console.log(`✓ 共 ${students.length} 个学生: ${students.map(s => s.name).join(', ')}`);
  
  // 【关键】滚动回顶部，确保第一个学生在 DOM 中
  console.log('滚动到顶部...');
  await page.evaluate(() => {
    const container = document.querySelector('[style*="overflow-y: scroll"]');
    if (container) container.scrollTop = 0;
  });
  await page.waitForTimeout(1500);
  console.log('');
  
  // 3. 截图每个学生
  console.log('========================================');
  console.log('  开始截图');
  console.log('========================================\n');
  
  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    const nextStudent = (i < students.length - 1) ? students[i + 1] : null;
    
    console.log(`[${i + 1}/${students.length}] ${student.name}`);
    
    // 第一个学生默认已在视图中，其他学生需要滚动
    if (i > 0) {
      await page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && label.indexOf(name) === 0) {
            el.scrollIntoView({ block: 'start', behavior: 'instant' });
            break;
          }
        }
      }, student.name);
      await page.waitForTimeout(1500);
    }
    
    // 获取当前位置
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
      
      if (nextPos) {
        const height = nextPos.top - pos.top;
        clip = { x: 0, y: pos.top, width: 929, height: Math.max(100, height) };
        console.log(`  截图: ${student.name} → ${nextStudent.name} (${height.toFixed(0)}px)`);
      }
    }
    
    if (!clip) {
      clip = { x: 0, y: pos.top, width: 929, height: 800 };
      console.log(`  截图: ${student.name} → 底部 (800px)`);
    }
    
    // 第一个学生从更上面开始
    if (i === 0) {
      clip.y = -20;
      clip.height += 20;
      console.log(`  调整: 第一个学生从 y=-20 开始`);
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
