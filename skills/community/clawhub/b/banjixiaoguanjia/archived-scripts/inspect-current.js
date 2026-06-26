const { chromium } = require('playwright');

async function inspectPage() {
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  if (!page) {
    console.log('未找到班级小管家页面');
    return;
  }
  
  console.log('当前页面URL:', page.url());
  console.log('\n检查页面元素...\n');
  
  // 获取所有语义元素
  const elements = await page.evaluate(() => {
    const list = [];
    const all = document.querySelectorAll('flt-semantics[aria-label]');
    for (let i = 0; i < Math.min(all.length, 50); i++) {
      const el = all[i];
      const label = el.getAttribute('aria-label');
      if (label) {
        list.push({ index: i, label: label.substring(0, 100) });
      }
    }
    return list;
  });
  
  console.log('页面元素 (前50个):');
  elements.forEach(e => {
    console.log(`[${e.index}] ${e.label}`);
  });
  
  // 查找已提交数量
  console.log('\n查找已提交数量...');
  const submittedInfo = await page.evaluate(() => {
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && (label.includes('已提交') || label.includes('提交'))) {
        return label;
      }
    }
    return null;
  });
  
  if (submittedInfo) {
    console.log('找到:', submittedInfo);
  } else {
    console.log('未找到已提交信息');
  }
  
  // 查找学生信息
  console.log('\n查找学生信息...');
  const students = await page.evaluate(() => {
    const list = [];
    const elements = document.querySelectorAll('flt-semantics[aria-label]');
    for (const el of elements) {
      const label = el.getAttribute('aria-label');
      if (label && label.length > 20) {
        const lines = label.split(/\r?\n/);
        const name = lines[0].trim();
        if (name && name.length < 15 && !name.includes('详情') && !name.includes('查看')) {
          list.push({ name, preview: label.substring(0, 80) });
        }
      }
    }
    return list;
  });
  
  console.log(`找到 ${students.length} 个学生:`);
  students.forEach((s, i) => {
    console.log(`  ${i + 1}. ${s.name} - ${s.preview}`);
  });
  
  await browser.close();
}

inspectPage().catch(console.error);
