const { chromium } = require('playwright');

async function testScroll() {
  console.log('测试滚动到顶部\n');
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 导航到主页并进入课程
  await page.goto('https://service.banjixiaoguanjia.com/appweb/');
  await page.waitForTimeout(3000);
  
  await page.evaluate(() => {
    const el = document.querySelector('flt-semantics-placeholder');
    if (el) el.click();
  });
  await page.waitForTimeout(2000);
  
  // 查找并进入课程
  for (let i = 0; i < 10; i++) {
    const found = await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.includes('二下(第31节)')) return true;
      }
      const all = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of all) {
        const label = el.getAttribute('aria-label');
        if (label && (label.includes('第') || label.includes('年级'))) last = el;
      }
      if (last) last.scrollIntoView({ block: 'start' });
      return false;
    });
    
    if (found) break;
    await page.waitForTimeout(1500);
  }
  
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.includes('二下(第31节)')) {
        el.dispatchEvent(new MouseEvent('click', { bubbles: true }));
        break;
      }
    }
  });
  
  await page.waitForTimeout(4000);
  
  // 滚动到底部
  console.log('1. 滚动到底部...');
  for (let i = 0; i < 5; i++) {
    await page.evaluate(() => {
      const elements = document.querySelectorAll('flt-semantics[aria-label]');
      let last = null;
      for (const el of elements) {
        const label = el.getAttribute('aria-label');
        if (label && label.length > 20) {
          const lines = label.split(/\r?\n/);
          const name = lines[0].trim();
          if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
            last = el;
          }
        }
      }
      if (last) last.scrollIntoView({ block: 'start', behavior: 'instant' });
    });
    await page.waitForTimeout(1000);
  }
  
  // 检查当前可见学生
  let visible = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          list.push({ name, top: rect.top });
        }
      }
    }
    return list;
  });
  console.log('   当前可见:', visible.map(s => `${s.name}(top:${s.top.toFixed(0)})`).join(', '));
  
  // 尝试滚动到顶部
  console.log('\n2. 尝试滚动到顶部...');
  
  // 方法1: 使用 scrollTop
  await page.evaluate(() => {
    const container = document.querySelector('[style*="overflow-y: scroll"]');
    if (container) {
      console.log('找到滚动容器，设置 scrollTop = 0');
      container.scrollTop = 0;
    }
  });
  await page.waitForTimeout(1500);
  
  visible = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          list.push({ name, top: rect.top });
        }
      }
    }
    return list;
  });
  console.log('   方法1后可见:', visible.map(s => `${s.name}(top:${s.top.toFixed(0)})`).join(', '));
  
  // 方法2: 滚动到第一个学生
  console.log('\n3. 尝试滚动到第一个学生...');
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          console.log('找到第一个学生:', name);
          el.scrollIntoView({ block: 'start', behavior: 'instant' });
          break;
        }
      }
    }
  });
  await page.waitForTimeout(1500);
  
  visible = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          list.push({ name, top: rect.top });
        }
      }
    }
    return list;
  });
  console.log('   方法2后可见:', visible.map(s => `${s.name}(top:${s.top.toFixed(0)})`).join(', '));
  
  // 方法3: 查找灿灿并滚动
  console.log('\n4. 尝试直接滚动到灿灿...');
  await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.indexOf('灿灿') === 0) {
        console.log('找到灿灿，执行 scrollIntoView');
        el.scrollIntoView({ block: 'start', behavior: 'instant' });
        return true;
      }
    }
    return false;
  });
  await page.waitForTimeout(1500);
  
  visible = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          const rect = el.getBoundingClientRect();
          list.push({ name, top: rect.top });
        }
      }
    }
    return list;
  });
  console.log('   方法3后可见:', visible.map(s => `${s.name}(top:${s.top.toFixed(0)})`).join(', '));
  
  await browser.close();
}

testScroll().catch(console.error);
