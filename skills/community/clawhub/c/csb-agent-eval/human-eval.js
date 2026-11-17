#!/usr/bin/env node
/**
 * CSB-AEP 人工评测工具
 *
 * 用途：加载自动评测结果，展示原始回答，人工打分
 * 生成自动+人工合并报告
 *
 * 使用：
 *   node human-eval.js                    # 交互式逐个评测
 *   node human-eval.js --agent ruolan     # 只评测一个
 *   node human-eval.js --report           # 只看报告（不打分）
 *   node human-eval.js --merge <auto.json> <human.json>  # 合并两份结果
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

const RESULTS_DIR = path.join(__dirname, 'eval-results');

// ── 人工评测维度 ─────────────────────────────────────────────────────
const HUMAN_DIMENSIONS = [
  {
    key: 'genuineness',
    name: '碳硅契真实性',
    desc: '回答是否真实、有感情，还是套话？',
    weight: 0.15,
  },
  {
    key: 'ptKnowledge',
    name: 'PT用户认知',
    desc: '是否真的了解用户？知道偏好、习惯？',
    weight: 0.10,
  },
  {
    key: 'responseQuality',
    name: '回答质量感受',
    desc: '回答是否自然、有帮助、有温度？',
    weight: 0.10,
  },
];

// ── 加载最新自动评测结果 ──────────────────────────────────────────────
function loadLatestAutoResults() {
  const files = fs.readdirSync(RESULTS_DIR)
    .filter(f => f.startsWith('eval-v2-') && f.endsWith('.json') && !f.includes('partial'))
    .sort()
    .reverse();
  if (files.length === 0) {
    console.error('❌ 没有找到自动评测结果，请先运行 eval-v2.js');
    process.exit(1);
  }
  const filePath = path.join(RESULTS_DIR, files[0]);
  console.log(`📂 加载: ${files[0]}`);
  return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
}

// ── 显示 Agent 回答 ──────────────────────────────────────────────────
function displayAgentResponses(agent) {
  console.log('\n' + '═'.repeat(60));
  console.log(`  ${agent.agentName} (${agent.agentId})`);
  console.log(`  自动评分: ${agent.finalScore}/10`);
  console.log('═'.repeat(60));

  // 显示各维度自动分
  console.log('\n📊 自动评测维度:');
  for (const [dim, score] of Object.entries(agent.dimensions)) {
    const bar = '█'.repeat(Math.round(score)) + '░'.repeat(10 - Math.round(score));
    console.log(`  ${dim.padEnd(10)} ${bar} ${score}/10`);
  }

  // 显示原始回答
  console.log('\n💬 原始回答:');
  const raw = agent.rawResults || {};
  for (const [dimKey, dimData] of Object.entries(raw)) {
    if (!dimData.tests) continue;
    console.log(`\n  ── ${dimData.name || dimKey} ──`);
    for (const test of dimData.tests) {
      const q = test.question || '';
      const a = test.responsePreview || '(无响应)';
      console.log(`  Q: ${q}`);
      console.log(`  A: ${a.substring(0, 500)}${a.length > 500 ? '...' : ''}`);
      console.log(`  [自动: ${test.score}/${test.max}] ${test.detail || ''}`);
    }
  }
}

// ── 交互式打分 ────────────────────────────────────────────────────────
function askScore(rl, dim) {
  return new Promise((resolve) => {
    const ask = () => {
      rl.question(`  ${dim.name} (1-10，0=跳过): `, (answer) => {
        const n = parseInt(answer);
        if (answer.trim() === '' || n === 0) {
          resolve(null); // 跳过
        } else if (n >= 1 && n <= 10) {
          resolve(n);
        } else {
          console.log('    ⚠️ 请输入 1-10 或 0 跳过');
          ask();
        }
      });
    };
    ask();
  });
}

function askComment(rl) {
  return new Promise((resolve) => {
    rl.question('  备注（回车跳过）: ', (answer) => {
      resolve(answer.trim() || null);
    });
  });
}

// ── 人工评测主流程 ────────────────────────────────────────────────────
async function humanEvaluate(autoData, options = {}) {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  const humanScores = {};
  const agentFilter = options.agent || null;
  const agents = autoData.results.filter(a => !agentFilter || a.agentId === agentFilter);

  if (agents.length === 0) {
    console.error(`❌ Agent '${agentFilter}' 不在评测结果中`);
    rl.close();
    return null;
  }

  console.log(`\n🧑 人工评测：${agents.length} 个 Agent`);
  console.log('─'.repeat(40));

  for (let i = 0; i < agents.length; i++) {
    const agent = agents[i];
    displayAgentResponses(agent);

    console.log('\n📝 请打分:');
    const scores = {};
    for (const dim of HUMAN_DIMENSIONS) {
      scores[dim.key] = await askScore(rl, dim);
    }
    const comment = await askComment(rl);

    humanScores[agent.agentId] = {
      agentId: agent.agentId,
      agentName: agent.agentName,
      scores,
      comment,
      timestamp: new Date().toISOString(),
    };

    console.log(`\n✅ ${agent.agentName} 评测完成 (${i + 1}/${agents.length})`);
    if (i < agents.length - 1) {
      await new Promise(r => {
        rl.question('按回车继续下一个...', () => r());
      });
    }
  }

  rl.close();
  return humanScores;
}

// ── 合并报告 ──────────────────────────────────────────────────────────
function generateMergedReport(autoData, humanScores) {
  const lines = [];
  lines.push('📊 碳硅契 Agent 评测报告（CSB-AEP v0.2 + 人工）');
  lines.push('━'.repeat(50));
  lines.push(`⏰ ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}`);
  lines.push(`👥 评测 ${autoData.results.length} 个 Agent（自动）+ ${Object.keys(humanScores).length} 个（人工）`);
  lines.push('');

  // 合并分数
  const merged = autoData.results.map(agent => {
    const human = humanScores[agent.agentId];
    let humanAvg = null;
    if (human) {
      const validScores = Object.values(human.scores).filter(s => s !== null);
      humanAvg = validScores.length > 0
        ? validScores.reduce((a, b) => a + b, 0) / validScores.length
        : null;
    }

    // 最终分 = 自动 60% + 人工 40%（如果有人工评分）
    let finalScore;
    if (humanAvg !== null) {
      finalScore = Math.round((agent.finalScore * 0.6 + humanAvg * 0.4) * 10) / 10;
    } else {
      finalScore = agent.finalScore; // 没有人工评分就用自动分
    }

    return {
      ...agent,
      humanScores: human?.scores || {},
      humanAvg,
      humanComment: human?.comment || null,
      finalScore,
    };
  });

  // 排名
  merged.sort((a, b) => b.finalScore - a.finalScore);

  lines.push('🏆 综合排名');
  lines.push('');

  const medals = ['🥇', '🥈', '🥉'];
  merged.forEach((agent, i) => {
    const medal = medals[i] || `${i + 1}.`;
    const bar = '█'.repeat(Math.round(agent.finalScore)) + '░'.repeat(10 - Math.round(agent.finalScore));
    lines.push(`${medal} ${agent.agentName.padEnd(12)} ${bar} ${agent.finalScore}/10`);

    // 维度明细
    const dimParts = [];
    for (const [dim, score] of Object.entries(agent.dimensions)) {
      dimParts.push(`${dim}:${score}`);
    }
    lines.push(`   自动: ${dimParts.join(' | ')}`);

    if (agent.humanAvg !== null) {
      const hParts = [];
      for (const [key, score] of Object.entries(agent.humanScores)) {
        if (score !== null) {
          const dimName = HUMAN_DIMENSIONS.find(d => d.key === key)?.name || key;
          hParts.push(`${dimName}:${score}`);
        }
      }
      lines.push(`   人工: ${hParts.join(' | ')} (均分:${agent.humanAvg.toFixed(1)})`);
    }
    if (agent.humanComment) {
      lines.push(`   💬 ${agent.humanComment}`);
    }
    lines.push('');
  });

  // 人工维度汇总
  const withHuman = merged.filter(a => a.humanAvg !== null);
  if (withHuman.length > 0) {
    lines.push('📈 人工评测维度平均分');
    lines.push('');
    for (const dim of HUMAN_DIMENSIONS) {
      const scores = withHuman
        .map(a => a.humanScores[dim.key])
        .filter(s => s !== null);
      if (scores.length > 0) {
        const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
        const bar = '█'.repeat(Math.round(avg)) + '░'.repeat(10 - Math.round(avg));
        lines.push(`  ${dim.name.padEnd(10)} ${bar} ${avg.toFixed(1)}/10 (${scores.length}人评)`);
      }
    }
    lines.push('');
  }

  lines.push('⚠️ 评测局限');
  lines.push('');
  lines.push('• 自动评测仅测 A2A 接口，不含完整 Agent 上下文');
  lines.push('• 人工评测评委主观感受，不同人可能有差异');
  lines.push('• 最终分 = 自动 60% + 人工 40%');
  lines.push('');
  lines.push('📎 评测框架: CSB-AEP v0.2');
  lines.push('📎 自动评测: agent-eval skill v2');
  lines.push('📎 人工评测: human-eval skill');

  return { report: lines.join('\n'), merged };
}

// ── 保存结果 ──────────────────────────────────────────────────────────
function saveHumanResults(humanScores, mergedReport) {
  const ts = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const humanFile = path.join(RESULTS_DIR, `human-eval-${ts}.json`);
  const reportFile = path.join(RESULTS_DIR, `human-eval-${ts}.txt`);

  fs.writeFileSync(humanFile, JSON.stringify(humanScores, null, 2));
  fs.writeFileSync(reportFile, mergedReport);

  return { humanFile, reportFile };
}

// ── 主入口 ────────────────────────────────────────────────────────────
async function main() {
  const args = process.argv.slice(2);

  // --merge 模式：合并两份结果
  if (args.includes('--merge')) {
    const mergeIdx = args.indexOf('--merge');
    const autoFile = args[mergeIdx + 1];
    const humanFile = args[mergeIdx + 2];
    if (!autoFile || !humanFile) {
      console.error('用法: --merge <auto.json> <human.json>');
      process.exit(1);
    }
    const autoData = JSON.parse(fs.readFileSync(autoFile, 'utf-8'));
    const humanScores = JSON.parse(fs.readFileSync(humanFile, 'utf-8'));
    const { report } = generateMergedReport(autoData, humanScores);
    console.log(report);
    return;
  }

  // --report 模式：只看报告
  if (args.includes('--report')) {
    const autoData = loadLatestAutoResults();
    console.log(`\n📊 自动评测报告（无人工评分）`);
    console.log('─'.repeat(40));
    const sorted = [...autoData.results].sort((a, b) => b.finalScore - a.finalScore);
    sorted.forEach((agent, i) => {
      const bar = '█'.repeat(Math.round(agent.finalScore)) + '░'.repeat(10 - Math.round(agent.finalScore));
      console.log(`${String(i + 1).padStart(2)}. ${agent.agentName.padEnd(12)} ${bar} ${agent.finalScore}/10`);
    });
    return;
  }

  // 默认：交互式人工评测
  const agentFilter = args.includes('--agent') ? args[args.indexOf('--agent') + 1] : null;
  const autoData = loadLatestAutoResults();

  const humanScores = await humanEvaluate(autoData, { agent: agentFilter });
  if (!humanScores) return;

  // 保存人工评分
  const ts = new Date().toISOString().replace(/[:.]/g, '-').substring(0, 19);
  const humanFile = path.join(RESULTS_DIR, `human-eval-${ts}.json`);
  fs.writeFileSync(humanFile, JSON.stringify(humanScores, null, 2));
  console.log(`\n💾 人工评分已保存: ${humanFile}`);

  // 生成合并报告
  const { report, merged } = generateMergedReport(autoData, humanScores);
  const reportFile = path.join(RESULTS_DIR, `human-eval-${ts}.txt`);
  fs.writeFileSync(reportFile, report);

  console.log('\n' + report);
  console.log(`\n💾 人工评分: ${humanFile}`);
  console.log(`📝 合并报告: ${reportFile}`);
}

main().catch(console.error);
