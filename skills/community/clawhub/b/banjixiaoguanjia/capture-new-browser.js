const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 加载 .zshrc 中的环境变量
function loadEnvFromZshrc() {
  try {
    const zshrcPath = path.join(require('os').homedir(), '.zshrc');
    if (fs.existsSync(zshrcPath)) {
      const content = fs.readFileSync(zshrcPath, 'utf-8');
      const envMatches = content.match(/export\s+([A-Z_]+)=(.+)/g);
      if (envMatches) {
        envMatches.forEach(line => {
          const match = line.match(/export\s+([A-Z_]+)=(.+)/);
          if (match && !process.env[match[1]]) {
            process.env[match[1]] = match[2].replace(/^["']|["']$/g, '');
          }
        });
      }
    }
  } catch (e) {
    // 忽略错误
  }
}

// 启动时加载环境变量
loadEnvFromZshrc();

// 等待函数
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function captureHomework(courseName) {
  console.log('\n' + '='.repeat(60));
  console.log(`  班级小管家作业截图`);
  console.log(`  课程: ${courseName}`);
  console.log('='.repeat(60) + '\n');

  const outputDir = path.join(require('os').homedir(), 'Desktop', courseName);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log('1. 检查是否已有打开的班级小管家...');
  
  let browser;
  let page;
  let reused = false;
  
  // 尝试连接已打开的 Chrome
  try {
    browser = await chromium.connectOverCDP('http://localhost:9222');
    const contexts = browser.contexts();
    
    if (contexts.length > 0) {
      // 查找是否有班级小管家的页面
      for (const context of contexts) {
        const pages = context.pages();
        const bjxgjPage = pages.find(p => p.url().includes('banjixiaoguanjia'));
        if (bjxgjPage) {
          page = bjxgjPage;
          reused = true;
          console.log('   ✅ 找到已打开的班级小管家页面');
          break;
        }
      }
    }
    
    if (!reused) {
      console.log('   已连接的浏览器没有班级小管家页面，使用当前浏览器打开新页面...');
      
      // 使用已连接的浏览器创建新页面
      const context = browser.contexts()[0] || await browser.newContext({
        viewport: { width: 1280, height: 1000 }
      });
      
      page = await context.newPage();
      console.log('   ✅ 在已连接浏览器中创建新页面');
    }
  } catch (e) {
    // 无法连接，启动新浏览器
    console.log('   未找到已打开的浏览器，启动新浏览器...');
    
    // 使用持久化上下文，保存登录状态
    const userDataDir = path.join(require('os').homedir(), '.banjixiaoguanjia', 'chrome-profile');
    if (!fs.existsSync(userDataDir)) {
      fs.mkdirSync(userDataDir, { recursive: true });
    }
    
    // 使用 launchPersistentContext 而不是 launch + newContext
    const context = await chromium.launchPersistentContext(userDataDir, {
      headless: false,
      channel: 'chrome',
      args: [
        '--remote-debugging-port=9222',
        '--window-size=1280,1000'
      ],
      viewport: { width: 1280, height: 1000 }
    });
    
    browser = context.browser();
    page = context.pages()[0] || await context.newPage();
    console.log('   ✅ 新浏览器已启动（已开启调试端口 9222，使用持久化配置文件）');
    console.log('   📁 用户数据目录:', userDataDir);
  }
  
  console.log('');
  console.log('2. 打开班级小管家...');
  
  if (!reused) {
    await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(3000);
  } else {
    console.log('   ✅ 使用已有页面，导航到首页...');
    await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(5000);
  }
  
  console.log('   ✅ 页面已加载');
  console.log('   等待页面完全加载...');
  await sleep(5000);
  console.log('   页面加载完成\n');
  console.log('3. 启用辅助功能...');
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await sleep(3000);
  
  console.log('   ✅ 辅助功能已启用\n');
  console.log('4. 查找课程...');
  
  // 滚动查找课程
  let found = false;
  let scrollAttempts = 0;
  const maxScrollAttempts = 30;
  
  // 先等待一下确保课程列表加载
  await sleep(3000);
  
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
        if (label && (label.includes('第') || label.includes('年级') || label.includes('班'))) {
          lastCourseEl = el;
        }
      }
      
      if (lastCourseEl) {
        lastCourseEl.scrollIntoView({ block: 'start' });
      }
    });
    
    await sleep(2000);
    scrollAttempts++;
    process.stdout.write(`   滚动查找中... (${scrollAttempts}/${maxScrollAttempts})\r`);
  }
  
  if (!found) {
    console.log('\n❌ 未找到课程:', courseName);
    await browser.close();
    return;
  }
  
  console.log('\n5. 点击进入课程...');
  
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
  console.log('6. 收集学生列表...');
  
  const students = [];
  let scrollCount = 0;
  const maxScrolls = 10;
  let noNewStudentCount = 0;  // 连续没有发现新学生的次数
  const maxNoNewStudent = 2;  // 连续2次没有发现新学生就退出
  
  while (scrollCount < maxScrolls && noNewStudentCount < maxNoNewStudent) {
    const previousStudentCount = students.length;
    
    // 获取当前视图中的学生
    const result = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      const students = [];
      
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        // 学生标签特征：包含日期2026-，并且包含课内或奥数
        if (label && label.includes('2026-') && (label.includes('课内') || label.includes('奥数'))) {
          const lines = label.split('\n');
          const name = lines[0].trim();
          const hasCorrection = label.includes('改正如下');
          
          if (name && !students.find(s => s.name === name)) {
            students.push({ name, fullLabel: label, hasCorrection });
          }
        }
      }
      
      return { students };
    });
    
    // 添加新发现的学生
    let newStudentCount = 0;
    for (const student of result.students) {
      if (!students.find(s => s.name === student.name)) {
        students.push(student);
        newStudentCount++;
      }
    }
    
    // 检查是否发现新学生
    if (newStudentCount === 0) {
      noNewStudentCount++;
    } else {
      noNewStudentCount = 0;  // 重置计数器
    }
    
    // 检查是否显示"没有更多了"
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
      break;
    }
    
    // 继续滚动
    await page.evaluate(() => {
      const container = document.querySelector('[style*="overflow-y"]');
      if (container) {
        container.scrollTop += 400;
      }
    });
    await sleep(1000);  // 等待页面加载
    scrollCount++;
  }
  
  console.log(`   ✅ 找到 ${students.length} 个学生`);
  students.forEach((s, i) => {
    const correctionMark = s.hasCorrection ? ' [有改正]' : '';
    console.log(`      ${i + 1}. ${s.name}${correctionMark}`);
  });
  console.log('');
  
  // 【关键】重新进入页面，从第一个学生开始按顺序截图
  console.log('7. 重新进入课程页面，按顺序截图...');
  
  if (reused) {
    // 如果复用了浏览器，直接滚动到页面顶部，不重新导航
    console.log('   复用浏览器，滚动到页面顶部...');
    await page.evaluate(() => {
      const container = document.querySelector('[style*="overflow-y"]');
      if (container) {
        container.scrollTop = 0;
      }
    });
    await sleep(2000);
    console.log('   ✅ 已在课程页面顶部\n');
  } else {
    // 新浏览器，需要重新进入课程
    // 重新进入页面（从顶部开始）
    await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle', timeout: 60000 });
    await sleep(3000);
    
    // 启用辅助功能
    await page.evaluate(() => {
      const el = document.querySelector('flt-semantics-placeholder');
      if (el) el.click();
    });
    await sleep(2000);
    
    // 查找课程
    for (let i = 0; i < 15; i++) {
      const found = await page.evaluate((name) => {
        const elements = document.querySelectorAll('flt-semantics[aria-label]');
        for (const el of elements) {
          const label = el.getAttribute('aria-label');
          if (label && label.includes(name)) return true;
        }
        // 滚动查找
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
      await sleep(1500);
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
    }, courseName);
    
    await sleep(5000);
    console.log('   ✅ 已重新进入课程详情页\n');
  }
  
  // 按顺序截图每个学生
  const screenshots = [];
  const scrollStep = 400;
  
  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    console.log(`   [${i + 1}/${students.length}] ${student.name}`);
    
    // 截图当前学生
    const screenshotPath = path.join(outputDir, `${student.name}.png`);
    await page.screenshot({ path: screenshotPath, fullPage: false, timeout: 60000 });
    screenshots.push({ name: student.name, path: screenshotPath, hasCorrection: student.hasCorrection });
    console.log(`      ✅ 已保存: ${student.name}.png`);
    
    // 【改正作业截图】如果有改正补交，额外滚动截图
    if (student.hasCorrection) {
      console.log(`      检测到改正补交，额外滚动截图...`);
      await page.evaluate((step) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) container.scrollTop += step;
      }, scrollStep);
      await sleep(1500);
      
      const correctionPath = path.join(outputDir, `${student.name}_改正.png`);
      await page.screenshot({ path: correctionPath, fullPage: false, timeout: 60000 });
      console.log(`      ✅ 已保存: ${student.name}_改正.png`);
    }
    
    // 如果不是最后一个学生，滚动到下一个
    if (i < students.length - 1) {
      console.log(`      滚动到下一个学生...`);
      await page.evaluate((step) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) container.scrollTop += step;
      }, scrollStep);
      await sleep(1000);
    }
  }
  
  console.log(`\n   ✅ 截图完成，共 ${screenshots.length} 个学生\n`);
  
  // AI 分析
  console.log('9. AI 分析作业数量...');
  
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
  
  // 保持浏览器打开，方便用户查看
  console.log('ℹ️ 浏览器保持打开状态，您可以手动查看和批改');
  console.log('ℹ️ 完成后请手动关闭浏览器\n');
  
  console.log('✅ 全部完成！');
  console.log(`📁 输出目录: ${outputDir}\n`);
  
  // 保持脚本运行，防止浏览器被关闭
  console.log('⏳ 等待用户手动关闭浏览器...');
  
  // 使用 setInterval 保持事件循环活跃，确保 Playwright 连接不被断开
  const keepAlive = setInterval(() => {
    // 定期检查浏览器是否还连接
    if (browser && browser.isConnected) {
      try {
        const connected = browser.isConnected();
        if (!connected) {
          console.log('浏览器已断开连接');
          clearInterval(keepAlive);
          process.exit(0);
        }
      } catch (e) {
        // 忽略错误
      }
    }
  }, 5000);
  
  // 无限等待，但保持事件循环活跃
  await new Promise(() => {});
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
  console.log('用法: node capture-new-browser.js "课程名称"');
  console.log('示例: node capture-new-browser.js "二下(第38节)"');
  process.exit(1);
}

captureHomework(courseName).catch(console.error);
