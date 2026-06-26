const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function testSwitchStudent() {
  console.log('========================================');
  console.log('  测试: 动态获取学生列表并切换');
  console.log('========================================\n');

  // 1. 连接 Chrome
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

  // 2. 获取当前学生信息（页面顶部元素[7]）
  console.log('2. 获取当前学生信息...');
  const currentInfo = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    // 优先检查元素[7]（页面顶部标题）
    if (elements[7]) {
      const text = elements[7].textContent || elements[7].getAttribute('aria-label') || '';
      console.log('元素[7]内容:', text);
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
  
  if (currentInfo) {
    console.log(`   当前学生: ${currentInfo.student}`);
    console.log(`   图片位置: 第 ${currentInfo.current} / ${currentInfo.total} 张\n`);
  } else {
    console.log('   ⚠️ 无法获取当前学生信息\n');
  }

  // 3. 获取左侧学生列表
  console.log('3. 获取左侧学生列表...');
  const students = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    const studentList = [];
    
    for (let i = 0; i < elements.length; i++) {
      const text = elements[i].textContent || elements[i].getAttribute('aria-label') || '';
      // 匹配学生名字（短文本，不包含"作业"、"图片"等关键词）
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
          !text.includes('缩小')) {
        studentList.push({
          index: i,
          name: text.trim()
        });
      }
    }
    return studentList;
  });
  
  console.log(`   找到 ${students.length} 个学生:`);
  students.forEach(s => console.log(`     [${s.index}] ${s.name}`));
  console.log('');

  // 4. 测试切换到另一个学生
  const targetStudent = currentInfo && currentInfo.student === '球球' ? 'Zoey' : '球球';
  console.log(`4. 尝试切换到: ${targetStudent}`);
  
  const targetInfo = students.find(s => s.name === targetStudent);
  if (!targetInfo) {
    console.log(`   ❌ 未找到学生 ${targetStudent}`);
    await browser.close();
    return;
  }
  
  console.log(`   目标学生在索引: ${targetInfo.index}`);

  // 点击目标学生
  const clicked = await page.evaluate((targetName) => {
    const elements = document.querySelectorAll('flt-semantics');
    for (const el of elements) {
      const label = el.getAttribute('aria-label') || '';
      // 匹配学生名字（在列表中，通常是较短的文本，不包含"的作业"）
      if (label.includes(targetName) && label.length < 50 && !label.includes('的作业')) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return true;
      }
    }
    return false;
  }, targetStudent);
  
  if (!clicked) {
    console.log(`   ❌ 点击失败`);
    await browser.close();
    return;
  }
  console.log('   ✅ 已点击学生名字\n');

  // 5. 验证切换结果（关键！）
  console.log('5. 验证切换结果...');
  await page.waitForTimeout(4000);
  
  const newInfo = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    // 优先检查元素[7]（页面顶部标题）
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
  
  if (newInfo) {
    console.log(`   切换后学生: ${newInfo.student}`);
    console.log(`   图片位置: 第 ${newInfo.current} / ${newInfo.total} 张`);
    
    if (newInfo.student === targetStudent) {
      console.log('   ✅ 切换成功！\n');
    } else {
      console.log(`   ❌ 切换失败！预期: ${targetStudent}, 实际: ${newInfo.student}\n`);
    }
  } else {
    console.log('   ❌ 无法获取切换后的学生信息\n');
  }

  console.log('========================================');
  console.log('  测试完成');
  console.log('========================================');

  await browser.close();
}

testSwitchStudent().catch(console.error);
