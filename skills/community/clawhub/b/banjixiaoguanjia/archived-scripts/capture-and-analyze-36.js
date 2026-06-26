const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

async function captureAndAnalyzeHomework(courseName, outputDir) {
  console.log('========================================');
  console.log(`  作业截图与分析 - ${courseName}`);
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
  for (let i = 0; i < 20; i++) {
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
  
  const targetCount = submittedCount || 10;
  
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
        if (label && label.length > 20 && label.includes('2026-')) {
          const lines = label.split(/\r?\n/);
          const name = lines[0].trim();
          if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
            const rect = el.getBoundingClientRect();
            if (rect.top >= -50 && rect.top < window.innerHeight) {
              list.push({ name, top: rect.top, label });
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
  for (let i = 0; i < 20; i++) {
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
  console.log(`\n✓ 截图完成，共 ${screenshots.length} 个学生`);
  console.log(`输出目录: ${outputDir}\n`);
  
  await browser.close();
  
  // ========== 第三阶段：使用 Qwen3.5-Plus 分析 ==========
  console.log('【第三阶段】使用 Qwen3.5-Plus 分析作业\n');
  
  const analysisResults = [];
  
  for (const screenshot of screenshots) {
    console.log(`分析: ${screenshot.name}`);
    
    try {
      // 使用 qwen35-plus-image-analyze 技能分析图片
      const prompt = `请分析这张班级小管家作业截图，识别以下信息：
1. 学生姓名
2. 课内作业提交数量（图片中显示"课内"相关的数字）
3. 奥数作业提交数量（图片中显示"奥数"相关的数字）

请以以下格式输出：
学生姓名：XXX
课内作业：X张
奥数作业：X张`;
      
      const result = analyzeWithQwen(screenshot.filepath, prompt);
      
      analysisResults.push({
        name: screenshot.name,
        filepath: screenshot.filepath,
        analysis: result
      });
      
      console.log(`   ✓ 分析完成\n`);
    } catch (err) {
      console.log(`   ✗ 分析失败: ${err.message}\n`);
      analysisResults.push({
        name: screenshot.name,
        filepath: screenshot.filepath,
        analysis: '分析失败'
      });
    }
  }
  
  // ========== 第四阶段：生成报告 ==========
  console.log('【第四阶段】生成分析报告\n');
  
  const reportPath = path.join(outputDir, '分析报告.txt');
  let report = `========================================
  作业提交情况分析报告
  课程: ${courseName}
  时间: ${new Date().toLocaleString('zh-CN')}
========================================

`;
  
  // 统计信息
  let totalKeNei = 0;
  let totalAoShu = 0;
  const submittedStudents = [];
  const unsubmittedStudents = [];
  
  for (const result of analysisResults) {
    const analysis = result.analysis;
    
    // 尝试提取数量
    const keNeiMatch = analysis.match(/课内作业[:：]\s*(\d+)/);
    const aoShuMatch = analysis.match(/奥数作业[:：]\s*(\d+)/);
    
    const keNeiCount = keNeiMatch ? parseInt(keNeiMatch[1]) : 0;
    const aoShuCount = aoShuMatch ? parseInt(aoShuMatch[1]) : 0;
    
    totalKeNei += keNeiCount;
    totalAoShu += aoShuCount;
    
    if (keNeiCount > 0 || aoShuCount > 0) {
      submittedStudents.push({
        name: result.name,
        keNei: keNeiCount,
        aoShu: aoShuCount
      });
    } else {
      unsubmittedStudents.push(result.name);
    }
  }
  
  // 报告内容
  report += `【总体情况】\n`;
  report += `应提交人数: ${studentList.length} 人\n`;
  report += `已提交人数: ${submittedStudents.length} 人\n`;
  report += `未提交人数: ${unsubmittedStudents.length} 人\n`;
  report += `课内作业总计: ${totalKeNei} 张\n`;
  report += `奥数作业总计: ${totalAoShu} 张\n\n`;
  
  report += `【已提交学生详情】\n`;
  if (submittedStudents.length > 0) {
    submittedStudents.forEach((s, i) => {
      report += `${i + 1}. ${s.name}: 课内 ${s.keNei} 张, 奥数 ${s.aoShu} 张\n`;
    });
  } else {
    report += `无\n`;
  }
  report += `\n`;
  
  report += `【未提交学生】\n`;
  if (unsubmittedStudents.length > 0) {
    unsubmittedStudents.forEach((name, i) => {
      report += `${i + 1}. ${name}\n`;
    });
  } else {
    report += `无\n`;
  }
  report += `\n`;
  
  report += `【原始分析数据】\n`;
  analysisResults.forEach((result, i) => {
    report += `\n--- ${result.name} ---\n`;
    report += `${result.analysis}\n`;
  });
  
  fs.writeFileSync(reportPath, report, 'utf8');
  console.log(`✓ 分析报告已保存: ${reportPath}\n`);
  
  // 打印摘要
  console.log('========================================');
  console.log('  分析结果摘要');
  console.log('========================================');
  console.log(`课程: ${courseName}`);
  console.log(`已提交: ${submittedStudents.length}/${studentList.length} 人`);
  console.log(`课内作业: ${totalKeNei} 张`);
  console.log(`奥数作业: ${totalAoShu} 张`);
  console.log('========================================');
  
  return {
    course: courseName,
    submittedCount: submittedStudents.length,
    totalStudents: studentList.length,
    keNeiTotal: totalKeNei,
    aoShuTotal: totalAoShu,
    submittedStudents,
    unsubmittedStudents,
    outputDir,
    reportPath
  };
}

// 使用 Qwen3.5-Plus 分析图片
function analyzeWithQwen(imagePath, prompt) {
  const skillPath = path.join(process.env.USERPROFILE, '.openclaw', 'workspace', 'skills', 'qwen35-plus-image-analyze', 'scripts', 'analyze_image.py');
  
  try {
    const result = execSync(
      `python "${skillPath}" "${imagePath}" "${prompt}"`,
      { encoding: 'utf8', timeout: 60000 }
    );
    return result.trim();
  } catch (err) {
    throw new Error(`Qwen分析失败: ${err.message}`);
  }
}

// 运行
captureAndAnalyzeHomework('二下(第36节)', 'C:\\Users\\Administrator\\Desktop\\二下(第36节)')
  .then(result => {
    console.log('\n任务完成！');
    console.log(`报告位置: ${result.reportPath}`);
  })
  .catch(err => {
    console.error('任务失败:', err);
    process.exit(1);
  });
