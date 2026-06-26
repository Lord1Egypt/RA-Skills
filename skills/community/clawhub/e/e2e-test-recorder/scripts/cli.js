#!/usr/bin/env node

/**
 * E2E测试录制CLI工具
 * 命令行接口，支持多种录制模式
 */

const { program } = require('commander');
const chalk = require('chalk');
const { ScreenRecorder, quickRecord } = require('./record-browser');
const { recordE2ETest, recordAPITest, recordTestSuite } = require('./record-test');
const { checkDependencies, checkFFmpeg, Logger, generateUniqueFilename } = require('./utils');
const path = require('path');
const fs = require('fs-extra');

// 版本信息
const packageJson = require('../package.json');
program.version(packageJson.version, '-v, --version', '显示版本信息');

// 全局选项
program
  .option('-d, --debug', '启用调试模式')
  .option('-l, --log-level <level>', '日志级别', 'info')
  .option('-o, --output <path>', '输出文件路径')
  .option('--no-deps-check', '跳过依赖检查');

// 基础录制命令
program
  .command('record <url>')
  .description('录制指定URL的页面')
  .option('-f, --fps <fps>', '帧率', '30')
  .option('-q, --quality <quality>', '视频质量 (0-100)', '80')
  .option('-t, --timeout <seconds>', '录制时长(秒)', '30')
  .option('--headless', '使用无头模式')
  .option('--viewport <width>x<height>', '视口尺寸', '1920x1080')
  .action(async (url, options) => {
    try {
      await runRecordCommand(url, options);
    } catch (error) {
      console.error(chalk.red('❌ 录制失败:'), error.message);
      process.exit(1);
    }
  });

// 端到端测试录制命令
program
  .command('test <config>')
  .description('录制端到端测试')
  .option('-n, --name <name>', '测试名称')
  .option('-u, --url <url>', '测试URL（覆盖配置中的URL）')
  .option('-o, --output <path>', '输出文件路径')
  .action(async (configPath, options) => {
    try {
      await runTestCommand(configPath, options);
    } catch (error) {
      console.error(chalk.red('❌ 测试录制失败:'), error.message);
      process.exit(1);
    }
  });

// API测试录制命令
program
  .command('api <config>')
  .description('录制API测试')
  .option('-o, --output <path>', '输出文件路径')
  .option('--format <format>', '输出格式 (mp4/gif)', 'gif')
  .action(async (configPath, options) => {
    try {
      await runAPICommand(configPath, options);
    } catch (error) {
      console.error(chalk.red('❌ API测试录制失败:'), error.message);
      process.exit(1);
    }
  });

// 批量测试套件命令
program
  .command('suite <config>')
  .description('录制测试套件')
  .option('-o, --output-dir <dir>', '输出目录', './recordings')
  .option('--parallel', '并行执行测试')
  .option('--max-parallel <number>', '最大并行数', '3')
  .action(async (configPath, options) => {
    try {
      await runSuiteCommand(configPath, options);
    } catch (error) {
      console.error(chalk.red('❌ 测试套件录制失败:'), error.message);
      process.exit(1);
    }
  });

// 转换格式命令
program
  .command('convert <input>')
  .description('转换视频格式')
  .option('-o, --output <path>', '输出文件路径')
  .option('-f, --format <format>', '目标格式 (mp4/gif/webm)', 'mp4')
  .option('-q, --quality <quality>', '质量 (0-100)', '80')
  .option('--width <width>', '宽度')
  .option('--height <height>', '高度')
  .action(async (inputPath, options) => {
    try {
      await runConvertCommand(inputPath, options);
    } catch (error) {
      console.error(chalk.red('❌ 格式转换失败:'), error.message);
      process.exit(1);
    }
  });

// 检查命令
program
  .command('check')
  .description('检查系统环境和依赖')
  .action(async () => {
    await runCheckCommand();
  });

// 示例命令
program
  .command('demo')
  .description('运行演示示例')
  .option('-t, --type <type>', '示例类型 (basic/interactive/multi)', 'basic')
  .action(async (options) => {
    try {
      await runDemoCommand(options);
    } catch (error) {
      console.error(chalk.red('❌ 演示运行失败:'), error.message);
      process.exit(1);
    }
  });

// 帮助命令
program
  .command('help')
  .description('显示帮助信息')
  .action(() => {
    program.help();
  });

