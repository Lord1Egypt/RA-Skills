const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');

// 启动 Chrome 调试模式
async function startChromeDebugger() {
  console.log('🚀 正在启动 Chrome 调试模式...');
  
  const isWindows = process.platform === 'win32';
  const isMac = process.platform === 'darwin';
  
  let chromePath;
  let args;
  
  if (isWindows) {
    chromePath = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
    args = [
      '--remote-debugging-port=9222',
      '--window-size=1280,800',
      'https://service.banjixiaoguanjia.com/appweb/'
    ];
  } else if (isMac) {
    chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
    args = [
      '--remote-debugging-port=9222',
      '--window-size=1280,800',
      'https://service.banjixiaoguanjia.com/appweb/'
    ];
  } else {
    // Linux
    chromePath = 'google-chrome';
    args = [
      '--remote-debugging-port=9222',
      '--window-size=1280,800',
      'https://service.banjixiaoguanjia.com/appweb/'
    ];
  }
  
  // 检查 Chrome 是否已经在运行
  try {
    const response = await fetch('http://localhost:9222/json/version');
    if (response.ok) {
      console.log('   ✅ Chrome 调试模式已在运行');
      return true;
    }
  } catch (e) {
    // Chrome 未启动，继续启动
  }
  
  // 启动 Chrome
  return new Promise((resolve, reject) => {
    const chrome = spawn(chromePath, args, {
      detached: true,
      stdio: 'ignore'
    });
    
    chrome.on('error', (err) => {
      console.error('❌ 启动 Chrome 失败:', err.message);
      reject(err);
    });
    
    // 等待 Chrome 启动完成
    let attempts = 0;
    const maxAttempts = 30;
    
    const checkConnection = setInterval(async () => {
      attempts++;
      try {
        const response = await fetch('http://localhost:9222/json/version');
        if (response.ok) {
          clearInterval(checkConnection);
          console.log('   ✅ Chrome 调试模式已启动 (端口 9222，窗口 1280x800)');
          resolve(true);
        }
      } catch (e) {
        if (attempts >= maxAttempts) {
          clearInterval(checkConnection);
          reject(new Error('Chrome 启动超时，请检查 Chrome 是否已安装'));
        }
      }
    }, 1000);
  });
}

