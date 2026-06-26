#!/usr/bin/env node
/**
 * AI Cost Optimizer - Recommend Model
 * 根据使用场景智能推荐最优 AI 模型
 */

const readline = require('readline');
const MODELS = {
  daily: {
    name: 'DeepSeek V3',
    provider: 'deepseek',
    model: 'deepseek-chat',
    input: 0.27,
    output: 1.08,
    desc: '性价比最高，适合日常对话、写作、编程',
    monthlyCost: 27,
    tokensPerCall: 1000,
  },
  coding: {
    name: 'DeepSeek Coder',
    provider: 'deepseek',
    model: 'deepseek-coder',
    input: 0.27,
    output: 1.08,
    desc: '代码专项优化，适合代码生成、审查',
    monthlyCost: 27,
    tokensPerCall: 1500,
  },
  chinese: {
    name: '智谱 GLM-4',
    provider: 'zhipu',
    model: 'glm-4',
    input: 0.10,
    output: 0.10,
    desc: '中文能力强，适合中文内容创作',
    monthlyCost: 10,
    tokensPerCall: 800,
  },
  complex: {
    name: 'Claude 3.5 Sonnet',
    provider: 'anthropic',
    model: 'claude-3-5-sonnet-20241022',
    input: 17.50,
    output: 52.50,
    desc: '推理能力强，适合复杂任务',
    monthlyCost: 350,
    tokensPerCall: 2000,
  },
  multimodal: {
    name: '通义千问 Plus',
    provider: 'qwen',
    model: 'qwen-plus',
    input: 0.30,
    output: 0.60,
    desc: '多模态支持，图文处理',
    monthlyCost: 36,
    tokensPerCall: 1200,
  },
};

const SCENARIOS = {
  '1': {
    name: '日常对话/写作',
    recommend: 'daily',
    alternatives: ['chinese'],
  },
  '2': {
    name: '编程/代码生成',
    recommend: 'coding',
    alternatives: ['daily'],
  },
  '3': {
    name: '中文内容创作',
    recommend: 'chinese',
    alternatives: ['daily'],
  },
  '4': {
    name: '复杂推理/分析',
    recommend: 'complex',
    alternatives: ['daily'],
  },
  '5': {
    name: '多模态（图文）',
    recommend: 'multimodal',
    alternatives: ['daily'],
  },
};

const FREQUENCY = {
  '1': { label: '< 100 次/天', factor: 0.1 },
  '2': { label: '100-1000 次/天', factor: 1 },
  '3': { label: '1000-10000 次/天', factor: 10 },
  '4': { label: '> 10000 次/天', factor: 50 },
};

const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';

async function prompt(rl, question) {
  return new Promise(resolve => {
    rl.question(question, answer => {
      resolve(answer.trim());
    });
  });
}

function estimateMonthlyCost(modelKey, frequencyFactor) {
  const model = MODELS[modelKey];
  const tokensPerMonth = model.tokensPerCall * 30 * frequencyFactor;
  const costPerMonth = (model.input / 1000000 * tokensPerMonth * 0.5 +
                        model.output / 1000000 * tokensPerMonth * 0.5);
  return {
    tokens: tokensPerMonth,
    cost: costPerMonth,
  };
}

async function main() {
  console.log('\n🎯 AI 模型智能推荐\n');
  console.log('─'.repeat(60));

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  try {
    // 问题 1：主要用途
    console.log('\n❓ 主要用途？\n');
    Object.entries(SCENARIOS).forEach(([key, scenario]) => {
      console.log(`   ${key}. ${scenario.name}`);
    });

    const scenarioChoice = await prompt(rl, '\n请选择 (1-5): ');

    const scenario = SCENARIOS[scenarioChoice];
    if (!scenario) {
      console.log('❌ 无效选择');
      rl.close();
      return;
    }

    // 问题 2：使用频率
    console.log('\n❓ 每天大约调用次数？\n');
    Object.entries(FREQUENCY).forEach(([key, freq]) => {
      console.log(`   ${key}. ${freq.label}`);
    });

    const freqChoice = await prompt(rl, '\n请选择 (1-4): ');

    const frequency = FREQUENCY[freqChoice];
    if (!frequency) {
      console.log('❌ 无效选择');
      rl.close();
      return;
    }

    rl.close();

    // 推荐模型
    console.log('\n' + '─'.repeat(60));
    console.log(`${GREEN}💡 推荐模型：${MODELS[scenario.recommend].name}${RESET}\n`);
    console.log(`   ${MODELS[scenario.recommend].desc}`);

    const estimate = estimateMonthlyCost(scenario.recommend, frequency.factor);
    console.log(`\n   预估每月费用：¥${estimate.cost.toFixed(2)}`);
    console.log(`   预估每月 tokens：${estimate.tokens.toLocaleString()}`);

    // 对比 GPT-4o
    const gpt4oEstimate = estimateMonthlyCost('daily', frequency.factor);
    const gpt4oCost = gpt4oEstimate.cost * (35 / 0.27); // GPT-4o vs DeepSeek ratio
    const savings = gpt4oCost - estimate.cost;
    const savingsPercent = ((savings / gpt4oCost) * 100).toFixed(1);

    console.log(`\n   ${YELLOW}💰 相比 GPT-4o：节省 ¥${savings.toFixed(2)} (${savingsPercent}%)${RESET}`);

    // 备选方案
    console.log('\n' + '─'.repeat(60));
    console.log('🔄 备选方案：\n');

    scenario.alternatives.forEach((altKey, index) => {
      const altModel = MODELS[altKey];
      const altEstimate = estimateMonthlyCost(altKey, frequency.factor);
      console.log(`   ${index + 1}. ${altModel.name}`);
      console.log(`      ${altModel.desc}`);
      console.log(`      预估每月费用：¥${altEstimate.cost.toFixed(2)}\n`);
    });

    console.log('─'.repeat(60));
    console.log('\n📖 如何配置模型？\n');
    console.log('   方式 1: 使用 openclaw-cn-installer');
    console.log('     npx clawhub@latest install openclaw-cn-installer');
    console.log(`     node ~/.openclaw/skills/openclaw-cn-installer/setup-ai.js ${MODELS[scenario.recommend].provider}`);

    console.log('\n   方式 2: 手动编辑配置文件');
    console.log('     编辑 ~/.openclaw/config.json：');
    console.log('     {');
    console.log(`       "model": {`);
    console.log(`         "provider": "${MODELS[scenario.recommend].provider}",`);
    console.log(`         "model": "${MODELS[scenario.recommend].model}"`);
    console.log(`       }`);
    console.log('     }\n');

  } catch (e) {
    console.error('Error:', e.message);
    rl.close();
  }
}

main();
