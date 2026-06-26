/**
 * 调试脚本 - 继续查找"查看原图"按钮
 */

const { chromium } = require('playwright');

async function continueFinding() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const contexts = browser.contexts();
  const context = contexts[0];
  let page = context.pages()[0];
  
  // 确保在批改页面
  console.log('当前URL:', page.url());
  
  // 获取所有元素
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
  
  // 显示所有元素（按位置排序）
  console.log('\n所有元素（前30个）:');
  console.log('='.repeat(80));
  for (const el of allElements.slice(0, 30)) {
    console.log(`[${el.index}] 位置:(${el.left.toFixed(0)},${el.top.toFixed(0)}) 尺寸:${el.width.toFixed(0)}x${el.height.toFixed(0)} 标签:"${el.label}"`);
  }
  
  // 测试更多元素
  console.log('\n=== 测试更多元素 ===');
  const indicesToTest = [6, 7, 8, 9, 10, 11, 12, 15, 16, 17];
  
  for (const idx of indicesToTest) {
    if (idx >= allElements.length) continue;
    
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
    
    if (pages.length > 1) {
      const newPage = pages[pages.length - 1];
      const url = newPage.url();
      console.log('✓ 新页面URL:', url.substring(0, 80));
      
      if (url.includes('img.banjixiaoguanjia.com')) {
        console.log(`✓✓✓ 元素 [${idx}] 是"查看原图"按钮！`);
        await newPage.close();
        break;
      }
      await newPage.close();
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
        console.log('✗ 弹出了对话框');
        await page.keyboard.press('Escape');
        await page.waitForTimeout(500);
      } else {
        console.log('? 无变化');
      }
    }
  }
  
  await browser.close();
}

continueFinding().catch(console.error);