// 等待函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function captureHomework(courseName) {
  console.log('\n' + '='.repeat(60));
  console.log(`  班级小管家作业截图`);
  console.log(`  课程: ${courseName}`);
  console.log('='.repeat(60) + '\n');

  // 步骤1: 启动 Chrome
  try {
    await startChromeDebugger();
    console.log('');
  } catch (err) {
    console.error('❌ 无法启动 Chrome:', err.message);
    console.log('\n请手动启动 Chrome 调试模式：');
    console.log('"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --window-size=1280,800');
    return;
  }

  const outputDir = path.join(require('os').homedir(), 'Desktop', courseName);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log('2. 连接 Chrome...');
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0];
  const pages = context.pages();
  
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('❌ 未找到班级小管家页面');
    await browser.close();
    return;
  }
  
  console.log('   ✅ 已连接\n');
  console.log('3. 导航到首页...');
  
  // 导航到首页
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await sleep(3000);
  
  console.log('   ✅ 已回到首页\n');
  console.log('4. 启用辅助功能...');
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await sleep(2000);
  
  console.log('   ✅ 辅助功能已启用\n');
  console.log('5. 查找课程...');
  
  // 滚动查找课程
  let found = false;
  let scrollAttempts = 0;
  const maxScrollAttempts = 20;
  
  while (!found && scrollAttempts < maxScrollAttempts) {
    // 在当前视图查找课程
    const courseInfo = await page.evaluate((name) => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes(name)) {
          return { found: true, label, hasCorrection: label.includes('改正如下') };
        }
      }
      return { found: false };
    }, courseName);
    
    if (courseInfo.found) {
      console.log(`   ✅ 找到课程: ${courseInfo.label}`);
      found = true;
      break;
    }
    
    // 滚动到最后一个课程，触发加载更多
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      let lastCourseEl = null;
      
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) {
          lastCourseEl = el;
        }
      }
      
      if (lastCourseEl) {
        lastCourseEl.scrollIntoView({ block: 'start' });
      }
    });
    
    await sleep(1500);
    scrollAttempts++;
    process.stdout.write(`   滚动查找中... (${scrollAttempts}/${maxScrollAttempts})\r`);
  }
  
  if (!found) {
    console.log('\n❌ 未找到课程:', courseName);
    await browser.close();
    return;
  }
  
  console.log('\n6. 点击进入课程...');
  
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
  }, courseName);
  
  await sleep(4000);
  console.log('   ✅ 已进入课程\n');
  
  // 收集学生列表
  console.log('7. 收集学生列表...');
  
  const students = [];
  let hasMore = true;
  let scrollCount = 0;
  const maxScrolls = 50;
  
  while (hasMore && scrollCount < maxScrolls) {
    const result = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      const students = [];
      let hasMoreContent = false;
      
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('2026-') && label.includes('课内')) {
          const lines = label.split('\n');
          const name = lines[0].trim();
          const hasCorrection = label.includes('改正如下');
          
          if (name && !students.find(s => s.name === name)) {
            students.push({ name, fullLabel: label, hasCorrection });
          }
        }
        if (label && label.includes('没有更多了')) {
          hasMoreContent = false;
        } else if (label && (label.includes('第') || label.includes('年级'))) {
          hasMoreContent = true;
        }
      }
      
      return { students, hasMoreContent };
    });
    
    // 添加新发现的学生
    for (const student of result.students) {
      if (!students.find(s => s.name === student.name)) {
        students.push(student);
      }
    }
    
    // 检查是否还有更多
    const hasNoMore = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('没有更多了')) {
          return true;
        }
      }
      return false;
    });
    
    if (hasNoMore) {
      hasMore = false;
    } else {
      // 继续滚动
      await page.evaluate(() => {
        const container = document.querySelector('[style*="overflow-y"]');
        if (container) {
          container.scrollTop += 400;
        }
      });
      await sleep(1000);
      scrollCount++;
    }
  }
  
  console.log(`   ✅ 找到 ${students.length} 个学生`);
  students.forEach((s, i) => {
    const correctionMark = s.hasCorrection ? ' [有改正]' : '';
    console.log(`      ${i + 1}. ${s.name}${correctionMark}`);
  });
  console.log('');
  
  // 重新进入页面，按顺序截图
  console.log('8. 重新进入页面准备截图...');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await sleep(3000);
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await sleep(2000);
  
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
  }, courseName);
  
  await sleep(4000);
  console.log('   ✅ 已重新进入课程\n');
  
  // 截图每个学生
  console.log('9. 截图学生作业...');
  
  const screenshots = [];
  const scrollStep = 400;
  
  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    
    // 复位滚动位置
    await page.evaluate(() => {
      const container = document.querySelector('[style*="overflow-y"]');
      if (container) {
        container.scrollTop = -1000;
      }
    });
    await sleep(500);
    
    // 滚动到指定位置
    const scrollTop = i * scrollStep;
    await page.evaluate((top) => {
      const container = document.querySelector('[style*="overflow-y"]');
      if (container) {
        container.scrollTop = top;
      }
    }, scrollTop);
    await sleep(1000);
    
    // 截图
    const screenshotPath = path.join(outputDir, `${student.name}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false });
    screenshots.push({ name: student.name, path: screenshotPath, hasCorrection: student.hasCorrection });
    
    console.log(`   ✅ [${i + 1}/${students.length}] ${student.name}`);
    
    // 如果有改正，额外截图改正部分
    if (student.hasCorrection) {
      await sleep(500);
      const correctionPath = path.join(outputDir, `${student.name}_改正.png`);
      await page.screenshot({ path: correctionPath, fullPage: false });
      console.log(`      📌 已截图改正部分: ${student.name}_改正.png`);
    }
  }
  
  console.log(`\n   ✅ 截图完成，共 ${screenshots.length} 个学生\n`);
  
  // AI 分析
  console.log('10. AI 分析作业数量...');
  
  const analysisResults = [];
  
  for (let i = 0; i < screenshots.length; i++) {
    const { name, path: screenshotPath, hasCorrection } = screenshots[i];
    process.stdout.write(`    分析中: ${name}...\r`);
    
    // 读取图片
    const imageBuffer = fs.readFileSync(screenshotPath);
    const base64Image = imageBuffer.toString('base64');
    
    // 调用 AI 分析
    try {
      const analysis = await analyzeHomework(base64Image, name, hasCorrection);
      analysisResults.push({
        student: name,
        keNei: analysis.keNei,
        aoShu: analysis.aoShu,
        hasCorrection: hasCorrection
      });
      console.log(`    ✅ ${name}: 课内${analysis.keNei}张, 奥数${analysis.aoShu}张${hasCorrection ? ' (有改正)' : ''}`);
    } catch (err) {
      console.log(`    ❌ ${name}: 分析失败 - ${err.message}`);
      analysisResults.push({
        student: name,
        keNei: 0,
        aoShu: 0,
        error: err.message
      });
    }
  }
  
  // 保存分析结果
  const resultPath = path.join(outputDir, 'analysis-results.json');
  fs.writeFileSync(resultPath, JSON.stringify(analysisResults, null, 2));
  
  console.log(`\n   ✅ 分析完成，结果已保存: ${resultPath}\n`);
  
  // 打印汇总
  console.log('='.repeat(60));
  console.log('  作业数量汇总');
  console.log('='.repeat(60));
  
  let totalKeNei = 0;
  let totalAoShu = 0;
  
  for (const result of analysisResults) {
    const correctionMark = result.hasCorrection ? ' [改]' : '';
    console.log(`  ${result.student.padEnd(10)} 课内: ${result.keNei.toString().padStart(2)}张  奥数: ${result.aoShu.toString().padStart(2)}张${correctionMark}`);
    totalKeNei += result.keNei;
    totalAoShu += result.aoShu;
  }
  
  console.log('-'.repeat(60));
  console.log(`  总计       课内: ${totalKeNei.toString().padStart(2)}张  奥数: ${totalAoShu.toString().padStart(2)}张`);
  console.log('='.repeat(60) + '\n');
  
  await browser.close();
  
  console.log('✅ 全部完成！');
  console.log(`📁 输出目录: ${outputDir}\n`);
}

// AI 分析函数
async function analyzeHomework(base64Image, studentName, hasCorrection) {
  const apiKey = process.env.DASHSCOPE_API_KEY;
  
  if (!apiKey) {
    throw new Error('未设置 DASHSCOPE_API_KEY 环境变量');
  }
  
  const correctionPrompt = hasCorrection 
    ? '注意：截图中包含"改正如下"的部分，这是学生补交的改正作业，在统计数量时不需要计入。' 
    : '';
  
  const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'qwen-vl-max-latest',
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'text',
              text: `请分析这张学生作业截图，统计课内作业和奥数作业的数量。

${correctionPrompt}

请按以下格式回复：
课内作业：X张
奥数作业：Y张

只需要返回这两行，不要其他内容。`
            },
            {
              type: 'image_url',
              image_url: { url: `data:image/png;base64,${base64Image}` }
            }
          ]
        }
      ]
    })
  });
  
  if (!response.ok) {
    throw new Error(`API 请求失败: ${response.status}`);
  }
  
  const data = await response.json();
  const content = data.choices[0].message.content;
  
  // 解析结果
  const keNeiMatch = content.match(/课内作业[:：]\s*(\d+)/);
  const aoShuMatch = content.match(/奥数作业[:：]\s*(\d+)/);
  
  return {
    keNei: keNeiMatch ? parseInt(keNeiMatch[1]) : 0,
    aoShu: aoShuMatch ? parseInt(aoShuMatch[1]) : 0
  };
}

// 主函数
const courseName = process.argv[2];

if (!courseName) {
  console.log('用法: node capture-auto-start.js "课程名称"');
  console.log('示例: node capture-auto-start.js "二下(第38节)"');
  process.exit(1);
}

captureHomework(courseName).catch(console.error);
