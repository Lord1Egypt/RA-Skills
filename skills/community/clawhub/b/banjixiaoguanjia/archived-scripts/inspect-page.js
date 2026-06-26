const { chromium } = require('playwright');

async function inspectPage() {
  console.log('连接到 Chrome 并检查页面结构...\n');
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('未找到班级小管家页面');
    await browser.close();
    return;
  }
  
  console.log('当前页面 URL:', page.url());
  console.log('页面标题:', await page.title());
  
  // 启用辅助功能
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 检查页面结构
  const structure = await page.evaluate(() => {
    const result = {
      fltScene: !!document.querySelector('flt-scene'),
      fltSemanticsCount: document.querySelectorAll('flt-semantics').length,
      scrollContainers: [],
      courses: []
    };
    
    // 查找所有可能滚动的元素
    const allElements = document.querySelectorAll('*');
    for (const el of allElements) {
      const style = el.getAttribute('style') || '';
      const tagName = el.tagName.toLowerCase();
      
      if (style.includes('overflow') || style.includes('scroll')) {
        result.scrollContainers.push({
          tag: tagName,
          style: style.substring(0, 100),
          scrollTop: el.scrollTop,
          scrollHeight: el.scrollHeight,
          clientHeight: el.clientHeight
        });
      }
    }
    
    // 查找课程
    const semantics = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of semantics) {
      const label = el.getAttribute('aria-label');
      if (label && (label.includes('第') || label.includes('年级'))) {
        result.courses.push(label.substring(0, 60));
      }
    }
    
    return result;
  });
  
  console.log('\n=== 页面结构 ===');
  console.log('flt-scene 存在:', structure.fltScene);
  console.log('flt-semantics 数量:', structure.fltSemanticsCount);
  
  console.log('\n=== 滚动容器 ===');
  structure.scrollContainers.forEach((c, i) => {
    console.log(`[${i}] ${c.tag}`);
    console.log(`    style: ${c.style}`);
    console.log(`    scrollTop: ${c.scrollTop}, scrollHeight: ${c.scrollHeight}, clientHeight: ${c.clientHeight}`);
  });
  
  console.log('\n=== 当前可见课程 ===');
  structure.courses.forEach((c, i) => {
    console.log(`[${i}] ${c.replace(/\n/g, ' | ')}`);
  });
  
  await browser.close();
}

inspectPage().catch(console.error);
