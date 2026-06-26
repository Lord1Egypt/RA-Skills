/**
 * 基础录制示例
 * 演示如何使用 ScreenRecorder 进行基本录制
 */

const { ScreenRecorder } = require('../scripts/record-browser');
const { checkDependencies, checkFFmpeg, Logger } = require('../scripts/utils');
const chalk = require('chalk');

async function runBasicExample() {
  console.log(chalk.cyan('='.repeat(60)));
  console.log(chalk.cyan('🎬 基础录制示例'));
  console.log(chalk.cyan('='.repeat(60)));
  
  // 检查依赖
  const depsOk = await checkDependencies();
  if (!depsOk) {
    console.log(chalk.red('❌ 依赖检查失败，请先安装依赖'));
    return;
  }
  
  const ffmpegOk = await checkFFmpeg();
  if (!ffmpegOk) {
    console.log(chalk.yellow('⚠️  FFmpeg 未安装，某些功能可能受限'));
  }
  
  // 创建日志记录器
  const logger = new Logger();
  logger.info('开始基础录制示例');
  
  try {
    // 创建录制器实例
    const recorder = new ScreenRecorder({
      outputPath: './recordings/basic-example.mp4',
      fps: 24,
      quality: 85,
      headless: false,
      viewport: { width: 1280, height: 720 },
      debug: true
    });
    
    logger.info('录制器创建成功', { outputPath: './recordings/basic-example.mp4' });
    
    // 开始录制（访问示例页面）
    const testUrl = 'https://example.com';
    console.log(chalk.blue(`\n🌐 开始录制: ${testUrl}`));
    
    await recorder.startRecording(testUrl);
    
    logger.success('录制开始', { url: testUrl });
    
    // 执行一些操作
    console.log(chalk.yellow('\n🔄 执行测试操作...'));
    
    // 等待页面加载
    await recorder.page.waitForTimeout(2000);
    
    // 添加标注
    await recorder.addAnnotation('测试标注 - 页面已加载', { x: 50, y: 50 });
    logger.info('添加标注', { text: '测试标注 - 页面已加载' });
    
    // 模拟滚动
    await recorder.page.evaluate(() => {
      window.scrollTo(0, 500);
    });
    await recorder.page.waitForTimeout(1000);
    
    // 模拟点击（如果页面有可点击元素）
    try {
      await recorder.page.click('a');
      logger.info('模拟点击操作');
    } catch (error) {
      // 忽略点击错误，示例页面可能没有链接
    }
    
    // 等待更多时间以便录制
    console.log(chalk.yellow('⏳ 录制中，5秒后停止...'));
    await recorder.page.waitForTimeout(5000);
    
    // 停止录制
    console.log(chalk.yellow('\n⏹️  停止录制...'));
    const result = await recorder.stopRecording();
    
    logger.success('录制完成', result);
    
    // 显示结果
    console.log(chalk.green('\n✅ 录制完成！'));
    console.log(chalk.cyan('📊 录制统计:'));
    console.log(chalk.cyan(`   时长: ${result.duration.toFixed(2)} 秒`));
    console.log(chalk.cyan(`   文件大小: ${(result.fileSize / (1024 * 1024)).toFixed(2)} MB`));
    console.log(chalk.cyan(`   输出文件: ${result.filePath}`));
    console.log(chalk.cyan(`   帧数: ${result.frameCount}`));
    
    logger.info('示例完成', { success: true });
    
  } catch (error) {
    console.error(chalk.red('\n❌ 录制失败:'), error.message);
    logger.error('录制失败', { error: error.message, stack: error.stack });
  }
  
  console.log(chalk.cyan('\n='.repeat(60)));
  console.log(chalk.cyan('🎬 示例结束'));
  console.log(chalk.cyan('='.repeat(60)));
}

async function runMultiSiteExample() {
  console.log(chalk.cyan('\n🌐 多站点录制示例'));
  
  const sites = [
    { name: 'GitHub', url: 'https://github.com' },
    { name: 'MDN Web Docs', url: 'https://developer.mozilla.org' },
    { name: 'Stack Overflow', url: 'https://stackoverflow.com' }
  ];
  
  const recorder = new ScreenRecorder({
    outputPath: './recordings/multi-site-example.mp4',
    fps: 20,
    quality: 75,
    headless: true
  });
  
  try {
    for (let i = 0; i < sites.length; i++) {
      const site = sites[i];
      const siteNumber = i + 1;
      
      console.log(chalk.blue(`\n📍 站点 ${siteNumber}/${sites.length}: ${site.name}`));
      
      if (i === 0) {
        // 第一个站点开始录制
        await recorder.startRecording(site.url);
      } else {
        // 后续站点导航
        await recorder.page.goto(site.url, { waitUntil: 'networkidle0' });
      }
      
      // 添加站点标注
      await recorder.addAnnotation(`站点 ${siteNumber}: ${site.name}`, { x: 50, y: 50 });
      
      // 在站点上停留一段时间
      await recorder.page.waitForTimeout(3000);
      
      // 模拟一些交互
      if (site.name === 'GitHub') {
        // 在GitHub搜索
        await recorder.page.type('.header-search-input', 'puppeteer');
        await recorder.page.waitForTimeout(1000);
      }
      
      console.log(chalk.green(`✅ ${site.name} 录制完成`));
    }
    
    // 停止录制
    const result = await recorder.stopRecording();
    
    console.log(chalk.green('\n🎉 多站点录制完成'));
    console.log(chalk.cyan(`   总时长: ${result.duration.toFixed(2)} 秒`));
    console.log(chalk.cyan(`   文件: ${result.filePath}`));
    
  } catch (error) {
    console.error(chalk.red('❌ 多站点录制失败:'), error);
    await recorder.cleanup();
  }
}

