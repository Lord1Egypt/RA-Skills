const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureCourse(courseName, outputDir) {
  console.log('========================================');
  console.log(`  截图工具 - ${courseName}`);
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
  
  if (!page) {
    console.log('未找到班级小管家页面');
    await browser.close();
    return;
  }
  
  // 1. 导航到主页
  console.log('导航到主页...');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/');
  await page.waitForTimeout(3000);
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 2. 查找并进入课程
  console.log(`查找课程: ${courseName}`);
  for (let i = 0; i < 15; i++) {
    const found = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) return true;
      }
      // 滚动加载更多
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
  
  // 3. 滚动加载所有学生
  console.log('加载学生列表...');
  const allStudents = new Map();
  
  for (let i = 0; i < 15; i++) {
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
  
  const studentList = Array.from(allStudents.values());
  console.log(`✓ 共 ${studentList.length} 个学生: ${studentList.map(s => s.name).join(', ')}\n`);
  
  // 4. 截图前先滚动到顶部，确保所有学生都在 DOM 中
  console.log('滚动到页面顶部...');
  await page.evaluate(() => {
    // 【关键】使用 scrollTop = 0 滚动到顶部（scrollIntoView 在 Flutter 页面无效）
    const container = document.querySelector('[style*="overflow-y: scroll"]');
    if (container) {
      container.scrollTop = 0;
    }
    window.scrollTo(0, 0);
  });
  await page.waitForTimeout(2000);
  
  // 5. 截图每个学生
  console.log('========================================');
  console.log('  开始截图');
  console.log('========================================\n');
  
  // 【关键】使用滚动搜索来找到每个学生
  // 因为 scrollIntoView 在 Flutter 页面无效，我们需要通过滚动来定位学生
  
  for (let i = 0; i < studentList.length; i++) {
    const student = studentList[i];
    const nextStudent = (i < studentList.length - 1) ? studentList[i + 1] : null;
    
    console.log(`[${i + 1}/${studentList.length}] ${student.name}`);
    
    // 滚动搜索该学生
    let found = false;
    let scrollAttempts = 0;
    const maxScrollAttempts = 20;
    
    while (!found && scrollAttempts < maxScrollAttempts) {
      // 检查当前是否在视图中
      const checkResult = await page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && label.indexOf(name) === 0) {
            const rect = el.getBoundingClientRect();
            // 如果在视口顶部附近，认为找到了
            if (rect.top >= 0 && rect.top < 200) {
              return { found: true, top: rect.top, bottom: rect.bottom };
            }
          }
        }
        return { found: false };
      }, student.name);
      
      if (checkResult.found) {
        found = true;
        console.log(`  找到: top=${checkResult.top.toFixed(0)}`);
        
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
            const height = nextPos.top - checkResult.top;
            clip = { x: 0, y: Math.max(0, checkResult.top), width: 929, height: Math.max(100, height) };
            console.log(`  截图: ${student.name} → ${nextStudent.name} (${height.toFixed(0)}px)`);
          }
        }
        
        if (!clip) {
          // 最后一个学生：截图到底部
          clip = { x: 0, y: Math.max(0, checkResult.top), width: 929, height: 800 };
          console.log(`  截图: ${student.name} → 底部 (800px)`);
        }
        
        // 【关键】第一个学生的截图从更上面开始（-20），确保包含完整内容
        if (i === 0) {
          clip.y = -20;
          clip.height = clip.height + 20;
          console.log(`  调整: 第一个学生从 y=-20 开始`);
        }
        
        const filepath = path.join(outputDir, `${student.name}.png`);
        await page.screenshot({ path: filepath, clip: clip });
        console.log(`  ✓ 已保存: ${path.basename(filepath)}\n`);
        break;
      }
      
      // 未找到，滚动查找
      scrollAttempts++;
      
      if (scrollAttempts === 1 && i === 0) {
        // 第一个学生，先滚动到顶部
        await page.evaluate(() => {
          const container = document.querySelector('[style*="overflow-y: scroll"]');
          if (container) container.scrollTop = 0;
        });
      } else {
        // 滚动到最后一个可见学生
        await page.evaluate(() => {
          const elements = document.querySelectorAll('flt-semantics[aria-label]');
          let last = null;
          for (const el of elements) {
            const label = el.getAttribute('aria-label');
            if (label && label.length > 20) {
              const lines = label.split(/\r?\n/);
              const name = lines[0].trim();
              if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
                const rect = el.getBoundingClientRect();
                if (rect.top > 0) {
                  last = el;
                }
              }
            }
          }
          if (last) last.scrollIntoView({ block: 'start', behavior: 'instant' });
        });
      }
      
      await page.waitForTimeout(1000);
    }
    
    if (!found) {
      console.log(`  ⚠️ 未找到 ${student.name}\n`);
    }
  }
  
  console.log('\n========================================');
  console.log('  截图完成');
  console.log('========================================\n');
  
  await browser.close();
  
  return {
    course: courseName,
    studentCount: studentList.length,
    students: studentList.map(s => s.name),
    outputDir
  };
}

// 运行
const courseName = '二下(第31节)';
const outputDir = `C:\\Users\\Administrator\\Desktop\\${courseName}`;

captureCourse(courseName, outputDir)
  .then(result => {
    console.log('批改结果:');
    console.log(`  课程: ${result.course}`);
    console.log(`  学生: ${result.studentCount}`);
    console.log(`  列表: ${result.students.join(', ')}`);
    console.log(`  目录: ${result.outputDir}`);
  })
  .catch(console.error);
