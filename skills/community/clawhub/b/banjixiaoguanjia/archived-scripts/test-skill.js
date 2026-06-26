const { BanjixiaoguanjiaCapture } = require('./index');

async function testSkill() {
  console.log('========================================');
  console.log('  测试班级小管家作业截图 Skill');
  console.log('  课程：一下(第9节)');
  console.log('========================================\n');
  
  const capture = new BanjixiaoguanjiaCapture();
  
  try {
    const result = await capture.captureCourse('一下(第9节)');
    
    console.log('\n========================================');
    console.log('  批改结果');
    console.log('========================================');
    console.log(`课程: ${result.course}`);
    console.log(`已提交: ${result.submittedCount} 人`);
    console.log(`已截图: ${result.screenshotCount} 人`);
    console.log(`学生: ${result.students.map(s => s.name).join(', ')}`);
    console.log(`目录: ${result.outputDir}`);
    console.log('========================================');
    
  } catch (error) {
    console.error('错误:', error.message);
    console.error(error.stack);
  }
}

testSkill();
