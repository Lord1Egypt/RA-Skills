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
  
  // 2. 获取所有学生列表（滚动加载）
  console.log('获取学生列表...');
  const allStudents = [];
  
  for (let scrollCount = 0; scrollCount < 10; scrollCount++) {
    // 获取当前可见的学生
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
    
    // 添加到列表（去重）
    for (const s of students) {
      if (!allStudents.find(existing => existing.name === s.name)) {
        allStudents.push(s);
      }
    }
    
    // 滚动到最后一个学生
    const hasMore = await page.evaluate(() => {
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
      if (last) {
        last.scrollIntoView({ block: 'start', behavior: 'instant' });
        return true;
      }
      return false;
    });
    
    if (!hasMore) break;
    await page.waitForTimeout(1500);
  }
  
  console.log(`✓ 共 ${allStudents.length} 个学生: ${allStudents.map(s => s.name).join(', ')}\n`);
  
  // 3. 滚动回顶部
  console.log('滚动到顶部...');
  await page.evaluate(() => {
    const container = document.querySelector('[style*="overflow-y: scroll"]');
    if (container) container.scrollTop = 0;
  });
  await page.waitForTimeout(1500);
  console.log('');
  
  // 4. 截图每个学生
  console.log('========================================');
  console.log('  开始截图');
  console.log('========================================\n');
  
  for (let i = 0; i < allStudents.length; i++) {
    const student = allStudents[i];
    const nextStudent = allStudents[i + 1];
    
    console.log(`[${i + 1}/${allStudents.length}] ${student.name}`);
    
    // 【关键】滚动到该学生，确保其在视口顶部
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
    await page.waitForTimeout(2000);
    
    // 【关键】等待滚动稳定后，重新获取位置
    await page.waitForTimeout(500);
    
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