// 主函数：运行录制命令
async function runRecordCommand(url, options) {
  console.log(chalk.cyan('='.repeat(60)));
  console.log(chalk.cyan('🎬 E2E测试录制工具'));
  console.log(chalk.cyan('='.repeat(60)));
  
  // 检查依赖
  if (!program.opts().noDepsCheck) {
    const depsOk = await checkDependencies();
    if (!depsOk) {
      console.log(chalk.red('❌ 依赖检查失败，请先安装依赖'));
      process.exit(1);
    }
  }
  
  // 解析视口尺寸
  const [width, height] = options.viewport.split('x').map(Number);
  
  // 生成输出路径
  const outputPath = options.output || generateOutputPath('recording', 'mp4');
  
  // 创建日志记录器
  const logger = new Logger('./logs', program.opts().logLevel);
  
  console.log(chalk.blue('\n📋 录制配置:'));
  console.log(chalk.blue(`   URL: ${url}`));
  console.log(chalk.blue(`   输出: ${outputPath}`));
  console.log(chalk.blue(`   帧率: ${options.fps} FPS`));
  console.log(chalk.blue(`   质量: ${options.quality}`));
  console.log(chalk.blue(`   时长: ${options.timeout} 秒`));
  console.log(chalk.blue(`   视口: ${width}x${height}`));
  console.log(chalk.blue(`   无头模式: ${options.headless ? '是' : '否'}`));
  
  logger.info('开始录制', {
    url,
    outputPath,
    fps: options.fps,
    quality: options.quality,
    timeout: options.timeout,
    viewport: { width, height },
    headless: options.headless
  });
  
  try {
    // 使用快速录制函数
    const result = await quickRecord(url, {
      outputPath,
      fps: parseInt(options.fps),
      quality: parseInt(options.quality),
      timeout: parseInt(options.timeout) * 1000,
      headless: options.headless,
      viewport: { width, height },
      debug: program.opts().debug
    });
    
    logger.success('录制完成', result);
    
    console.log(chalk.green('\n✅ 录制完成！'));
    console.log(chalk.cyan('📊 录制结果:'));
    console.log(chalk.cyan(`   文件: ${result.filePath}`));
    console.log(chalk.cyan(`   时长: ${result.duration.toFixed(2)} 秒`));
    console.log(chalk.cyan(`   大小: ${(result.fileSize / (1024 * 1024)).toFixed(2)} MB`));
    
  } catch (error) {
    logger.error('录制失败', { error: error.message, stack: error.stack });
    throw error;
  }
}

// 运行测试命令
async function runTestCommand(configPath, options) {
  console.log(chalk.cyan('🧪 端到端测试录制'));
  
  // 加载配置文件
  const config = await loadConfigFile(configPath);
  if (!config) {
    console.log(chalk.red(`❌ 无法加载配置文件: ${configPath}`));
    process.exit(1);
  }
  
  // 覆盖配置
  if (options.url) config.url = options.url;
  if (options.name) config.testName = options.name;
  if (options.output) config.output = options.output;
  
  // 确保输出目录存在
  const outputDir = path.dirname(config.output || './recordings/test.mp4');
  fs.ensureDirSync(outputDir);
  
  console.log(chalk.blue('\n📋 测试配置:'));
  console.log(chalk.blue(`   名称: ${config.testName}`));
  console.log(chalk.blue(`   URL: ${config.url}`));
  console.log(chalk.blue(`   步骤数: ${config.testSteps?.length || 0}`));
  console.log(chalk.blue(`   输出: ${config.output || '未指定'}`));
  
  try {
    const result = await recordE2ETest(config);
    
    console.log(chalk.green('\n✅ 测试录制完成！'));
    console.log(chalk.cyan(`   文件: ${result.filePath}`));
    console.log(chalk.cyan(`   报告: ${result.reportPath}`));
    
  } catch (error) {
    console.error(chalk.red('❌ 测试录制失败:'), error.message);
    throw error;
  }
}

// 运行API命令
async function runAPICommand(configPath, options) {
  console.log(chalk.cyan('🔌 API测试录制'));
  
  const config = await loadConfigFile(configPath);
  if (!config) {
    console.log(chalk.red(`❌ 无法加载配置文件: ${configPath}`));
    process.exit(1);
  }
  
  // 设置输出路径
  if (options.output) {
    config.output = options.output;
  } else if (!config.output) {
    config.output = generateOutputPath('api-test', options.format || 'gif');
  }
  
  console.log(chalk.blue('\n📋 API测试配置:'));
  console.log(chalk.blue(`   API地址: ${config.apiUrl}`));
  console.log(chalk.blue(`   测试数量: ${config.tests?.length || 0}`));
  console.log(chalk.blue(`   输出格式: ${options.format || 'gif'}`));
  console.log(chalk.blue(`   输出文件: ${config.output}`));
  
  try {
    const result = await recordAPITest(config);
    
    console.log(chalk.green('\n✅ API测试录制完成！'));
    console.log(chalk.cyan(`   文件: ${result.filePath}`));
    
  } catch (error) {
    console.error(chalk.red('❌ API测试录制失败:'), error.message);
    throw error;
  }
}

