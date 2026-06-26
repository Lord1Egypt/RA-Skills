#!/usr/bin/env node

const readline = require('readline');
const { generateAssessment } = require('./rules');

function splitList(value) {
  return (value || '').split(',').map(item => item.trim()).filter(Boolean);
}

function parseArgs() {
  const args = process.argv.slice(2);
  const input = {};

  for (let i = 0; i < args.length; i += 1) {
    const key = args[i];
    const value = args[i + 1];
    switch (key) {
      case '--project':
        input.project = value;
        i += 1;
        break;
      case '--industry':
        input.industry = value;
        i += 1;
        break;
      case '--type':
        input.type = value;
        i += 1;
        break;
      case '--cycle':
        input.cycle = value;
        i += 1;
        break;
      case '--team-size':
        input.teamSize = value;
        i += 1;
        break;
      case '--payment':
        input.payment = value;
        i += 1;
        break;
      case '--client-location':
        input.clientLocation = value;
        i += 1;
        break;
      case '--phase':
        input.phase = value;
        i += 1;
        break;
      case '--signals':
        input.signals = splitList(value);
        i += 1;
        break;
      default:
        break;
    }
  }

  return input;
}

function printList(items, prefix = '  - ') {
  items.forEach(item => console.log(`${prefix}${item}`));
}

function printOutput(result) {
  console.log('');
  console.log('='.repeat(64));
  console.log('delivery-risk-compass | 项目交付罗盘');
  console.log('='.repeat(64));
  console.log(`项目: ${result.project}`);
  console.log(`行业: ${result.industry} (${result.industryProfile.label})`);
  console.log(`类型: ${result.type}`);
  console.log(`周期: ${result.cycle}`);
  console.log(`团队: ${result.teamSize}`);
  console.log(`付款: ${result.payment}`);
  console.log('');

  console.log('1. 项目健康度');
  console.log(`评分: ${result.healthScore}/100 (${result.healthLevel})`);
  if (result.warnings.length === 0) {
    console.log('  - 暂未检测到明显风险信号。');
  } else {
    printList(result.warnings);
  }
  console.log('');

  console.log('2. 当前阶段建议');
  console.log(`阶段: ${result.currentPhase}`);
  console.log(result.phaseAdvice.overall);
  printList(result.phaseAdvice.key_points);
  console.log('交付物:');
  printList(result.phaseAdvice.deliverables);
  console.log('检查点:');
  printList(result.phaseAdvice.checkpoints);
  console.log('');

  console.log('3. 行业风险侧重点');
  console.log('优先关注:');
  printList(result.industryProfile.priorities);
  console.log('常见风险:');
  printList(result.industryProfile.watchouts);
  console.log('');

  console.log('4. 推荐卡点');
  result.recommendedPitfalls.forEach(item => {
    console.log(`  [${item.severityLabel}] ${item.name}`);
    console.log(`    ${item.description}`);
    console.log(`    应对: ${item.mitigation}`);
    console.log(`    来源: ${item.from}`);
  });
  console.log('');

  console.log('5. 沟通策略');
  Object.entries(result.communicationStrategy.stakeholder_strategy).forEach(([role, strategy]) => {
    console.log(`  ${role}: ${strategy.frequency}`);
    console.log(`    形式: ${strategy.format}`);
    console.log(`    提示: ${strategy.tip}`);
  });
  console.log('升级规则:');
  result.communicationStrategy.escalation_rules.forEach(rule => {
    console.log(`  - ${rule.condition} -> ${rule.action}`);
  });
  console.log('');

  console.log('6. 救急方案');
  result.emergencyPlans.forEach(plan => {
    console.log(`  ${plan.situation} (${plan.from})`);
    printList(plan.actions, '    - ');
  });
  console.log('');

  console.log('7. 下一步');
  printList(result.nextMoves);
  console.log('');
  console.log(`经验提示: ${result.tip}`);
  console.log('='.repeat(64));
}

async function interactive() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  const ask = question => new Promise(resolve => rl.question(question, resolve));

  console.log('');
  console.log('delivery-risk-compass | 项目交付罗盘');
  const project = await ask('项目名称: ');
  const industry = await ask('所属行业: ');
  const type = (await ask('项目类型 (纯开发/实施+开发/纯实施/运维) [实施+开发]: ')) || '实施+开发';
  const cycle = await ask('预期周期 (如: 6个月): ');
  const teamSize = await ask('团队人数 (可选): ');
  const payment = await ask('付款方式 (可选): ');
  const clientLocation = (await ask('交付方式 (驻场/远程/混合) [混合]: ')) || '混合';
  const phase = await ask('当前阶段 (可选): ');
  const signals = splitList(await ask('风险信号 (逗号分隔，可选): '));
  rl.close();

  printOutput(generateAssessment({ project, industry, type, cycle, teamSize, payment, clientLocation, phase, signals }));
}

if (process.argv.includes('--quick')) {
  const input = parseArgs();
  if (!input.project || !input.industry) {
    console.error('快速模式需要至少指定 --project 和 --industry');
    console.error('示例: delivery-risk-compass --quick --project "某平台升级项目" --industry "政府/公共服务"');
    process.exit(1);
  }
  printOutput(generateAssessment(input));
} else {
  interactive().catch(error => {
    console.error(error);
    process.exit(1);
  });
}
