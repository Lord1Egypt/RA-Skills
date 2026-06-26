const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

async function captureTwoStudents() {
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
  
  // 学生列表（已确认只有2个）
  const studentList = [
    { name: '球球', scrollTop: 0 },
    { name: 'Zoey', scrollTop: 400 }
  ];
  
  console.log('学生列表:');
  studentList.forEach((s, i) => console.log(`  ${i + 1}. ${s.name}`));
  console.log();
  
  // 截图每个学生
  console.log('【截图】\n');
  
  const screenshots = [];
  
  for (let i = 0; i < studentList.length; i++) {
    const student = studentList[i];
    
    console.log(`[${i + 1}] ${student.name}`);
    
    // 设置滚动位置
    if (i > 0) {
      await page.evaluate((scrollTop) => {
        const container = document.querySelector('[style*="overflow-y: scroll"]');
        if (container) {
          container.scrollTop = scrollTop;
        }
      }, student.scrollTop);
      await page.waitForTimeout(1000);
    }
    
    // 截图
    const filepath = path.join(outputDir, `${student.name}.png`);
    await page.screenshot({ path: filepath, fullPage: false });
    console.log(`   ✓ 已保存: ${student.name}.png`);
    
    screenshots.push({ name: student.name, filepath });
  }
  
  console.log('\n========================================');
  console.log(`✓ 截图完成，共 ${screenshots.length} 个学生`);
  console.log(`输出目录: ${outputDir}\n`);
  
  await browser.close();
  
  return {
    course: courseName,
    screenshotCount: screenshots.length,
    students: screenshots.map(s => s.name),
    outputDir
  };
}

captureTwoStudents()
  .then(result => {
    console.log('========================================');
    console.log('  截图完成');
    console.log('========================================');
    console.log(`课程: ${result.course}`);
    console.log(`已截图: ${result.screenshotCount} 人`);
    console.log(`学生: ${result.students.join(', ')}`);
    console.log(`目录: ${result.outputDir}`);
    console.log('========================================');
  })
  .catch(console.error);