async function runInteractiveExample() {
  console.log(chalk.cyan('\n🎮 交互式录制示例'));
  
  const inquirer = require('inquirer');
  
  const answers = await inquirer.prompt([
    {
      type: 'input',
      name: 'url',
      message: '请输入要录制的URL:',
      default: 'https://example.com'
    },
    {
      type: 'number',
      name: 'duration',
      message: '录制时长(秒):',
      default: 10,
      validate: (value) => value > 0 && value <= 300
    },
    {
      type: 'list',
      name: 'quality',
      message: '选择视频质量:',
      choices: [
        { name: '高 (文件较大)', value: 90 },
        { name: '中 (推荐)', value: 80 },
        { name: '低 (文件较小)', value: 70 }
      ],
      default: 80
    },
    {
      type: 'confirm',
      name: 'headless',
      message: '使用无头模式?',
      default: false
    }
  ]);
  
  const recorder = new ScreenRecorder({
    outputPath: './recordings/interactive-example.mp4',
    fps: 30,
    quality: answers.quality,
    headless: answers.headless
  });
  
  console.log(chalk.blue(`\n🚀 开始录制: ${answers.url}`));
  console.log(chalk.blue(`⏱️  时长: ${answers.duration} 秒`));
  console.log(chalk.blue(`🎨 质量: ${answers.quality}`));
  console.log(chalk.blue(`👻 无头模式: ${answers.headless ? '是' : '否'}`));
  
  try {
    await recorder.startRecording(answers.url);
    
    // 添加开始标注
    await recorder.addAnnotation(`开始录制: ${answers.url}`, { x: 50, y: 50 });
    
    // 显示倒计时
    console.log(chalk.yellow('\n⏳ 录制中...'));
    for (let i = answers.duration; i > 0; i--) {
      process.stdout.write(`\r剩余: ${i} 秒`);
      await recorder.page.waitForTimeout(1000);
      
      // 更新标注
      if (i % 5 === 0) {
        await recorder.addAnnotation(`剩余: ${i} 秒`, { x: 50, y: 100 });
      }
    }
    process.stdout.write('\n');
    
    // 添加结束标注
    await recorder.addAnnotation('录制完成!', { x: 50, y: 50 });
    await recorder.page.waitForTimeout(1000);
    
    const result = await recorder.stopRecording();
    
    console.log(chalk.green('\n✅ 交互式录制完成'));
    console.log(chalk.cyan(`   文件: ${result.filePath}`));
    console.log(chalk.cyan(`   实际时长: ${result.duration.toFixed(2)} 秒`));
    
  } catch (error) {
    console.error(chalk.red('❌ 交互式录制失败:'), error);
    await recorder.cleanup();
  }
}

// 主函数
async function main() {
  console.log(chalk.cyan('🎬 E2E测试录制示例程序'));
  console.log(chalk.cyan('请选择要运行的示例:'));
  console.log(chalk.cyan('1. 基础录制示例'));
  console.log(chalk.cyan('2. 多站点录制示例'));
  console.log(chalk.cyan('3. 交互式录制示例'));
  console.log(chalk.cyan('4. 运行所有示例'));
  console.log(chalk.cyan('0. 退出'));
  
  const inquirer = require('inquirer');
  
  const answer = await inquirer.prompt([
    {
      type: 'list',
      name: 'choice',
      message: '请选择:',
      choices: [
        { name: '基础录制示例', value: '1' },
        { name: '多站点录制示例', value: '2' },
        { name: '交互式录制示例', value: '3' },
        { name: '运行所有示例', value: '4' },
        { name: '退出', value: '0' }
      ]
    }
  ]);
  
  switch (answer.choice) {
    case '1':
      await runBasicExample();
      break;
    case '2':
      await runMultiSiteExample();
      break;
    case '3':
      await runInteractiveExample();
      break;
    case '4':
      await runBasicExample();
      await runMultiSiteExample();
      await runInteractiveExample();
      break;
    case '0':
      console.log(chalk.yellow('👋 再见！'));
      process.exit(0);
  }
  
  // 询问是否继续
  const continueAnswer = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'continue',
      message: '是否运行其他示例?',
      default: false
    }
  ]);
  
  if (continueAnswer.continue) {
    await main();
  } else {
    console.log(chalk.green('🎉 所有示例运行完成！'));
    console.log(chalk.cyan('📁 录制文件保存在 recordings/ 目录中'));
  }
}

// 如果直接运行此文件
if (require.main === module) {
  main().catch(error => {
    console.error(chalk.red('❌ 示例程序运行失败:'), error);
    process.exit(1);
  });
}

module.exports = {
  runBasicExample,
  runMultiSiteExample,
  runInteractiveExample,
  main
};