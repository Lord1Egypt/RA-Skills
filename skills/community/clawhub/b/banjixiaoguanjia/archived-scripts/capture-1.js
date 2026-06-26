const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureFirstStudent() {
  console.log('截图第一个学生（灿灿）\n');
  
  const outputDir = 'C:\\Users\\Administrator\\Desktop\\二下(第31节)';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 截图第一个学生（灿灿）
  const filepath = path.join(outputDir, '灿灿.png');
  await page.screenshot({ path: filepath, fullPage: false, timeout: 60000 });
  console.log(`✓ 已保存: 灿灿.png`);
  
  await browser.close();
  console.log('\n完成！');
}

captureFirstStudent().catch(console.error);
