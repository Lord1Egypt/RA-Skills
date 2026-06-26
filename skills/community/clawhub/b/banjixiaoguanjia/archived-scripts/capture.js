#!/usr/bin/env node

/**
 * 班级小管家作业截图命令行工具
 * 用法: node capture.js --course "三上(第11节)" --output ./screenshots
 */

const { BanjixiaoguanjiaCapture } = require('./index');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    course: null,
    output: './screenshots',
    cdpUrl: 'http://localhost:9222'
  };
  
  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--course':
      case '-c':
        options.course = args[++i];
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--cdp':
        options.cdpUrl = args[++i];
        break;
      case '--help':
      case '-h':
        showHelp();
        process.exit(0);
        break;
    }
  }
  
  return options;
}

function showHelp() {
  console.log(`
班级小管家作业截图工具

用法:
  node capture.js --course "三上(第11节)" --output ./screenshots

选项:
  --course, -c    课程名称 (必填)
  --output, -o    输出目录 (默认: ./screenshots)
  --cdp           Chrome 调试端口 URL (默认: http://localhost:9222)
  --help, -h      显示帮助

示例:
  # 截图三上第11节课程
  node capture.js --course "三上(第11节)"

  # 指定输出目录
  node capture.js --course "二下(第35节)" --output ./homework/2026-03-20

前置要求:
  1. Chrome 必须以调试模式启动:
     "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
  
  2. 已登录班级小管家
`);
}

async function main() {
  const options = parseArgs();
  
  if (!options.course) {
    console.error('错误: 请指定课程名称');
    console.error('用法: node capture.js --course "三上(第11节)"');
    process.exit(1);
  }
  
  console.log('=== 班级小管家作业截图 ===');
  console.log(`课程: ${options.course}`);
  console.log(`输出目录: ${options.output}`);
  console.log(`CDP URL: ${options.cdpUrl}`);
  console.log();
  
  const capture = new BanjixiaoguanjiaCapture({
    cdpUrl: options.cdpUrl,
    outputDir: options.output
  });
  
  try {
    const result = await capture.captureCourse(options.course);
    
    if (result) {
      console.log('\n=== 截图完成 ===');
      console.log(`课程: ${result.course}`);
      console.log(`学生数: ${result.students.length}`);
      console.log(`输出目录: ${result.outputDir}`);
    } else {
      console.log('\n截图失败');
      process.exit(1);
    }
  } catch (err) {
    console.error('错误:', err.message);
    process.exit(1);
  }
}

main();
