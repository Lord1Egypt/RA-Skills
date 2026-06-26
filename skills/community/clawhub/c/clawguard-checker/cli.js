#!/usr/bin/env node
/**
 * ClawGuard v3 - Checker CLI
 * 配置检查 + 智能加固建议
 */

const path = require('path');
const fs = require('fs');
const { Checker } = require('./src/checker.js');

const args = process.argv.slice(2);
const options = {
  configPath: null,
  deep: args.includes('--deep'),
  fix: args.includes('--fix'),
  output: null,
  format: 'table'
};

// 解析参数
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--output' && args[i + 1]) {
    options.output = args[i + 1];
    i++;
  } else if (args[i] === '--format' && args[i + 1]) {
    options.format = args[i + 1];
    i++;
  } else if (!args[i].startsWith('--')) {
    options.configPath = args[i];
  }
}

if (!options.configPath) {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║           🦞 ClawGuard v3 - Checker (配置检查)          ║
╠═══════════════════════════════════════════════════════════════╣
║  用法: node cli.js [openclaw.json路径] [选项]            ║
║                                                               ║
║  选项:                                                        ║
║    --deep      深度检查模式                                   ║
║    --fix       生成加固配置                                   ║
║    --output    输出报告文件路径                               ║
║    --format    输出格式 (table|json|markdown)               ║
║                                                               ║
║  示例:                                                        ║
║    node cli.js                                                ║
║    node cli.js ~/.openclaw/openclaw.json --fix               ║
║    node cli.js --deep --output report.json                   ║
╚═══════════════════════════════════════════════════════════════╝
  `);
  process.exit(0);
}

// 解析配置路径
let configPath = options.configPath;
if (!fs.existsSync(configPath)) {
  // 尝试常见路径
  const commonPaths = [
    path.join(process.env.HOME || '', '.openclaw', 'openclaw.json'),
    path.join(process.env.HOME || '', '.claw', 'openclaw.json'),
    '/etc/openclaw/openclaw.json'
  ];

  const found = commonPaths.find(p => fs.existsSync(p));
  if (found) {
    configPath = found;
    console.log(`📍 使用默认配置路径: ${configPath}`);
  } else {
    console.error(`❌ 配置文件不存在: ${configPath}`);
    process.exit(1);
  }
}

async function main() {
  console.log(`\n🦞 ClawGuard v3 Checker - 配置检查中...\n`);

  const checker = new Checker(options);
  const report = await checker.check(configPath);

  // 输出报告
  if (options.output) {
    fs.writeFileSync(options.output, JSON.stringify(report, null, 2));
    console.log(`\n✅ 报告已保存到: ${options.output}`);
  }

  // 如果指定了 --fix，生成加固配置
  if (options.fix) {
    const fixedConfig = checker.generateHardenedConfig(report);
    const fixedPath = configPath + '.hardened.json';
    fs.writeFileSync(fixedPath, JSON.stringify(fixedConfig, null, 2));
    console.log(`\n🛡️ 加固配置已生成: ${fixedPath}`);
    console.log('\n💡 使用方法:');
    console.log(`   cp ${configPath} ${configPath}.backup  # 备份原配置`);
    console.log(`   cp ${fixedPath} ${configPath}          # 应用加固配置`);
  }

  // 根据风险等级返回退出码
  const exitCode = report.maxSeverity >= 3 ? 3 : report.maxSeverity >= 2 ? 2 : 0;
  process.exit(exitCode);
}

main().catch(err => {
  console.error('❌ 检查失败:', err.message);
  process.exit(1);
});
