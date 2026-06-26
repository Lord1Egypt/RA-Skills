const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureCorrectly() {
  const courseName = '二下(第36节)';
  const outputDir = 'C:\\Users\\Administrator\\Desktop\\二下(第36节)';
  
  console.log('========================================');
  console.log(`  作业截图 - ${courseName}`);
  console.log('========================================\n');
  
  // 清理目录
  if (fs.existsSync(outputDir)) {
    fs.rmSync(outputDir, { recursive: true });
  }
  fs.mkdirSync(outputDir, { recursive: true });
  
  const browser = await chromium.connectOverCDP('http://localhost:9222');
  const context = browser.contexts()[0] || await browser.newContext();
  const pages = context.pages();
  let page = pages.find(p => p.url().includes('banjixiaoguanjia'));
  
  console.log('当前页面URL:', page.url());
  console.log('\n开始截图...\n');
  
  // 先截图球球（第一个学生，不需要滚动）
  console.log('[1] 截图: 球球');
  await page.screenshot({ path: path.join(outputDir, '球球.png') });
  console.log('   ✓ 已保存: 球球.png');
  
  // 滚动到Zoey
  console.log('\n滚动到下一个学生...');
  await page.evaluate(() => {
    const container = document.querySelector('[style*="overflow-y: scroll"]');
    if (container) {
      container.scrollTop = 400;
    }
  });
  await page.waitForTimeout(1500);
  
  // 截图Zoey
  console.log('[2] 截图: Zoey');
  await page.screenshot({ path: path.join(outputDir, 'Zoey.png') });
  console.log('   ✓ 已保存: Zoey.png');
  
  console.log('\n========================================');
  console.log('✓ 截图完成！');
  console.log(`输出目录: ${outputDir}`);
  console.log('========================================');
  
  await browser.close();
}

captureCorrectly().catch(console.error);
