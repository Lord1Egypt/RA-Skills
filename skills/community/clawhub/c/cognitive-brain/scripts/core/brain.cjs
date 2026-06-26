#!/usr/bin/env node
/**
 * Cognitive Brain - 统一命令行接口
 * 快速访问所有功能
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('brain');
const path = require('path');
const { execSync } = require('child_process'); // 未使用，改用 spawn

const SKILL_DIR = path.dirname(__dirname);

const COMMANDS = {
  // 核心功能
  'encode': '编码记忆',
  'recall': '检索记忆',
  'reflect': '自我反思',
  'forget': '遗忘记忆',
  
  // 高级功能
  'associate': '联想网络',
  'auto_associate': '自动构建联想',
  'user_model': '用户建模',
  'prediction': '预测',
  'working_memory': '工作记忆',
  'goal_management': '目标管理',
  
  // 工具
  'batch_encode': '批量编码',
  'export': '导出数据',
  'health_check': '健康检查',
  'perf_monitor': '性能监控',
  
  // 辅助
  'selfaware': '自我认知',
  'safety': '安全检查',
  'dialogue': '对话管理',
  'intent': '意图识别',
  'emotion': '情感分析'
};

function showHelp() {
  console.log(`
🧠 Cognitive Brain 统一接口

用法:
  node brain.cjs <命令> [参数]

核心功能:
  encode <内容>           编码记忆
  recall <查询>           检索记忆
  reflect                自我反思
  forget <ID>            遗忘记忆

高级功能:
  associate              管理联想网络
  auto_associate         自动构建联想
  user_model             用户建模
  prediction             预测
  working_memory         工作记忆
  goal_management        目标管理

工具:
  batch_encode <文件>    批量编码
  export [json|md|csv]   导出数据
  health_check           健康检查
  perf_monitor report    性能报告

示例:
  node brain.cjs encode "今天学习了新技能"
  node brain.cjs recall "技能"
  node brain.cjs export md
  node brain.cjs health_check
`);
}

async function main() {
  const args = process.argv.slice(2);
  const cmd = args[0];
  
  if (!cmd || cmd === 'help' || cmd === '--help') {
    showHelp();
    return;
  }
  
  // 查找脚本
  const scriptPath = path.join(SKILL_DIR, 'scripts', `${cmd}.cjs`);
  
  if (!require('fs').existsSync(scriptPath)) {
    console.log(`❌ 未知命令: ${cmd}`);
    console.log('运行 `node brain.cjs help` 查看帮助');
    process.exit(1);
  }
  
  // 执行脚本（使用 spawn 避免命令注入）
  const { spawn } = require('child_process');
  const scriptArgs = args.slice(1);

  try {
    const result = spawn('node', [scriptPath, ...scriptArgs], {
      cwd: SKILL_DIR,
      stdio: 'inherit'
    });
    result.on('error', (err) => {
      console.error('执行失败:', err.message);
    });
  } catch (e) { console.error("[brain] 错误:", e.message);
    // 错误已在脚本中输出
  }
}

main();

