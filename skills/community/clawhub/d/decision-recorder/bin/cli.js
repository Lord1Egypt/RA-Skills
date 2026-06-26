#!/usr/bin/env node
/**
 * Decision Recorder CLI
 * 命令行接口实现
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');
const {
  detectDecisionKeywords,
  createDecision,
  listDecisions,
  searchDecisions,
  getDecision,
  analyzeDecisions,
  deleteDecision,
  updateDecision,
  DECISION_KEYWORDS
} = require('./index');

const COLORS = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m'
};

function color(name, text) {
  return `${COLORS[name]}${text}${COLORS.reset}`;
}

function printHelp() {
  console.log(`
${color('bright', '决策记录器 (Decision Recorder)')}

用法: decision-recorder <command> [options]

命令:
  record, r          记录一个新决策
  list, ls           列出所有决策记录
  search, s <query>  搜索决策记录
  analyze, a         分析决策模式
  view, v <id>       查看单个决策详情
  delete, d <id>     删除决策记录
  update, u <id>     更新决策记录
  detect <text>      检测文本是否包含决策关键词
  keywords           显示所有决策关键词
  help, h            显示帮助信息

示例:
  decision-recorder record
  decision-recorder list --tag=重要
  decision-recorder search "技术选型"
  decision-recorder analyze
  decision-recorder detect "我决定使用 Node.js"
`);
}

async function prompt(question) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

async function promptMultiLine(question) {
  console.log(question);
  console.log(color('dim', '(输入空行结束)'));
  
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  const lines = [];
  
  return new Promise(resolve => {
    rl.on('line', line => {
      if (line.trim() === '') {
        rl.close();
        resolve(lines.join('\n'));
      } else {
        lines.push(line);
      }
    });
  });
}

async function cmdRecord(args) {
  console.log(color('cyan', '\n📝 记录新决策\n'));
  
  const question = await prompt('决策问题: ');
  if (!question) {
    console.log(color('red', '❌ 决策问题不能为空'));
    return;
  }
  
  console.log(color('dim', '\n输入选项 (每行一个，空行结束):'));
  const options = [];
  let option;
  while ((option = await prompt(`选项 ${options.length + 1}: `))) {
    options.push(option);
  }
  
  const reasoning = await promptMultiLine('\n决策理由:');
  const result = await prompt('最终选择: ');
  const context = await promptMultiLine('\n决策背景/上下文:');
  const tagsInput = await prompt('标签 (用逗号分隔): ');
  const tags = tagsInput.split(',').map(t => t.trim()).filter(t => t);
  
  const decision = {
    question,
    options,
    reasoning,
    result,
    context,
    tags
  };
  
  const record = createDecision(decision);
  
  console.log(color('green', `\n✅ 决策已记录! ID: ${record.id}`));
  console.log(color('dim', `时间: ${record.timestamp}`));
}

function cmdList(args) {
  const filters = {};
  
  // 解析参数
  args.forEach(arg => {
    if (arg.startsWith('--tag=')) {
      filters.tag = arg.split('=')[1];
    } else if (arg.startsWith('--from=')) {
      filters.dateFrom = arg.split('=')[1];
    } else if (arg.startsWith('--to=')) {
      filters.dateTo = arg.split('=')[1];
    }
  });
  
  const decisions = listDecisions(filters);
  
  if (decisions.length === 0) {
    console.log(color('yellow', '暂无决策记录'));
    return;
  }
  
  console.log(color('cyan', `\n📋 共找到 ${decisions.length} 条决策记录\n`));
  
  decisions.forEach((d, i) => {
    const date = new Date(d.timestamp).toLocaleString('zh-CN');
    const tags = d.tags && d.tags.length > 0 
      ? d.tags.map(t => color('magenta', `[${t}]`)).join(' ')
      : '';
    
    console.log(`${color('dim', `${i + 1}.`)} ${color('bright', d.id)}`);
    console.log(`   ${color('blue', '📅')} ${date}`);
    console.log(`   ${color('yellow', '❓')} ${d.question}`);
    if (d.result) {
      console.log(`   ${color('green', '✓')} ${d.result}`);
    }
    if (tags) {
      console.log(`   ${tags}`);
    }
    console.log();
  });
}

function cmdSearch(args) {
  const query = args.join(' ');
  if (!query) {
    console.log(color('red', '❌ 请提供搜索关键词'));
    return;
  }
  
  const decisions = searchDecisions(query);
  
  if (decisions.length === 0) {
    console.log(color('yellow', `未找到包含 "${query}" 的决策记录`));
    return;
  }
  
  console.log(color('cyan', `\n🔍 找到 ${decisions.length} 条相关决策\n`));
  
  decisions.forEach((d, i) => {
    const date = new Date(d.timestamp).toLocaleString('zh-CN');
    console.log(`${color('dim', `${i + 1}.`)} ${color('bright', d.id)}`);
    console.log(`   ${color('blue', '📅')} ${date}`);
    console.log(`   ${color('yellow', '❓')} ${highlight(d.question, query)}`);
    if (d.result) {
      console.log(`   ${color('green', '✓')} ${highlight(d.result, query)}`);
    }
    console.log();
  });
}

function highlight(text, query) {
  if (!text) return '';
  const regex = new RegExp(`(${query})`, 'gi');
  return text.replace(regex, `${COLORS.red}$1${COLORS.reset}`);
}

function cmdAnalyze() {
  const analysis = analyzeDecisions();
  
  console.log(color('cyan', '\n📊 决策分析报告\n'));
  console.log(`${color('bright', '总计决策数:')} ${analysis.total}`);
  
  if (analysis.total === 0) {
    return;
  }
  
  console.log(`${color('bright', '首次决策:')} ${new Date(analysis.firstDecision).toLocaleString('zh-CN')}`);
  console.log(`${color('bright', '最新决策:')} ${new Date(analysis.latestDecision).toLocaleString('zh-CN')}`);
  
  console.log(color('bright', '\n标签统计:'));
  if (Object.keys(analysis.tagStats).length === 0) {
    console.log('  (无标签)');
  } else {
    Object.entries(analysis.tagStats)
      .sort((a, b) => b[1] - a[1])
      .forEach(([tag, count]) => {
        const bar = '█'.repeat(Math.min(count, 20));
        console.log(`  ${color('magenta', tag)}: ${bar} ${count}`);
      });
  }
  
  console.log(color('bright', '\n高频关键词:'));
  analysis.topKeywords.forEach(([word, count], i) => {
    console.log(`  ${i + 1}. ${word}: ${count} 次`);
  });
  
  console.log(color('bright', '\n决策趋势 (最近10天):'));
  const recentTrend = analysis.trend.slice(-10);
  recentTrend.forEach(t => {
    const bar = '█'.repeat(Math.min(t.count, 10));
    console.log(`  ${t.date}: ${bar} ${t.count}`);
  });
}

function cmdView(args) {
  const id = args[0];
  if (!id) {
    console.log(color('red', '❌ 请提供决策ID'));
    return;
  }
  
  const decision = getDecision(id);
  if (!decision) {
    console.log(color('red', `❌ 未找到ID为 ${id} 的决策记录`));
    return;
  }
  
  const date = new Date(decision.timestamp).toLocaleString('zh-CN');
  
  console.log(color('cyan', '\n📄 决策详情\n'));
  console.log(`${color('bright', 'ID:')} ${decision.id}`);
  console.log(`${color('bright', '时间:')} ${date}`);
  
  if (decision.tags && decision.tags.length > 0) {
    const tags = decision.tags.map(t => color('magenta', `[${t}]`)).join(' ');
    console.log(`${color('bright', '标签:')} ${tags}`);
  }
  
  console.log(color('bright', '\n问题:'));
  console.log(`  ${decision.question}`);
  
  if (decision.options && decision.options.length > 0) {
    console.log(color('bright', '\n选项:'));
    decision.options.forEach((opt, i) => {
      console.log(`  ${i + 1}. ${opt}`);
    });
  }
  
  if (decision.reasoning) {
    console.log(color('bright', '\n决策理由:'));
    console.log(`  ${decision.reasoning}`);
  }
  
  if (decision.result) {
    console.log(color('bright', '\n最终结果:'));
    console.log(`  ${color('green', decision.result)}`);
  }
  
  if (decision.context) {
    console.log(color('bright', '\n决策背景:'));
    console.log(`  ${decision.context}`);
  }
  
  console.log();
}

async function cmdDelete(args) {
  const id = args[0];
  if (!id) {
    console.log(color('red', '❌ 请提供决策ID'));
    return;
  }
  
  const confirm = await prompt(color('yellow', `确定要删除决策 ${id}? (yes/no): `));
  if (confirm.toLowerCase() !== 'yes') {
    console.log('已取消');
    return;
  }
  
  if (deleteDecision(id)) {
    console.log(color('green', `✅ 决策 ${id} 已删除`));
  } else {
    console.log(color('red', `❌ 未找到ID为 ${id} 的决策记录`));
  }
}

async function cmdUpdate(args) {
  const id = args[0];
  if (!id) {
    console.log(color('red', '❌ 请提供决策ID'));
    return;
  }
  
  const decision = getDecision(id);
  if (!decision) {
    console.log(color('red', `❌ 未找到ID为 ${id} 的决策记录`));
    return;
  }
  
  console.log(color('cyan', `\n✏️ 更新决策 ${id}\n`));
  console.log(color('dim', '(直接回车保留原值)\n'));
  
  const question = await prompt(`决策问题 [${decision.question}]: `);
  const result = await prompt(`最终选择 [${decision.result}]: `);
  const tagsInput = await prompt(`标签 [${decision.tags ? decision.tags.join(', ') : ''}]: `);
  
  const updates = {};
  if (question) updates.question = question;
  if (result) updates.result = result;
  if (tagsInput) updates.tags = tagsInput.split(',').map(t => t.trim()).filter(t => t);
  
  if (Object.keys(updates).length === 0) {
    console.log(color('yellow', '没有要更新的内容'));
    return;
  }
  
  const updated = updateDecision(id, updates);
  console.log(color('green', `\n✅ 决策已更新!`));
}

function cmdDetect(args) {
  const text = args.join(' ');
  if (!text) {
    console.log(color('red', '❌ 请提供要检测的文本'));
    return;
  }
  
  const hasKeywords = detectDecisionKeywords(text);
  
  console.log(color('cyan', '\n🔍 决策关键词检测\n'));
  console.log(`文本: "${text}"`);
  console.log(`\n检测结果: ${hasKeywords ? color('green', '✅ 包含决策关键词') : color('yellow', '⚠️ 未检测到决策关键词')}`);
  
  if (hasKeywords) {
    const found = DECISION_KEYWORDS.filter(k => 
      text.toLowerCase().includes(k.toLowerCase())
    );
    console.log(`匹配的关键词: ${found.map(k => color('magenta', k)).join(', ')}`);
  }
  
  console.log(color('dim', `\n所有关键词: ${DECISION_KEYWORDS.join(', ')}`));
}

function cmdKeywords() {
  console.log(color('cyan', '\n🔑 决策关键词列表\n'));
  console.log('中文关键词:');
  DECISION_KEYWORDS.filter(k => /[\u4e00-\u9fa5]/.test(k)).forEach(k => {
    console.log(`  • ${k}`);
  });
  console.log('\n英文关键词:');
  DECISION_KEYWORDS.filter(k => !/[\u4e00-\u9fa5]/.test(k)).forEach(k => {
    console.log(`  • ${k}`);
  });
}

function runCLI() {
  const args = process.argv.slice(2);
  const command = args[0];
  const commandArgs = args.slice(1);
  
  switch (command) {
    case 'record':
    case 'r':
      cmdRecord(commandArgs);
      break;
    case 'list':
    case 'ls':
      cmdList(commandArgs);
      break;
    case 'search':
    case 's':
      cmdSearch(commandArgs);
      break;
    case 'analyze':
    case 'a':
      cmdAnalyze();
      break;
    case 'view':
    case 'v':
      cmdView(commandArgs);
      break;
    case 'delete':
    case 'd':
      cmdDelete(commandArgs);
      break;
    case 'update':
    case 'u':
      cmdUpdate(commandArgs);
      break;
    case 'detect':
      cmdDetect(commandArgs);
      break;
    case 'keywords':
      cmdKeywords();
      break;
    case 'help':
    case 'h':
    case '--help':
    case '-h':
    default:
      printHelp();
      break;
  }
}

module.exports = { runCLI };

if (require.main === module) {
  runCLI();
}
