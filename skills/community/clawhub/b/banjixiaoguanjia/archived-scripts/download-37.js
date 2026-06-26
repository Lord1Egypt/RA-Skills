const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');

/**
 * 组合脚本：启动浏览器 + 下载作业
 * 课程: 二下(第37节)
 */

const COURSE_NAME = '二下(第37节)';
const CDP_URL = 'http://localhost:9222';
const BASE_URL = 'https://service.banjixiaoguanjia.com/appweb/';
const OUTPUT_DIR = path.join(require('os').homedir(), 'Desktop');

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function isChromeRunning() {
  try {
    const response = await fetch(`${CDP_URL}/json/version`);
    return response.ok;
  } catch (e) {
    return false;
  }
}

async function startChrome() {
  console.log('启动 Chrome...');
  const profileDir = path.join(require('os').homedir(), '.banjixiaoguanjia', 'chrome-profile');
  
  if (!fs.existsSync(profileDir)) {
    fs.mkdirSync(profileDir, { recursive: true });
  }
  
  const chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const args = [
    `--remote-debugging-port=9222`,
    `--user-data-dir=${profileDir}`,
    `--window-size=1280,1000`,
    `--no-first-run`,
    `--no-default-browser-check`,
    BASE_URL
  ];
  
  const chrome = spawn(chromePath, args, {
    detached: true,
    stdio: 'ignore'
  });
  
  chrome.unref();
  
  // 等待 Chrome 启动
  let attempts = 0;
  while (attempts < 30) {
    await delay(1000);
    if (await isChromeRunning()) {
      console.log('✅ Chrome 已启动');
      return true;
    }
    attempts++;
    process.stdout.write('.');
  }
  
  throw new Error('Chrome 启动超时');
}

