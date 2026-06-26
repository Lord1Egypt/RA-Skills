const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

async function downloadZoey() {
  console.log('========================================');
  console.log('  下载 Zoey 的作业 - 二下(第36节)');
  console.log('========================================\n');

  // 连接到 Chrome
  console.log('1. 连接 Chrome...');
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('❌ 未找到班级小管家页面');
    await browser.close();
    return;
  }
  console.log('   ✅ 已连接到 Chrome\n');

  // 获取当前学生信息
  console.log('2. 获取当前学生信息...');
  const currentInfo = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    if (elements[7]) {
      const text = elements[7].textContent || elements[7].getAttribute('aria-label') || '';
      const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
      if (match) {
        return {
          student: match[1].trim(),
          current: parseInt(match[2]),
          total: parseInt(match[3])
        };
      }
    }
    return null;
  });
  
  console.log(`   当前学生: ${currentInfo ? currentInfo.student : '未知'}`);
  console.log(`   图片位置: 第 ${currentInfo ? currentInfo.current : '?'} / ${currentInfo ? currentInfo.total : '?'} 张\n`);

  // 获取左侧学生列表
  console.log('3. 获取左侧学生列表...');
  const students = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    const studentList = [];
    
    for (let i = 0; i < elements.length; i++) {
      const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
      // 匹配学生名字（短文本，不包含特定关键词）
      if (text.length > 0 && text.length < 20 && 
          !text.includes('作业') && !text.includes('图片') && 
          !text.includes('查看') && !text.includes('详情') &&
          !text.includes('2026-') && !text.includes('课内') &&
          !text.includes('奥数') && !text.includes('返回') &&
          !text.includes('已点评') && !text.includes('待点评') &&
          !text.includes('没有更多') && !text.includes('收起') &&
          !text.includes('原图') && !text.includes('张')) {
        studentList.push({ index: i, name: text.trim() });
      }
    }
    return studentList;
  });
  
  console.log('   找到学生:', students.map(s => s.name).join(', '));
  
  // 查找 Zoey
  const zoeyStudent = students.find(s => s.name === 'Zoey');
  if (!zoeyStudent) {
    console.log('❌ 未找到 Zoey');
    await browser.close();
    return;
  }
  
  console.log(`   ✅ 找到 Zoey 在索引 ${zoeyStudent.index}\n`);

  // 点击切换到 Zoey
  console.log('4. 切换到 Zoey...');
  await page.evaluate((index) => {
    const elements = document.querySelectorAll('flt-semantics');
    if (elements[index]) {
      elements[index].dispatchEvent(new MouseEvent('click', { bubbles: true }));
    }
  }, zoeyStudent.index);
  
  await page.waitForTimeout(4000);

  // 验证切换结果
  const newInfo = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    if (elements[7]) {
      const text = elements[7].textContent || elements[7].getAttribute('aria-label') || '';
      const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
      if (match) {
        return {
          student: match[1].trim(),
          current: parseInt(match[2]),
          total: parseInt(match[3])
        };
      }
    }
    return null;
  });
  
  if (newInfo && newInfo.student === 'Zoey') {
    console.log(`   ✅ 已切换到 Zoey: 第${newInfo.current}/${newInfo.total}张\n`);
  } else {
    console.log(`   ⚠️ 切换后显示: ${newInfo ? newInfo.student : '未知'}`);
    console.log('   尝试继续...\n');
  }

  // 创建输出目录
  const outputDir = path.join(process.env.USERPROFILE, 'Desktop', '二下(第36节)', 'Zoey');
  const keNeiDir = path.join(outputDir, '课内');
  const aoShuDir = path.join(outputDir, '奥数');
  
  if (!fs.existsSync(keNeiDir)) fs.mkdirSync(keNeiDir, { recursive: true });
  if (!fs.existsSync(aoShuDir)) fs.mkdirSync(aoShuDir, { recursive: true });

  // 分析结果：Zoey 课内4张，奥数4张
  const keNeiCount = 4;
  const aoShuCount = 4;
  const totalCount = keNeiCount + aoShuCount;

  console.log('5. 下载 Zoey 的作业...');
  console.log(`   课内: ${keNeiCount}张, 奥数: ${aoShuCount}张\n`);

  // 下载课内作业
  console.log('   下载课内作业...');
  for (let i = 1; i <= keNeiCount; i++) {
    const savePath = path.join(keNeiDir, `图片${i}.jpg`);
    
    // 点击"查看原图"按钮
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[8]) {
        elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    });
    
    await page.waitForTimeout(3000);
    
    // 获取图片URL并下载
    const pages = context.pages();
    const newPage = pages.find(p => p !== page && p.url().includes('img.banjixiaoguanjia.com'));
    
    if (newPage) {
      const imageUrl = newPage.url();
      console.log(`     [${i}/${keNeiCount}] 下载: 图片${i}.jpg`);
      execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
      await newPage.close();
      await page.waitForTimeout(500);
    }
    
    // 切换到下一张
    if (i < totalCount) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(1500);
    }
  }

  // 下载奥数作业
  console.log('\n   下载奥数作业...');
  for (let i = 1; i <= aoShuCount; i++) {
    const savePath = path.join(aoShuDir, `图片${i}.jpg`);
    
    // 点击"查看原图"按钮
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[8]) {
        elements[8].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    });
    
    await page.waitForTimeout(3000);
    
    // 获取图片URL并下载
    const pages = context.pages();
    const newPage = pages.find(p => p !== page && p.url().includes('img.banjixiaoguanjia.com'));
    
    if (newPage) {
      const imageUrl = newPage.url();
      console.log(`     [${i}/${aoShuCount}] 下载: 图片${i}.jpg`);
      execSync(`curl -L -o "${savePath}" "${imageUrl}"`, { timeout: 30000 });
      await newPage.close();
      await page.waitForTimeout(500);
    }
    
    // 切换到下一张
    if (i < aoShuCount) {
      await page.keyboard.press('ArrowRight');
      await page.waitForTimeout(1500);
    }
  }

  // 核对结果
  console.log('\n6. 核对下载结果...');
  const keNeiFiles = fs.readdirSync(keNeiDir).filter(f => f.endsWith('.jpg'));
  const aoShuFiles = fs.readdirSync(aoShuDir).filter(f => f.endsWith('.jpg'));
  
  console.log(`   课内作业: 预期 ${keNeiCount} 张, 实际 ${keNeiFiles.length} 张 ${keNeiFiles.length === keNeiCount ? '✓' : '✗'}`);
  console.log(`   奥数作业: 预期 ${aoShuCount} 张, 实际 ${aoShuFiles.length} 张 ${aoShuFiles.length === aoShuCount ? '✓' : '✗'}`);
  
  if (keNeiFiles.length === keNeiCount && aoShuFiles.length === aoShuCount) {
    console.log(`   ✅ Zoey 全部下载完成`);
  } else {
    console.log(`   ⚠️ 数量不匹配`);
  }

  await browser.close();
  
  console.log('\n========================================');
  console.log('  Zoey 作业下载完成！');
  console.log(`  输出目录: ${outputDir}`);
  console.log('========================================');
}

downloadZoey().catch(console.error);