// 运行套件命令
async function runSuiteCommand(configPath, options) {
  console.log(chalk.cyan('📦 测试套件录制'));
  
  const config = await loadConfigFile(configPath);
  if (!config) {
    console.log(chalk.red(`❌ 无法加载配置文件: ${configPath}`));
    process.exit(1);
  }
  
  // 设置输出目录
  config.outputDir = options.outputDir;
  fs.ensureDirSync(config.outputDir);
  
  console.log(chalk.blue('\n📋 测试套件配置:'));
  console.log(chalk.blue(`   套件名称: ${config.name}`));
  console.log(chalk.blue(`   测试数量: ${config.tests?.length || 0}`));
  console.log(chalk.blue(`   输出目录: ${config.outputDir}`));
  console.log(chalk.blue(`   并行执行: ${options.parallel ? '是' : '否'}`));
  
  try {
    const result = await recordTestSuite(config);
    
    console.log(chalk.green('\n✅ 测试套件录制完成！'));
    console.log(chalk.cyan(`   成功: ${result.successfulTests}/${result.totalTests}`));
    console.log(chalk.cyan(`   报告: ${path.join(config.outputDir, `${config.name}-report.json`)}`));
    
  } catch (error) {
    console.error(chalk.red('❌ 测试套件录制失败:'), error.message);
    throw error;
  }
}

// 运行转换命令
async function runConvertCommand(inputPath, options) {
  console.log(chalk.cyan('🔄 视频格式转换'));
  
  if (!fs.existsSync(inputPath)) {
    console.log(chalk.red(`❌ 输入文件不存在: ${inputPath}`));
    process.exit(1);
  }
  
  // 生成输出路径
  const outputPath = options.output || generateOutputPath(
    path.basename(inputPath, path.extname(inputPath)),
    options.format || 'mp4'
  );
  
  console.log(chalk.blue('\n📋 转换配置:'));
  console.log(chalk.blue(`   输入: ${inputPath}`));
  console.log(chalk.blue(`   输出: ${outputPath}`));
  console.log(chalk.blue(`   格式: ${options.format || 'mp4'}`));
  console.log(chalk.blue(`   质量: ${options.quality}`));
  
  if (options.width && options.height) {
    console.log(chalk.blue(`   尺寸: ${options.width}x${options.height}`));
  }
  
  try {
    const { convertVideo } = require('./utils');
    
    await convertVideo(inputPath, outputPath, {
      format: options.format,
      quality: parseInt(options.quality),
      width: options.width ? parseInt(options.width) : null,
      height: options.height ? parseInt(options.height) : null
    });
    
    console.log(chalk.green('\n✅ 格式转换完成！'));
    console.log(chalk.cyan(`   文件: ${outputPath}`));
    
  } catch (error) {
    console.error(chalk.red('❌ 格式转换失败:'), error.message);
    throw error;
  }
}

// 运行检查命令
async function runCheckCommand() {
  console.log(chalk.cyan('🔍 系统环境检查'));
  
  console.log(chalk.blue('\n📋 基本信息:'));
  console.log(chalk.blue(`   Node.js: ${process.version}`));
  console.log(chalk.blue(`   平台: ${process.platform} ${process.arch}`));
  console.log(chalk.blue(`   工具版本: ${packageJson.version}`));
  
  console.log(chalk.blue('\n🔧 依赖检查:'));
  const depsOk = await checkDependencies();
  
  console.log(chalk.blue('\n🎥 FFmpeg检查:'));
  const ffmpegOk = await checkFFmpeg();
  
  console.log(chalk.blue('\n📁 目录检查:'));
  const requiredDirs = ['recordings', 'configs', 'logs'];
  requiredDirs.forEach(dir => {
    const dirPath = path.join(process.cwd(), dir);
    const exists = fs.existsSync(dirPath);
    console.log(chalk[exists ? 'green' : 'red'](`   ${dir}: ${exists ? '✅ 存在' : '❌ 缺失'}`));
  });
  
  const allOk = depsOk && ffmpegOk;
  console.log(chalk[allOk ? 'green' : 'yellow'](`\n${allOk ? '✅' : '⚠️ '} 检查完成: ${allOk ? '所有检查通过' : '存在一些问题'}`));
}

// 运行演示命令
async function runDemoCommand(options) {
  const { main } = require('../examples/basic-recording');
  await main();
}

// 辅助函数：加载配置文件
async function loadConfigFile(configPath) {
  try {
    const fullPath = path.isAbsolute(configPath) ? configPath : path.join(process.cwd(), configPath);
    return await fs.readJson(fullPath);
  } catch (error) {
    console.error(chalk.red(`❌ 加载配置文件失败: ${configPath}`), error.message);
    return null;
  }
}

// 辅助函数：生成输出路径
function generateOutputPath(prefix, extension) {
  const timestamp = new Date().toISOString()
    .replace(/[:.]/g, '-')
    .replace('T', '_')
    .split('.')[0];
  
  const filename = `${prefix}_${timestamp}.${extension}`;
  return path.join('./recordings', filename);
}

// 解析命令行参数
program.parse(process.argv);

// 如果没有提供命令，显示帮助
if (!process.argv.slice(2).length) {
  program.help();
}