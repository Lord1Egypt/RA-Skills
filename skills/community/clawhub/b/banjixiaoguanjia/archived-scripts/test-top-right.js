/**
 * 调试脚本 - 尝试点击右上角元素
 */

const { chromium } = require('playwright');

async function testTopRightButtons() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const contexts = browser.contexts();
  const context = contexts[0];
  const pages = context.pages();
  
  let page = pages.find(p => p.url().includes('correct_page'));
  
  if (!page) {
    console.log('未找到correct_page');
    await browser.close();
    return;
  }
  
  console.log('页面URL:', page.url());
  
  // 尝试点击右上角的元素 [8], [9], [44]
  const buttonsToTest = [8, 9, 44];
  
  for (const btnIndex of buttonsToTest) {
    console.log(`\n尝试点击元素 [${btnIndex}]...`);
    
    // 点击元素
    await page.evaluate((index) => {
      const elements = document.querySelectorAll('flt-semantics');
      if (elements[index]) {
        elements[index].dispatchEvent(new MouseEvent('click', { bubbles: true }));
      }
    }, btnIndex);
    
    await page.waitForTimeout(3000);
    
    // 检查是否有新页面打开
    const allPages = context.pages();
    console.log(`页面数量: ${allPages.length}`);
    
    if (allPages.length > 1) {
      const newPage = allPages[allPages.length - 1];
      console.log('新页面URL:', newPage.url());
      
      // 关闭新页面
      await newPage.close();
      await page.waitForTimeout(1000);
    }
    
    // 检查当前页面是否有变化
    console.log('当前页面URL:', page.url());
  }
  
  await browser.close();
}

testTopRightButtons().catch(console.error);
