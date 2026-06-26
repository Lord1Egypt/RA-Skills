const { chromium } = require('playwright');

async function checkCourse() {
  console.log('连接 Chrome...');
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0];
  const pages = context.pages();
  
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('❌ 未找到班级小管家页面');
    await browser.close();
    return;
  }
  
  console.log('当前页面URL:', page.url());
  console.log('\n点击"未提交"标签...\n');
  
  // 点击未提交标签
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics');
    for (const el of elements) {
      const text = el.getAttribute('aria-label') || el.textContent || '';
      if (text.includes('未提交')) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  });
  
  await sleep(2000);
  
  // 获取所有语义元素
  const elements = await page.evaluate(() => {
    const allElements = document.querySelectorAll('flt-semantics');
    const results = [];
    
    for (let i = 0; i < allElements.length; i++) {
      const el = allElements[i];
      const label = el.getAttribute('aria-label') || '';
      const text = el.textContent || '';
      if (label || text) {
        results.push({
          index: i,
          label: label.substring(0, 300),
          text: text.substring(0, 300)
        });
      }
    }
    
    return results;
  });
  
  console.log('所有元素:');
  for (const el of elements) {
    console.log(`[${el.index}] Label: ${el.label || '(empty)'}`);
    console.log(`     Text: ${el.text || '(empty)'}`);
    console.log('---');
  }
  
  await browser.close();
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

checkCourse().catch(console.error);
