const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync, spawn } = require('child_process');
const os = require('os');

// 配置
const CONFIG = {
  chromePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
  debugPort: 9222,
  baseUrl: 'https://service.banjixiaoguanjia.com/appweb/',
  maxRetries: 3,
  timeouts: {
    navigation: 30000,
    element: 10000,
    scroll: 1500,
    click: 5000
  }
};

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 检查 Chrome 是否已以调试模式运行
async function isChromeRunning() {
  try {
    const response = await fetch(`http://localhost:${CONFIG.debugPort}/json/version`);
    return response.ok;
  } catch {
    return false;
  }
}

// 启动 Chrome 调试模式
async function startChrome() {
  console.log('🚀 启动 Chrome 调试模式...');
  
  const tempProfile = path.join(os.tmpdir(), 'chrome-dev-profile');
  if (!fs.existsSync(tempProfile)) {
    fs.mkdirSync(tempProfile, { recursive: true });
  }
  
  // 启动 Chrome
  const chromeProcess = spawn(CONFIG.chromePath, [
    `--remote-debugging-port=${CONFIG.debugPort}`,
    `--user-data-dir=${tempProfile}`,
    CONFIG.baseUrl
  ], {
    detached: true,
    stdio: 'ignore'
  });
  
  chromeProcess.unref();
  
  // 等待 Chrome 启动
  let attempts = 0;
  while (attempts < 30) {
    if (await isChromeRunning()) {
      console.log('   ✅ Chrome 已启动\n');
      return true;
    }
    await sleep(1000);
    attempts++;
  }
  
  throw new Error('Chrome 启动超时');
}

// 连接 Chrome
async function connectBrowser() {
  console.log('1. 连接 Chrome...');
  
  // 如果 Chrome 未运行，自动启动
  if (!await isChromeRunning()) {
    await startChrome();
  }
  
  const browser = await chromium.connectOverCDP(`http://localhost:${CONFIG.debugPort}`);
  console.log('   ✅ 已连接\n');
  return browser;
}

// 获取班级小管家页面
async function getBanjixiaoguanjiaPage(browser) {
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    page = await context.newPage();
    await page.goto(CONFIG.baseUrl, { waitUntil: 'networkidle' });
  }
  
  return page;
}

// 导航到首页
async function navigateToHome(page) {
  console.log('2. 导航到首页...');
  await page.goto(CONFIG.baseUrl, { waitUntil: 'networkidle' });
  await sleep(3000);
  console.log('   ✅ 已回到首页\n');
}

// 启用辅助功能
async function enableAccessibility(page) {
  console.log('3. 启用辅助功能...');
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await sleep(2000);
  console.log('   ✅ 辅助功能已启用\n');
}

// 查找并进入课程
async function findAndEnterCourse(page, courseName) {
  console.log('4. 查找课程...');
  
  let found = false;
  for (let i = 0; i < 25; i++) {
    found = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) {
          return true;
        }
      }
      return false;
    }, courseName);
    
    if (found) {
      console.log('   ✅ 找到课程');
      break;
    }
    
    // 滚动查找
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) {
          last = el;
        }
      }
      if (last) last.scrollIntoView({ block: 'start' });
    });
    
    await sleep(1500);
  }
  
  if (!found) {
    throw new Error(`未找到课程: ${courseName}`);
  }
  
  console.log('\n5. 进入课程...');
  
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
  
  await sleep(5000);
  console.log('   ✅ 已进入课程\n');
}

// 收集学生列表
async function collectStudents(page) {
  console.log('6. 收集学生列表...');
  const students = [];
  
  for (let scrollCount = 0; scrollCount < 30; scrollCount++) {
    const currentStudents = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      const list = [];
      
      for (const el of elements) {
        const text = el.getAttribute('aria-label') || '';
        if (text.includes('2026-') && text.includes('课内') && text.length > 50) {
          const lines = text.split('\n').filter(l => l.trim());
          if (lines.length >= 2) {
            const name = lines[0].trim();
            if (!list.find(s => s.name === name)) {
              list.push({ name, fullLabel: text });
            }
          }
        }
      }
      return list;
    });
    
    for (const s of currentStudents) {
      if (!students.find(cs => cs.name === s.name)) {
        students.push(s);
      }
    }
    
    // 滚动
    await page.evaluate(() => {
      const container = document.querySelector('[style*="overflow-y: scroll"]');
      if (container) container.scrollTop += 400;
    });
    
    await sleep(1500);
    
    // 检查是否到底
    const hasMore = await page.evaluate(() => {
      const text = document.body.textContent;
      return !text.includes('没有更多了');
    });
    
    if (!hasMore && scrollCount > 5) break;
  }
  
  console.log(`   ✅ 收集到 ${students.length} 个学生\n`);
  return students;
}

// 截图学生作业
async function captureScreenshots(page, students, outputDir) {
  console.log('7. 截图所有学生作业...');
  
  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    console.log(`   [${i + 1}/${students.length}] ${student.name}`);
    
    await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label') || '';
        if (label.includes(name) && label.includes('2026-')) {
          el.scrollIntoView({ block: 'center' });
          break;
        }
      }
    }, student.name);
    
    await sleep(1500);
    
    const filepath = path.join(outputDir, `${student.name}.png`);
    await page.screenshot({ path: filepath, fullPage: false });
  }
  
  console.log(`   ✅ 截图完成\n`);
}

