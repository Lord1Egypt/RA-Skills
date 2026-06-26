const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function testCapture() {
  console.log('测试截图 - 二下第31节\n');
  
  const outputDir = 'C:\\Users\\Administrator\\Desktop\\二下(第31节)_测试';
  
  // 清理并创建目录
  if (fs.existsSync(outputDir)) {
    fs.rmSync(outputDir, { recursive: true });
  }
  fs.mkdirSync(outputDir, { recursive: true });
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('未找到班级小管家页面');
    await browser.close();
    return;
  }
  
  // 导航到主页
  await page.goto('https://service.banjixiaoguanjia.com/appweb/');
  await page.waitForTimeout(3000);
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 查找并进入二下第31节
  console.log('查找课程...');
  for (let i = 0; i < 10; i++) {
    const found = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('二下(第31节)')) return true;
      }
      const all = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of all) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) last = el;
      }
      if (last) last.scrollIntoView({ block: 'start' });
      return false;
    });
    
    if (found) break;
    await page.waitForTimeout(1500);
  }
  
  // 点击进入课程
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
  
  await page.waitForTimeout(4000);
  console.log('已进入课程详情页\n');
  
  // 获取学生列表（带滚动加载）
  console.log('获取学生列表...');
  const allStudents = new Map();
  
  for (let i = 0; i < 10; i++) {
    const students = await page.evaluate(() => {
      const list = [];
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.length > 20) {
          const lines = label.split('\n');
          const name = lines[0].trim();
          if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
            const rect = el.getBoundingClientRect();
            list.push({ name, top: rect.top, bottom: rect.bottom });
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
    
    console.log(`  第 ${i + 1} 次: +${newCount} 个 (累计: ${allStudents.size})`);
    
    if (newCount === 0 && i > 0) break;
    
    // 滚动到最后一个学生
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.length > 20) {
          const lines = label.split('\n');
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
  
  const studentList = Array.from(allStudents.values());
  console.log(`\n共找到 ${studentList.length} 个学生:`);
  studentList.forEach((s, i) => console.log(`  [${i}] ${s.name}`));
  
  // 截图
  console.log('\n=== 开始截图 ===');
  console.log('策略: 每个学生从顶部到下一个学生顶部\n');
  
  for (let i = 0; i < studentList.length; i++) {
    const student = studentList[i];
    const nextStudent = (i < studentList.length - 1) ? studentList[i + 1] : null;
    
    console.log(`[${i + 1}/${studentList.length}] ${student.name}`);
    
    // 滚动到该学生
    await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && (label.startsWith(name + '\n') || label.startsWith(name + '\r'))) {
          el.scrollIntoView({ block: 'start', behavior: 'instant' });
          break;
        }
      }
    }, student.name);
    await page.waitForTimeout(1500);
    
    // 获取当前学生位置
    const currentPos = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && (label.startsWith(name + '\n') || label.startsWith(name + '\r'))) {
          const rect = el.getBoundingClientRect();
          return { top: rect.top };
        }
      }
      return null;
    }, student.name);
    
    if (!currentPos) {
      console.log('  ⚠️ 未找到位置');
      continue;
    }
    
    // 确定截图区域
    let clip;
    if (nextStudent) {
      const nextPos = await page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && (label.startsWith(name + '\n') || label.startsWith(name + '\r'))) {
            const rect = el.getBoundingClientRect();
            return { top: rect.top };
          }
        }
        return null;
      }, nextStudent.name);
      
      if (nextPos) {
        const height = nextPos.top - currentPos.top;
        clip = { x: 0, y: Math.max(0, currentPos.top), width: 929, height: Math.max(100, height) };
        console.log(`  范围: ${student.name} → ${nextStudent.name} (${height.toFixed(0)}px)`);
      }
    }
    
    if (!clip) {
      clip = { x: 0, y: Math.max(0, currentPos.top), width: 929, height: 800 };
      console.log(`  范围: ${student.name} → 底部 (800px)`);
    }
    
    // 截图
    const filepath = path.join(outputDir, `${student.name}.png`);
    await page.screenshot({ path: filepath, clip: clip });
    console.log(`  ✓ 已保存\n`);
  }
  
  console.log('=== 截图完成 ===');
  console.log(`输出目录: ${outputDir}`);
  
  await browser.close();
}

testCapture().catch(console.error);
