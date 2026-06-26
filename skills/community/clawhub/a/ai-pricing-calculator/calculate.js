#!/usr/bin/env node
/**
 * AI Cost Optimizer - Calculate Cost
 * 计算特定模型的 API 费用
 */

const MODELS = {
  'deepseek': { name: 'DeepSeek V3', input: 0.27, output: 1.08 },
  'deepseek-coder': { name: 'DeepSeek Coder', input: 0.27, output: 1.08 },
  'glm-4': { name: '智谱 GLM-4', input: 0.10, output: 0.10 },
  'glm-3-turbo': { name: '智谱 GLM-3-Turbo', input: 0.05, output: 0.05 },
  'qwen-plus': { name: '通义千问 Plus', input: 0.30, output: 0.60 },
  'qwen-turbo': { name: '通义千问 Turbo', input: 0.10, output: 0.10 },
  'gpt-4o': { name: 'GPT-4o', input: 35, output: 105 },
  'gpt-4o-mini': { name: 'GPT-4o-mini', input: 3.50, output: 10.50 },
  'claude-3.5-sonnet': { name: 'Claude 3.5 Sonnet', input: 17.50, output: 52.50 },
  'claude-3.5-haiku': { name: 'Claude 3.5 Haiku', input: 0.18, output: 0.54 },
};

const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';

function calculateCost(modelKey, inputTokens, outputTokens) {
  const model = MODELS[modelKey.toLowerCase()];
  if (!model) {
    console.error(`❌ 未知模型: ${modelKey}`);
    console.log('支持的模型:', Object.keys(MODELS).join(', '));
    return null;
  }

  const inputCost = (model.input / 1000000) * inputTokens;
  const outputCost = (model.output / 1000000) * outputTokens;
  const totalCost = inputCost + outputCost;

  return {
    model: model.name,
    inputTokens,
    outputTokens,
    totalTokens: inputTokens + outputTokens,
    inputCost,
    outputCost,
    totalCost,
  };
}

function formatCost(cost) {
  if (cost < 1) return `${(cost * 100).toFixed(2)} 分`;
  return `¥${cost.toFixed(2)}`;
}

// 命令行参数
const args = process.argv.slice(2);

if (args.length >= 2) {
  // node calculate.js <model> <tokens>
  const modelKey = args[0];
  const totalTokens = parseInt(args[1]);

  // 假设输入输出各占一半
  const inputTokens = Math.floor(totalTokens / 2);
  const outputTokens = totalTokens - inputTokens;

  const result = calculateCost(modelKey, inputTokens, outputTokens);

  if (result) {
    console.log(`\n💰 费用计算：${result.model}\n`);
    console.log('─'.repeat(50));
    console.log(`   输入 tokens: ${result.inputTokens.toLocaleString()} → ${formatCost(result.inputCost)}`);
    console.log(`   输出 tokens: ${result.outputTokens.toLocaleString()} → ${formatCost(result.outputCost)}`);
    console.log('─'.repeat(50));
    console.log(`   ${GREEN}总计：${result.totalTokens.toLocaleString()} tokens = ${formatCost(result.totalCost)}${RESET}\n`);

    // 对比 GPT-4o
    if (modelKey !== 'gpt-4o') {
      const gpt4oCost = calculateCost('gpt-4o', inputTokens, outputTokens);
      const savings = gpt4oCost.totalCost - result.totalCost;
      const savingsPercent = ((savings / gpt4oCost.totalCost) * 100).toFixed(1);

      console.log(`   ${YELLOW}💡 相比 GPT-4o：节省 ¥${savings.toFixed(2)} (${savingsPercent}%)${RESET}\n`);
    }
  }
} else {
  // 交互式
  console.log('\n💰 AI 费用计算器\n');
  console.log('支持的模型:', Object.values(MODELS).map(m => m.name).join(', '));
  console.log('使用方法:');
  console.log('  node calculate.js <模型> <总tokens数量>\n');
  console.log('示例:');
  console.log('  node calculate.js deepseek 100000');
  console.log('  node calculate.js gpt-4o 500000\n');
}