// AI 分析作业
async function analyzeHomework(students, outputDir) {
  console.log('8. AI分析作业数量...');
  
  const apiKey = process.env.DASHSCOPE_API_KEY;
  if (!apiKey) {
    console.log('   ⚠️ 未设置 DASHSCOPE_API_KEY，跳过AI分析');
    return [];
  }
  
  const analysisResults = [];
  
  for (const student of students) {
    const screenshotPath = path.join(outputDir, `${student.name}.png`);
    
    if (!fs.existsSync(screenshotPath)) continue;
    
    console.log(`   分析: ${student.name}`);
    
    const prompt = `图片中格式：
认真完成课内课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）
认真完成奥数课后作业，并及时提交作业。
[图片][图片][图片]...（数量不固定）

分析出不同作业类型下的缩略图的图片数量。

用简洁的中文回答，格式如下：
学生姓名：XXX
课内作业：X张
奥数作业：X张`;

    const base64 = fs.readFileSync(screenshotPath, { encoding: 'base64' });
    
    const pythonScript = `
# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from openai import OpenAI

client = OpenAI(
    api_key="${apiKey}",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

response = client.chat.completions.create(
    model="qwen-vl-max-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": "data:image/png;base64,${base64}"}
                },
                {
                    "type": "text",
                    "text": """${prompt}"""
                }
            ]
        }
    ]
)

print(response.choices[0].message.content)
`;

    const tempScript = path.join(outputDir, `_analyze_${student.name}.py`);
    fs.writeFileSync(tempScript, pythonScript, 'utf-8');
    
    try {
      const result = execSync(`python3 "${tempScript}"`, { 
        encoding: 'utf-8',
        timeout: 120000
      });
      fs.unlinkSync(tempScript);
      
      const keNeiMatch = result.match(/课内作业：(\d+)张/);
      const aoShuMatch = result.match(/奥数作业：(\d+)张/);
      
      analysisResults.push({
        student: student.name,
        keNeiCount: keNeiMatch ? parseInt(keNeiMatch[1]) : 0,
        aoShuCount: aoShuMatch ? parseInt(aoShuMatch[1]) : 0,
        rawAnalysis: result
      });
      
      console.log(`      ✅ 课内:${keNeiMatch?.[1] || 0}张, 奥数:${aoShuMatch?.[1] || 0}张`);
    } catch (error) {
      if (fs.existsSync(tempScript)) fs.unlinkSync(tempScript);
      console.log(`      ⚠️ 分析失败`);
      analysisResults.push({
        student: student.name,
        keNeiCount: 0,
        aoShuCount: 0,
        error: true
      });
    }
  }
  
  return analysisResults;
}

// 保存结果
async function saveResults(analysisResults, outputDir) {
  const analysisPath = path.join(outputDir, 'analysis-results.json');
  fs.writeFileSync(analysisPath, JSON.stringify(analysisResults, null, 2), 'utf-8');
  
  console.log('\n   ✅ AI分析完成\n');
  console.log('📊 分析结果汇总:');
  console.log('-'.repeat(40));
  for (const r of analysisResults) {
    console.log(`   ${r.student}: 课内${r.keNeiCount}张 | 奥数${r.aoShuCount}张`);
  }
  console.log('-'.repeat(40));
}

// 主流程
async function captureHomework(courseName) {
  console.log('\n' + '='.repeat(60));
  console.log(`  📚 班级小管家作业截图 - 全自动化`);
  console.log(`  课程: ${courseName}`);
  console.log('='.repeat(60) + '\n');

  const outputDir = path.join(os.homedir(), 'Desktop', courseName);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  let browser = null;
  
  try {
    // 1. 连接浏览器（自动启动 Chrome）
    browser = await connectBrowser();
    
    // 2. 获取页面
    const page = await getBanjixiaoguanjiaPage(browser);
    
    // 3. 导航到首页
    await navigateToHome(page);
    
    // 4. 启用辅助功能
    await enableAccessibility(page);
    
    // 5. 查找并进入课程
    await findAndEnterCourse(page, courseName);
    
    // 6. 收集学生列表
    const students = await collectStudents(page);
    
    if (students.length === 0) {
      throw new Error('未找到学生');
    }
    
    // 7. 截图
    await captureScreenshots(page, students, outputDir);
    
    // 8. AI分析
    const analysisResults = await analyzeHomework(students, outputDir);
    
    // 9. 保存结果
    await saveResults(analysisResults, outputDir);
    
    console.log('\n' + '='.repeat(60));
    console.log('  ✅ 全自动化流程完成！');
    console.log(`  📁 结果保存: ${outputDir}`);
    console.log('='.repeat(60) + '\n');
    
    return {
      success: true,
      students: students.length,
      outputDir,
      analysisResults
    };
    
  } catch (error) {
    console.error('\n❌ 错误:', error.message);
    return {
      success: false,
      error: error.message
    };
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// 命令行入口
const courseName = process.argv[2] || '二下(第36节)';
captureHomework(courseName)
  .then(result => {
    process.exit(result.success ? 0 : 1);
  })
  .catch(error => {
    console.error('致命错误:', error);
    process.exit(1);
  });

module.exports = { captureHomework };
