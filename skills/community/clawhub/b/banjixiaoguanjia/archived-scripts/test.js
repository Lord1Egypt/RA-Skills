/**
 * 班级小管家截图工具测试
 */

const { BanjixiaoguanjiaCapture } = require('./index');

async function test() {
  console.log('=== 测试班级小管家截图工具 ===\n');
  
  const capture = new BanjixiaoguanjiaCapture({
    outputDir: './test-screenshots'
  });
  
  try {
    // 1. 连接 Chrome
    console.log('1. 测试连接 Chrome');
    await capture.connect();
    
    // 2. 启用辅助功能
    console.log('\n2. 测试启用辅助功能');
    await capture.enableAccessibility();
    
    // 3. 查找课程
    console.log('\n3. 测试查找课程');
    const courseInfo = await capture.findCourse('三上(第11节)');
    console.log('找到课程:', courseInfo.found);
    
    // 4. 进入课程
    console.log('\n4. 测试进入课程');
    const entered = await capture.enterCourse('三上(第11节)');
    if (!entered) {
      console.log('进入课程失败');
      return;
    }
    
    // 5. 获取学生列表
    console.log('\n5. 测试获取学生列表');
    const students = await capture.getStudents();
    
    // 6. 获取滚动信息
    console.log('\n6. 测试获取滚动信息');
    const scrollInfo = await capture.getScrollInfo();
    console.log('滚动信息:', scrollInfo);
    
    // 7. 截图
    console.log('\n7. 测试截图');
    await capture.screenshot('test-result.png');
    
    console.log('\n=== 所有测试通过 ===');
    
  } catch (err) {
    console.error('测试失败:', err);
  } finally {
    await capture.close();
  }
}

test();
