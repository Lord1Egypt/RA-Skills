const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureHomework(courseName) {
  console.log('\n' + '='.repeat(60));
  console.log(`  班级小管家作业截图`);
  console.log(`  课程: ${courseName}`);
  console.log('='.repeat(60) + '\n');

  const outputDir = path.join(require('os').homedir(), 'Desktop', courseName);
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }

  console.log('1. 连接 Chrome...');
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
  console.log('2. 导航到首页...');
  
  // 导航到首页
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
  await sleep(3000);
  
  console.log('   ✅ 已回到首页\n');
  console.log('3. 启用辅助功能...');
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await sleep(2000);
  
  console.log('   ✅ 辅助功能已启用\n');
  console.log('4. 查找课程...');
  
  // 滚动查找课程
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
    
    // 滚动
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
    console.log('   ❌ 未找到课程');
    await browser.close();
    return;
  }
  
  console.log('\n5. 进入课程...');
  
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
  console.log('   ✅ 已进入课程\n');
  
  // 收集学生列表 - 修正查找条件
  console.log('6. 收集学生列表...');
  const students = [];
  
  for (let scrollCount = 0; scrollCount < 30; scrollCount++) {
    const currentStudents = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      const list = [];
      
      for (const el of elements) {
        const text = el.getAttribute('aria-label') || '';
        // 修正：查找包含日期和作业信息的学生条目
        if (text.includes('2026-') && text.includes('课内') && text.length > 50) {
          const lines = text.split('\n').filter(l => l.trim());
          if (lines.length >= 2) {
            const name = lines[0].trim();
            // 排除重复
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
        // 检查是否有"改正如下"标签
        const hasCorrection = s.fullLabel && (s.fullLabel.includes('改正如下') || s.fullLabel.includes('改正'));
        if (hasCorrection) {
          s.hasCorrection = true;
          console.log(`       (${s.name} 有改正补交作业)`);
        }
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
  
  if (students.length === 0) {
    console.log('❌ 未找到学生，请检查课程是否正确');
    await browser.close();
    return;
  }
  
  // 【关键】重新进入页面，从第一个学生开始按顺序截图
  console.log('7. 重新进入课程页面，按顺序截图...');
  
  // 重新进入页面（从顶部开始）
  await page.goto('https://service.banjixiaoguanjia.com/appweb/', { waitUntil: 'networkidle' });
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
  
  // 按顺序截图每个学生
  const scrollStep = 400;
  
  for (let i = 0; i < students.length; i++) {
    const student = students[i];
    console.log(`   [${i + 1}/${students.length}] ${student.name}`);
    
    // 截图当前学生（增加超时时间）
    const filepath = path.join(outputDir, `${student.name}.png`);
    await page.screenshot({ path: filepath, fullPage: false, timeout: 60000 });
    console.log(`      ✅ 已保存: ${student.name}.png`);
    
    // 【改正作业截图】如果有改正补交，额外滚动截图
    if (student.hasCorrection) {
      console.log(`      检测到改正补交，额外滚动截图...`);
      await page.evaluate((step) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) container.scrollTop += step;
      }, scrollStep);
      await sleep(1500);
      
      // 截图改正部分（增加超时时间）
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
      await sleep(1500);
    }
  }
  
  console.log(`   ✅ 截图完成，保存到: ${outputDir}\n`);
  
  // AI分析
  console.log('8. AI分析作业数量...');
  
  const apiKey = process.env.DASHSCOPE_API_KEY;
  if (!apiKey) {
    console.log('   ⚠️ 未设置 DASHSCOPE_API_KEY，跳过AI分析');
    await browser.close();
    return;
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

注意：如果图片中有"改正如下"或"改正"的内容，这部分是改正补交的作业，不要统计到课内或奥数作业数量中。

分析出不同作业类型下的缩略图的图片数量（只统计原始作业，不统计改正部分）。

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
      const { execSync } = require('child_process');
      const result = execSync(`python3 "${tempScript}"`, { 
        encoding: 'utf-8',
        timeout: 120000
      });
      fs.unlinkSync(tempScript);
      
      // 解析结果
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
  
  // 保存分析结果
  const analysisPath = path.join(outputDir, 'analysis-results.json');
  fs.writeFileSync(analysisPath, JSON.stringify(analysisResults, null, 2), 'utf-8');
  
  console.log('\n   ✅ AI分析完成\n');
  console.log('分析结果汇总:');
  for (const r of analysisResults) {
    console.log(`   - ${r.student}: 课内${r.keNeiCount}张, 奥数${r.aoShuCount}张`);
  }
  
  await browser.close();
  
  console.log('\n' + '='.repeat(60));
  console.log('  ✅ 截图和分析完成！');
  console.log('='.repeat(60) + '\n');
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// 主入口
const courseName = process.argv[2] || '二下(第36节)';
captureHomework(courseName).catch(console.error);
