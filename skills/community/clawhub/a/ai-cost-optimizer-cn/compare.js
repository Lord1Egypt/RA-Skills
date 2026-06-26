#!/usr/bin/env node
/**
 * AI Cost Optimizer - Compare Prices
 * 对比不同 AI 模型的 API 价格
 */

const MODELS = [
  // 2026-03-24 更新：智谱 GLM-5 系列新定价
  { name: 'GLM-4.7-Flash', input: 0, output: 0, tags: ['免费'], best: '完全免费！' },
  { name: 'GLM-4-FlashX', input: 0.1, output: 0.05, tags: ['超便宜'], best: '最低成本' },
  { name: 'GLM-4-Air', input: 0.5, output: 0.25, tags: ['均衡'], best: '性价比' },
  { name: 'GLM-5-Turbo', input: 12, output: 18, tags: ['最新'], best: '限时免费' },
  // DeepSeek 系列
  { name: 'DeepSeek V3', input: 0.27, output: 1.08, tags: ['日常', '编程', '写作'], best: '性价比最高' },
  { name: 'DeepSeek Coder', input: 0.27, output: 1.08, tags: ['代码生成'], best: '代码能力强' },
  // 智谱 GLM-4 系列
  { name: '智谱 GLM-4', input: 0.10, output: 0.10, tags: ['中文'], best: '中文能力强' },
  { name: '智谱 GLM-3-Turbo', input: 0.05, output: 0.05, tags: ['高频'], best: '超便宜' },
  // 阿里通义
  { name: '通义千问 Plus', input: 0.30, output: 0.60, tags: ['多模态'], best: '图文处理' },
  { name: '通义千问 Turbo', input: 0.10, output: 0.10, tags: ['快速'], best: '快速响应' },
  // OpenAI
  { name: 'GPT-4o', input: 35, output: 105, tags: ['复杂推理'], best: '企业级' },
  { name: 'GPT-4o-mini', input: 3.50, output: 10.50, tags: ['中等任务'], best: '均衡' },
  // Anthropic
  { name: 'Claude 3.5 Sonnet', input: 17.50, output: 52.50, tags: ['长文本', '代码'], best: '推理强' },
  { name: 'Claude 3.5 Haiku', input: 0.18, output: 0.54, tags: ['快速'], best: '便宜又快' },
];

const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const CYAN = '\x1b[36m';
const RESET = '\x1b[0m';

function calculateCost100k(model) {
  // 假设输入输出各占一半，即 50k 输入 + 50k 输出
  const inputCost = (model.input / 1000000) * 50000;
  const outputCost = (model.output / 1000000) * 50000;
  return inputCost + outputCost;
}

console.log('\n📊 AI 模型价格对比\n');
console.log('─'.repeat(70));

// 表头
console.log(`│ ${'模型'.padEnd(12)} │ ${'输入'.padEnd(10)} │ ${'输出'.padEnd(10)} │ ${'10万tokens'.padEnd(12)} │`);

console.log('─'.repeat(70));

// 排序：按价格从低到高
const sortedModels = [...MODELS].sort((a, b) => calculateCost100k(a) - calculateCost100k(b));

sortedModels.forEach((model, index) => {
  const cost100k = calculateCost100k(model);
  const costStr = `¥${cost100k.toFixed(2)}`;
  const icon = index === 0 ? GREEN + '🏆' + RESET : '  ';
  console.log(`${icon} │ ${model.name.padEnd(12)} │ ¥${model.input.toFixed(2)}/M  │ ¥${model.output.toFixed(2)}/M  │ ${costStr.padEnd(12)} │`);
});

console.log('─'.repeat(70));

// 推荐建议
console.log('\n💡 推荐选择：\n');

const recommendations = [
  {
    title: '日常使用',
    model: 'DeepSeek V3',
    desc: '性价比最高',
    savings: '省 99% 费用',
    price: calculateCost100k(MODELS.find(m => m.name === 'DeepSeek V3')),
  },
  {
    title: '中文内容',
    model: '智谱 GLM-4',
    desc: '中文能力强',
    savings: '省 99.5% 费用',
    price: calculateCost100k(MODELS.find(m => m.name === '智谱 GLM-4')),
  },
  {
    title: '复杂推理',
    model: 'Claude 3.5 Sonnet',
    desc: '推理能力强',
    savings: '省 50% 费用（对比 GPT-4o）',
    price: calculateCost100k(MODELS.find(m => m.name === 'Claude 3.5 Sonnet')),
  },
  {
    title: '代码生成',
    model: 'DeepSeek Coder',
    desc: '代码专项优化',
    savings: '省 99% 费用',
    price: calculateCost100k(MODELS.find(m => m.name === 'DeepSeek Coder')),
  },
];

recommendations.forEach(rec => {
  console.log(`   ${YELLOW}→${RESET} ${rec.title.padEnd(8)} → ${CYAN}${rec.model}${RESET}`);
  console.log(`      ${rec.desc}, ${rec.savings}`);
  console.log(`      每10万 tokens：¥${rec.price.toFixed(2)}\n`);
});

// 对比 GPT-4o
const gpt4o = MODELS.find(m => m.name === 'GPT-4o');
const deepseek = MODELS.find(m => m.name === 'DeepSeek V3');
const ratio = calculateCost100k(gpt4o) / calculateCost100k(deepseek);

console.log('─'.repeat(70));
console.log(`\n${GREEN}📈 省钱潜力：${RESET}`);
console.log(`   DeepSeek V3 vs GPT-4o：便宜 ${ratio.toFixed(0)} 倍`);
console.log(`   同样使用 100 万 tokens：`);
console.log(`   - GPT-4o: ¥${(calculateCost100k(gpt4o) * 10).toFixed(2)}`);
console.log(`   - DeepSeek: ¥${(calculateCost100k(deepseek) * 10).toFixed(2)}`);
console.log(`   ${GREEN}节省：¥${(calculateCost100k(gpt4o) * 10 - calculateCost100k(deepseek) * 10).toFixed(2)} (${((1 - 1/ratio) * 100).toFixed(0)}%)${RESET}\n`);

console.log('📖 更多功能：');
console.log('   node calculate.js - 计算使用费用');
console.log('   node recommend.js - 智能推荐模型\n');
