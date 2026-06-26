#!/usr/bin/env node
/**
 * ClawGuard v3 - Auditor CLI
 * Skill 安装前审计，支持意图偏离检测
 */

const path = require('path');
const fs = require('fs');
const { Auditor } = require('./src/auditor.js');

const args = process.argv.slice(2);
const options = {
  skillPath: null,
  deep: args.includes('--deep'),
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
    options.skillPath = args[i];
  }
}

if (!options.skillPath) {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║           🦞 ClawGuard v3 - Auditor (审计器)               ║
╠═══════════════════════════════════════════════════════════════╣
║  用法: node cli.js <skill-path> [选项]                       ║
║                                                               ║
║  选项:                                                        ║
║    --deep      深度审计模式（启用 ML 检测）                   ║
║    --output    输出报告文件路径                               ║
║    --format    输出格式 (table|json|markdown)                ║
║                                                               ║
║  示例:                                                        ║
║    node cli.js ./my-skill                                    ║
║    node cli.js ./my-skill --deep --output report.json         ║
╚═══════════════════════════════════════════════════════════════╝
  `);
  process.exit(0);
}

// 确保路径存在
if (!fs.existsSync(options.skillPath)) {
  console.error(`❌ 路径不存在: ${options.skillPath}`);
  process.exit(1);
}

async function main() {
  console.log(`\n🦞 ClawGuard v3 Auditor - 审计中...\n`);

  const auditor = new Auditor(options);
  const report = await auditor.audit(options.skillPath);

  // 输出报告
  if (options.output) {
    fs.writeFileSync(options.output, JSON.stringify(report, null, 2));
    console.log(`✅ 报告已保存到: ${options.output}`);
  }

  // 根据风险等级返回退出码
  const exitCode = getExitCode(report.riskLevel);
  process.exit(exitCode);
}

function getExitCode(riskLevel) {
  switch (riskLevel) {
    case 'TIER_0':
    case 'TIER_1':
      return 0;  // 安全
    case 'TIER_2':
      return 1;  // 需审核
    case 'TIER_3':
      return 2;  // 高危
    case 'TIER_4':
      return 3;  // 严重
    default:
      return 1;
  }
}

main().catch(err => {
  console.error('❌ 审计失败:', err.message);
  process.exit(1);
});
