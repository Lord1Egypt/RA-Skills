/**
 * 调试脚本 - 重新查找"查看原图"按钮
 */

const { chromium } = require('playwright');

async function findViewOriginalButton() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const contexts = browser.contexts();
  const context = contexts[0];
  let page = context.pages()[0];
  
  // 先回到课程详情页
  console.log('=== 回到课程详情页 ===');
  await page.goto('https://service.banjixiaoguanjia.com/appweb/notice/task_detail_teacher_page', { waitUntil: 'networkidle' });
  await page.waitForTimeout(3000);
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  console.log('当前URL:', page.url());
  
  // 点击第一个作业图片进入批改页面
  console.log('\n=== 点击第一个作业图片 ===');
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    for (let i = 0; i < elements.length; i++) {
      const rect = elements[i].getBoundingClientRect();
      // 查找92x92的图片元素
      if (rect.width >= 90 && rect.width <= 95 && rect.height >= 90 && rect.height <= 95) {
        elements[i].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        console.log('点击了元素索引:', i);
        return;
      }
    }
  });
  
  await page.waitForTimeout(4000);
  console.log('进入批改页面后URL:', page.url());
  
  // 现在检查批改页面的所有元素
  console.log('\n=== 分析批改页面元素 ===');
  const allElements = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    const results = [];
    
    for (let i = 0; i < elements.length; i++) {
      const el = elements[i];
      const rect = el.getBoundingClientRect();
      const label = el.getAttribute('aria-label') || '';
      
      results.push({
        index: i,
        label: label.substring(0, 50),
        left: rect.left,
        top: rect.top,
        width: rect.width,
        height: rect.height
      });
    }
    
    return results;
  });
  
  // 显示右上角区域的所有元素 (x > 700, y < 100)
  console.log('\n右上角区域 (x>700, y<100) 的元素:');
  console.log('='.repeat(80));
  for (const el of allElements) {
    if (el.left > 700 && el.top < 100) {
      console.log(`[${el.index}] 位置:(${el.left.toFixed(0)},${el.top.toFixed(0)}) 尺寸:${el.width.toFixed(0)}x${el.height.toFixed(0)} 标签:"${el.label}"`);
    }
  }
  
  // 测试每个右上角元素，看哪个是"查看原图"
  console.log('\n=== 测试右上角元素 ===');
  const topRightIndices = allElements
    .filter(el => el.left > 700 && el.top < 100)
    .map(el => el.index);
  
  for (const idx of topRightIndices.slice(0, 3)) {
    console.log(`\n尝试点击元素 [${idx}]...`);
    
    await page.evaluate((index) => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[index]) {
        elements[index].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    }, idx);
    
    await page.waitForTimeout(2500);
    
    // 检查是否有新页面打开
    const pages = context.pages();
    console.log(`页面数量: ${pages.length}`);
    
    if (pages.length > 1) {
      const newPage = pages[pages.length - 1];
      console.log('✓ 新页面URL:', newPage.url().substring(0, 80));
      await newPage.close();
      await page.waitForTimeout(1000);
      console.log(`元素 [${idx}] 是"查看原图"按钮！`);
      break;
    } else {
      // 检查是否有对话框
      const hasDialog = await page.evaluate(() => {
        const elements = document.querySelectorAll('flt-semantics');
        for (const el of elements) {
          const label = el.getAttribute('aria-label') || '';
          if (label.includes('对话框')) return true;
        }
        return false;
      });
      
      if (hasDialog) {
        console.log('✗ 弹出了对话框，不是"查看原图"按钮');
        // 关闭对话框
        await page.keyboard.press('Escape');
        await page.waitForTimeout(500);
      } else {
        console.log('? 无变化');
      }
    }
  }
  
  await browser.close();
}

findViewOriginalButton().catch(console.error);