async function downloadHomework() {
  console.log(`\n============================================================`);
  console.log(`  班级小管家作业下载`);
  console.log(`  课程: ${COURSE_NAME}`);
  console.log(`============================================================\n`);
  
  // 1. 检查并启动 Chrome
  if (!(await isChromeRunning())) {
    await startChrome();
    await delay(3000); // 等待页面加载
  } else {
    console.log('✅ Chrome 已在运行');
  }
  
  // 2. 连接到 Chrome
  console.log(`连接到 Chrome: ${CDP_URL}`);
  const browser = await chromium.connectOverCDP(CDP_URL);
  const contexts = browser.contexts();
  const context = contexts[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    page = await context.newPage();
    await page.goto(BASE_URL);
  }
  
  await page.waitForLoadState('networkidle');
  console.log('✅ 已连接到 Chrome\n');
  
  // 3. 加载分析结果
  const analysisFile = path.join(OUTPUT_DIR, COURSE_NAME, 'analysis-results.json');
  if (!fs.existsSync(analysisFile)) {
    throw new Error(`分析结果文件不存在: ${analysisFile}`);
  }
  
  const analysisResults = JSON.parse(fs.readFileSync(analysisFile, 'utf-8'));
  console.log(`✅ 已加载分析结果，共 ${analysisResults.length} 个学生\n`);
  
  // 4. 启用辅助功能
  console.log('阶段1: 启用辅助功能...');
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await delay(2000);
  console.log('✅ 辅助功能已启用\n');
  
  // 5. 进入课程
  console.log('阶段2: 进入课程...');
  
  // 先导航到首页
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await delay(3000);
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await delay(2000);
  
  // 查找课程
  let found = false;
  for (let i = 0; i < 30; i++) {
    found = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) {
          console.log('找到课程:', label);
          return true;
        }
      }
      return false;
    }, COURSE_NAME);
    
    if (found) {
      console.log(`\n✅ 找到课程: ${COURSE_NAME}`);
      break;
    }
    
    // 滚动查找
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      let lastCourseEl = null;
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) {
          lastCourseEl = el;
        }
      }
      if (lastCourseEl) lastCourseEl.scrollIntoView({ block: 'start' });
    });
    
    await delay(1500);
    process.stdout.write('.');
  }
  
  if (!found) {
    throw new Error('未找到课程');
  }
  
  // 点击进入课程
  await page.evaluate((name) => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes(name)) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  }, COURSE_NAME);
  
  await delay(4000);
  console.log('✅ 已进入课程\n');
  
  // 6. 点击第一个学生进入批改页面
  console.log('阶段3: 进入批改页面...');
  
  // 获取第一个学生
  const firstStudent = analysisResults[0];
  
  // 点击第一个学生
  await page.evaluate((studentName) => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label') || '';
      if (label.includes(studentName) && label.includes('2026-')) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  }, firstStudent.student);
  
  await delay(4000);
  console.log('✅ 已进入批改页面\n');
  
  // 7. 下载所有学生作业
  console.log('阶段4: 下载学生作业...');
  
  for (const studentAnalysis of analysisResults) {
    const studentName = studentAnalysis.student;
    const keNeiCount = studentAnalysis.keNei;
    const aoShuCount = studentAnalysis.aoShu;
    const totalCount = keNeiCount + aoShuCount;
    
    console.log(`\n----------------------------------------`);
    console.log(`下载: ${studentName}`);
    console.log(`课内: ${keNeiCount}张, 奥数: ${aoShuCount}张`);
    console.log(`----------------------------------------`);
    
    // 创建目录
    const studentDir = path.join(OUTPUT_DIR, COURSE_NAME, studentName);
    const keNeiDir = path.join(studentDir, '课内');
    const aoShuDir = path.join(studentDir, '奥数');
    
    if (!fs.existsSync(keNeiDir)) fs.mkdirSync(keNeiDir, { recursive: true });
    if (!fs.existsSync(aoShuDir)) fs.mkdirSync(aoShuDir, { recursive: true });
    
    // 下载课内作业
    for (let i = 1; i <= keNeiCount; i++) {
      const savePath = path.join(keNeiDir, `图片${i}.jpg`);
      
      // 点击"查看原图"
      await page.evaluate(() => {
        const elements = document.querySelectorAll('flt-semantics');
        if (elements[8]) {
          elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }
      });
      
      await delay(3000);
      
      // 获取图片URL并下载
      const allPages = context.pages();
      const newPage = allPages.find(p => p !== page && p.url().includes('img.banjixiaoguanjia.com'));
      
      if (newPage) {
        const imageUrl = newPage.url();
        try {
          execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
          console.log(`  ✅ 课内 图片${i}.jpg`);
        } catch (e) {
          console.log(`  ❌ 课内 图片${i}.jpg 下载失败`);
        }
        await newPage.close();
        await delay(500);
      }
      
      // 切换到下一张
      if (i < totalCount) {
        await page.keyboard.press('ArrowRight');
        await delay(1500);
      }
    }
    
    // 下载奥数作业
    for (let i = 1; i <= aoShuCount; i++) {
      const savePath = path.join(aoShuDir, `图片${i}.jpg`);
      
      // 点击"查看原图"
      await page.evaluate(() => {
        const elements = document.querySelectorAll('flt-semantics');
        if (elements[8]) {
          elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        }
      });
      
      await delay(3000);
      
      // 获取图片URL并下载
      const allPages = context.pages();
      const newPage = allPages.find(p => p !== page && p.url().includes('img.banjixiaoguanjia.com'));
      
      if (newPage) {
        const imageUrl = newPage.url();
        try {
          execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
          console.log(`  ✅ 奥数 图片${i}.jpg`);
        } catch (e) {
          console.log(`  ❌ 奥数 图片${i}.jpg 下载失败`);
        }
        await newPage.close();
        await delay(500);
      }
      
      // 切换到下一张
      if (i < aoShuCount) {
        await page.keyboard.press('ArrowRight');
        await delay(1500);
      }
    }
    
    // 核对
    const keNeiFiles = fs.readdirSync(keNeiDir).filter(f => f.endsWith('.jpg'));
    const aoShuFiles = fs.readdirSync(aoShuDir).filter(f => f.endsWith('.jpg'));
    
    console.log(`  核对: 课内 ${keNeiFiles.length}/${keNeiCount}, 奥数 ${aoShuFiles.length}/${aoShuCount}`);
    
    // 切换到下一个学生
    if (studentAnalysis !== analysisResults[analysisResults.length - 1]) {
      console.log(`  切换到下一个学生...`);
      
      // 获取当前学生索引
      const currentIndex = analysisResults.findIndex(s => s.student === studentName);
      const nextStudent = analysisResults[currentIndex + 1];
      
      // 动态获取学生列表并点击
      const students = await page.evaluate(() => {
        const elements = document.querySelectorAll('flt-semantics');
        const list = [];
        for (let i = 0; i < elements.length; i++) {
          const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
          if (text.length > 0 && text.length < 20 && 
              !text.includes('作业') && !text.includes('图片') && 
              !text.includes('查看') && !text.includes('详情') &&
              !text.includes('2026-') && !text.includes('课内') &&
              !text.includes('奥数') && !text.includes('返回') &&
              !text.includes('已点评') && !text.includes('待点评') &&
              !text.includes('没有更多') && !text.includes('收起') &&
              !text.includes('点评') && !text.includes('全部') &&
              !text.includes('未点评') && !text.includes('帮助') &&
              !text.includes('快捷键') && !text.includes('设置') &&
              !text.includes('画笔') && !text.includes('旋转') &&
              !text.includes('文字') && !text.includes('橡皮擦') &&
              !text.includes('撤销') && !text.includes('放大') &&
              !text.includes('缩小') && !text.includes('上一张') &&
              !text.includes('下一张') && !text.includes('保存')) {
            list.push({ index: i, name: text.trim() });
          }
        }
        return list;
      });
      
      const targetInfo = students.find(s => s.name === nextStudent.student);
      if (targetInfo) {
        await page.evaluate((index) => {
          const elements = document.querySelectorAll('flt-semantics');
          if (elements[index]) {
            elements[index].dispatchEvent(new MouseEvent('click', { bubbles: true }));
          }
        }, targetInfo.index);
        
        await delay(4000);
        console.log(`  ✅ 已切换到 ${nextStudent.student}`);
      }
    }
  }
  
  console.log(`\n========================================`);
  console.log(`  所有学生作业下载完成！`);
  console.log(`  输出目录: ${path.join(OUTPUT_DIR, COURSE_NAME)}`);
  console.log(`========================================\n`);
  
  // 回到首页
  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  console.log('✅ 已回到首页\n');
  
  console.log('⏳ 下载完成，浏览器保持打开...');
  console.log('ℹ️ 按 Ctrl+C 关闭此脚本\n');
  
  // 保持运行
  setInterval(() => {}, 5000);
  await new Promise(() => {});
}

// 执行
downloadHomework().catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});
