const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureSecondStudent() {
  console.log('截图第二个学生（Zoey）\n');
  
  const outputDir = 'C:\\Users\\Administrator\\Desktop\\二下(第31节)';
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  // 截图第二个学生（Zoey）
  const filepath = path.join(outputDir, 'Zoey.png');
  await page.screenshot({ path: filepath, fullPage: false, timeout: 60000 });
  console.log(`✓ 已保存: Zoey.png`);
  
  await browser.close();
  console.log('\n完成！');
}

captureSecondStudent().catch(console.error);
