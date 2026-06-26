#!/usr/bin/env node

/**
 * Figma设计分析命令行工具 - JavaScript版本
 * 统一接口，支持文件信息获取、设计属性提取、截图导出和比对验证功能
 */

const fs = require('fs');
const path = require('path');
const { program } = require('commander');
const chalk = require('chalk');
require('dotenv').config(); // 加载.env文件

// 导入各个功能模块
const { getFileInfo, parseFileId } = require('./modules/file-info');
const { extractDesignSystem } = require('./modules/design-extractor');
const { exportScreenshot } = require('./modules/screenshot-exporter');
const { compareWithImplementation } = require('./modules/design-comparator');

// 工具函数
function getFigmaToken() {
  const token = process.env.FIGMA_ACCESS_TOKEN;
  if (!token) {
    console.error(chalk.red('错误: 未设置FIGMA_ACCESS_TOKEN环境变量'));
    console.error(chalk.yellow('请选择以下方式之一设置令牌:'));
    console.error(chalk.yellow('1. 使用.env文件: cp .env.example .env 并填写您的令牌'));
    console.error(chalk.yellow('2. 直接设置环境变量: export FIGMA_ACCESS_TOKEN=your_token'));
    console.error(chalk.yellow('3. 临时设置: FIGMA_ACCESS_TOKEN=your_token node scripts/figma-cli.js ...'));
    process.exit(1);
  }
  return token;
}

function saveOutput(data, outputPath, format = 'json') {
  try {
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }

    if (format === 'json') {
      fs.writeFileSync(outputPath, JSON.stringify(data, null, 2), 'utf8');
      console.log(chalk.green(`结果已保存到: ${outputPath}`));
    } else if (format === 'txt') {
      fs.writeFileSync(outputPath, data.toString(), 'utf8');
      console.log(chalk.green(`结果已保存到: ${outputPath}`));
    } else {
      console.error(chalk.red(`不支持的输出格式: ${format}`));
    }
  } catch (error) {
    console.error(chalk.red(`保存文件时出错: ${error.message}`));
  }
}

// 命令处理函数
async function handleInfo(fileInput, outputPath) {
  const token = getFigmaToken();
  const fileId = parseFileId(fileInput);

  console.log(chalk.blue(`获取文件信息: ${fileId}`));
  const result = await getFileInfo(fileId, token);

  if (outputPath) {
    saveOutput(result, outputPath);
  } else {
    console.log(JSON.stringify(result, null, 2));
  }

  return result;
}

async function handleExtract(fileInput, outputPath) {
  const token = getFigmaToken();
  const fileId = parseFileId(fileInput);

  console.log(chalk.blue(`提取设计属性: ${fileId}`));
  const result = await extractDesignSystem(fileId, token);

  if (outputPath) {
    saveOutput(result, outputPath);
  } else {
    console.log(JSON.stringify(result, null, 2));
  }

  return result;
}

async function handleExport(fileInput, nodeId, options) {
  const token = getFigmaToken();
  const fileId = parseFileId(fileInput);

  console.log(chalk.blue(`导出截图: ${fileId}, 节点: ${nodeId}`));
  const result = await exportScreenshot(
    fileId,
    nodeId,
    token,
    options.format,
    options.scale
  );

  if (options.output) {
    if (result.imagePath) {
      console.log(chalk.green(`截图已保存到: ${result.imagePath}`));
    } else {
      saveOutput(result, options.output);
    }
  }

  return result;
}

async function handleCompare(fileInput, implementationPath, outputPath) {
  const token = getFigmaToken();
  const fileId = parseFileId(fileInput);

  console.log(chalk.blue(`比对验证: ${fileId} 与 ${implementationPath}`));
  const result = await compareWithImplementation(fileId, implementationPath, token);

  if (outputPath) {
    saveOutput(result, outputPath);
  } else {
    console.log(JSON.stringify(result, null, 2));
  }

  return result;
}

// 设置命令行程序
program
  .name('figma-analyzer')
  .description('Figma设计分析工具 - 提取设计系统、导出截图、验证实现')
  .version('1.0.0');

// info命令
program
  .command('info')
  .description('获取Figma文件信息')
  .argument('<file>', 'Figma文件URL或ID')
  .option('-o, --output <path>', '输出文件路径')
  .action(async (file, options) => {
    try {
      await handleInfo(file, options.output);
    } catch (error) {
      console.error(chalk.red(`执行失败: ${error.message}`));
      process.exit(1);
    }
  });

// extract命令
program
  .command('extract')
  .description('提取设计系统数据')
  .argument('<file>', 'Figma文件URL或ID')
  .option('-o, --output <path>', '输出文件路径')
  .action(async (file, options) => {
    try {
      await handleExtract(file, options.output);
    } catch (error) {
      console.error(chalk.red(`执行失败: ${error.message}`));
      process.exit(1);
    }
  });

// export命令
program
  .command('export')
  .description('导出设计节点截图')
  .argument('<file>', 'Figma文件URL或ID')
  .requiredOption('--node-id <id>', '节点ID')
  .option('--format <format>', '图片格式', 'png')
  .option('--scale <scale>', '缩放比例', '1')
  .option('-o, --output <path>', '输出文件路径')
  .action(async (file, options) => {
    try {
      await handleExport(file, options.nodeId, {
        format: options.format,
        scale: parseFloat(options.scale),
        output: options.output
      });
    } catch (error) {
      console.error(chalk.red(`执行失败: ${error.message}`));
      process.exit(1);
    }
  });

// compare命令
program
  .command('compare')
  .description('比对设计与实现')
  .argument('<file>', 'Figma文件URL或ID')
  .argument('<implementation>', '实现文件路径（CSS/代码）')
  .option('-o, --output <path>', '输出文件路径')
  .action(async (file, implementation, options) => {
    try {
      await handleCompare(file, implementation, options.output);
    } catch (error) {
      console.error(chalk.red(`执行失败: ${error.message}`));
      process.exit(1);
    }
  });

// 如果没有提供命令，显示帮助
if (process.argv.length <= 2) {
  program.help();
}

program.parse(process.argv);