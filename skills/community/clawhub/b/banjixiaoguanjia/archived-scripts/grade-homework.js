const { BanjixiaoguanjiaCapture } = require('./index');

async function main() {
  console.log('========================================');
  console.log('  班级小管家作业批改 - 二下第31节');
  console.log('========================================\n');
  
  const capture = new BanjixiaoguanjiaCapture({
    outputDir: 'C:\\Users\\Administrator\\Desktop\\二下第31节作业'
  });
  
  try {
    // 1. 截图所有学生作业
    const result = await capture.captureCourse('二下(第31节)');
    
    if (!result) {
      console.log('\n✗ 截图失败，请检查 Chrome 是否已启动并登录班级小管家');
      process.exit(1);
    }
    
    console.log('\n========================================');
    console.log('  截图完成！');
    console.log('========================================');
    console.log(`课程: ${result.course}`);
    console.log(`学生数量: ${result.studentCount}`);
    console.log(`输出目录: ${result.outputDir}`);
    console.log('\n学生列表:');
    result.students.forEach((s, i) => {
      console.log(`  ${i + 1}. ${s.name} - ${s.status || '待查看'}`);
    });
    
    console.log('\n========================================');
    console.log('  准备进行 AI 作业批改...');
    console.log('========================================\n');
    
    // 2. 使用 GLM-4V 分析作业
    // 从环境变量或配置文件读取 API Key
    const apiKey = process.env.GLM_API_KEY;
    
    if (!apiKey) {
      console.log('⚠️ 未设置 GLM_API_KEY 环境变量，跳过 AI 分析');
      console.log('如需 AI 批改，请设置: set GLM_API_KEY=your_api_key');
      console.log('\n截图文件已保存到:', result.outputDir);
      return;
    }
    
    const analysisResults = await capture.analyzeAllScreenshots(
      result.screenshots,
      apiKey
    );
    
    // 3. 生成批改报告
    console.log('\n========================================');
    console.log('  批改报告');
    console.log('========================================\n');
    
    for (const item of analysisResults) {
      console.log(`【${item.student}】`);
      console.log(item.analysis);
      console.log('----------------------------------------\n');
    }
    
    console.log('\n✓ 批改完成！');
    console.log('截图保存位置:', result.outputDir);
    
  } catch (error) {
    console.error('\n✗ 错误:', error.message);
    console.error(error.stack);
    process.exit(1);
  }
}

main();
