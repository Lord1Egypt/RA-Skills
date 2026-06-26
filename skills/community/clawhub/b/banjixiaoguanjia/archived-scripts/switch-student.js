/**
 * 切换到下一个学生（KIKI）
 */

const { chromium } = require('playwright');

async function switchToNextStudent() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const contexts = browser.contexts();
  const context = contexts[0];
  const pages = context.pages();
  
  let page = pages.find(p => p.url().includes('correct_page'));
  
  if (!page) {
    console.log('未找到批改页面');
    await browser.close();
    return;
  }
  
  // 获取当前学生信息
  const currentInfo = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    if (elements[7]) {
      const text = elements[7].textContent || '';
      const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
      if (match) {
        return {
          student: match[1],
          current: parseInt(match[2]),
          total: parseInt(match[3])
        };
      }
    }
    return null;
  });
  
  console.log('当前学生:', currentInfo ? currentInfo.student : '未知');
  console.log('切换到: KIKI');
  
  // 在左侧学生列表中查找并点击 KIKI
  // 根据之前的分析，学生列表在元素[18]或附近的滚动区域
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    
    // 查找包含 "KIKI" 的元素
    for (let i = 0; i < elements.length; i++) {
      const text = elements[i].textContent || '';
      if (text.includes('KIKI') && text.length < 100) {
        console.log('找到KIKI，元素索引:', i);
        elements[i].dispatchEvent(new MouseEvent('click', { bubbles: true }));
        return true;
      }
    }
    return false;
  });
  
  await page.waitForTimeout(3000);
  
  // 验证切换后的学生
  const newInfo = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    if (elements[7]) {
      const text = elements[7].textContent || '';
      const match = text.match(/(.+?)的作业\((\d+)\/(\d+)\)/);
      if (match) {
        return {
          student: match[1],
          current: parseInt(match[2]),
          total: parseInt(match[3])
        };
      }
    }
    return null;
  });
  
  if (newInfo) {
    console.log('\n切换后:');
    console.log('学生:', newInfo.student);
    console.log('图片位置:', `第 ${newInfo.current} / ${newInfo.total} 张`);
    
    if (newInfo.student === 'KIKI') {
      console.log('✓ 成功切换到 KIKI');
    } else {
      console.log(`⚠️ 当前是 ${newInfo.student}，不是 KIKI`);
    }
  } else {
    console.log('无法获取切换后的学生信息');
  }
  
  await browser.close();
}

switchToNextStudent().catch(console.error);
