#!/usr/bin/env node
/**
 * 完整示例：截图 + GLM 分析
 * 展示如何使用 banjixiaoguanjia skill 完成整个流程
 */

const { BanjixiaoguanjiaCapture } = require('./index');

async function main() {
  console.log('=== 班级小管家作业截图 + GLM 分析示例 ===\n');
  
  // GLM API Key
  const GLM_API_KEY = '0dd66809197f48a99f160838f9f9fddf.v2tN6n5lz5nR179u';
  
  // 课程名称
  const courseName = '三上(第11节)';
  
  // 创建截图工具实例
  const capture = new BanjixiaoguanjiaCapture({
    outputDir: `./screenshots/${courseName}`
  });
  
  try {
    // 步骤1: 截图
    console.log('步骤1: 截图学生作业...\n');
    const captureResult = await capture.captureCourse(courseName);
    
    if (!captureResult) {
      console.log('截图失败');
      return;
    }
    
    console.log(`✓ 截图完成，共 ${captureResult.studentCount} 个学生\n`);
    
    // 步骤2: 使用 GLM 分析
    console.log('步骤2: 使用 GLM-4V 分析截图...\n');
    const analysisResults = await capture.analyzeAllScreenshots(
      captureResult.screenshots,
      GLM_API_KEY
    );
    
    // 步骤3: 输出结果
    console.log('=== 分析结果汇总 ===\n');
    
    for (const result of analysisResults) {
      console.log(`【${result.student}】`);
      console.log('-'.repeat(40));
      console.log(result.analysis);
      console.log();
    }
    
    console.log('=== 完成 ===');
    
  } catch (error) {
    console.error('错误:', error.message);
  }
}

main();
