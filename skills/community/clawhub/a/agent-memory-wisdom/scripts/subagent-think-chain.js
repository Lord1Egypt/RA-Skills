#!/usr/bin/env node
/**
 * subagent-think-chain.js
 *
 * 派发 subagent 前的强制思维链检查点
 *
 * 使用方式：node subagent-think-chain.js "<任务描述>"
 *
 * ⚠️ 在派发任何 subagent 之前，必须运行此脚本
 * 输出 JSON 格式的路由决策，按输出结果执行，不允许口头覆盖。
 *
 * 注意：修改 modelRules 中的 model 字段为你实际使用的模型名称
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.HOME + '/.openclaw/workspace';
const LOG_FILE = WORKSPACE + '/memory/watchdog-log.md';

function log(msg) {
  const entry = `[${new Date().toISOString()}] [subagent-think-chain] ${msg}`;
  fs.appendFileSync(LOG_FILE, entry + '\n');
  console.error(entry);
}

const taskInput = process.argv.slice(2).join(' ').trim();

if (!taskInput) {
  console.error('用法: node subagent-think-chain.js "<任务描述>"');
  process.exit(1);
}

log(`分析任务: ${taskInput}`);

// ============================================================
// Step 1: 解析任务类别
// ============================================================
const taskLower = taskInput.toLowerCase();

const categoryPatterns = {
  'search': ['搜索', '调研', '查找', '查', '搜', '研究'],
  'code': ['代码', '写代码', '改bug', '调试', 'debug', 'script', '脚本', '编程'],
  'write': ['写', '文案', '文章', '内容', '生成', '创作', '润色'],
  'image': ['看图', '图片', '截图', '图像', '分析图'],
  'reason': ['分析', '推理', '判断', '评估', '诊断', '排查'],
  'memory': ['记忆', '日志', '记录', '存档', '整理记忆'],
  'browser': ['浏览器', '网页', '网站'],
  'config': ['配置', 'config', '模型', '网关', 'gateway', 'openclaw'],
};

const detectedCategories = [];
for (const [cat, keywords] of Object.entries(categoryPatterns)) {
  if (keywords.some(k => taskLower.includes(k))) {
    detectedCategories.push(cat);
  }
}

if (detectedCategories.length === 0) {
  detectedCategories.push('general');
}

log(`检测到类别: ${detectedCategories.join(', ')}`);

// ============================================================
// Step 2: 拆分决策（保守策略，v1.1.7修复激进拆分）
// ============================================================
const AGGRESSIVE_SPLIT_SIGNALS = [
  { pattern: /对比.*多个|比较.*之间/, reason: '明确对比分析需求' },
  { pattern: /分别调研|逐一|各自/, reason: '明确分离处理需求' },
  { pattern: /和.*同时进行|并行.*任务|多条线/, reason: '明确并行需求' },
];

const NO_SPLIT_SIGNALS = [
  { pattern: /直接|就行|简单|一下|就这样/, reason: '用户要求直接做，不拆分' },
  { pattern: /^读.*文件$|^查看.*$|总结|汇总/, reason: '单一目标，不需要拆分' },
  { pattern: /只|只要|仅/, reason: '目标单一，不需要拆分' },
  { pattern: /单一|全部|统一/, reason: '用户强调统一处理，不拆分' },
];

let shouldSplit = false;
let splitReason = '';
let noSplitReason = '';

// NO_SPLIT 优先级最高（显式禁止拆分）
for (const sig of NO_SPLIT_SIGNALS) {
  if (sig.pattern.test(taskInput)) {
    shouldSplit = false;
    noSplitReason = sig.reason;
    break;
  }
}

// 只有明确的多向需求才拆分（v1.1.7：降低激进度）
if (!noSplitReason) {
  for (const sig of AGGRESSIVE_SPLIT_SIGNALS) {
    if (sig.pattern.test(taskInput)) {
      shouldSplit = true;
      splitReason = sig.reason;
      break;
    }
  }
}

if (taskInput.length > 100 && !shouldSplit && !noSplitReason) {
  shouldSplit = true;
  splitReason = '任务描述较长，可能涉及多个方向';
}

// ============================================================
// Step 3: 置信度评估
// ============================================================
const SIGNAL_TABLE = [
  { pattern: /删除|销毁|rm|remove.*永久/, reason: '不可逆操作', delta: -0.3 },
  { pattern: /发布|上线|deploy/, reason: '对外操作', delta: -0.2 },
  { pattern: /配置.*网关|gateway.*配置|restart.*网关/, reason: '系统核心修改', delta: -0.2 },
  { pattern: /密码|密钥|secret|credential/, reason: '安全相关', delta: -0.2 },
  { pattern: /子任务.*[>2]|多个.*并行/, reason: '子任务>2', delta: -0.1 },
  { pattern: /首次|没做过|不熟悉/, reason: '首次遇到', delta: -0.2 },
  { pattern: /历史成功|做过.*成功|之前.*成功/, reason: '历史成功率高', delta: +0.1 },
  { pattern: /简单|直接|就行|一下/, reason: '任务明确简单', delta: +0.1 },
];

// ⚙️ 配置类任务初始置信度从 0.7 开始（v1.1.7新增）
let confidence = detectedCategories.includes('config') ? 0.7 : 0.9;
let confidenceReason = detectedCategories.includes('config')
  ? '配置类任务，初始置信度0.7（v1.1.7规则）'
  : '无特殊信号，默认置信度0.9';

for (const sig of SIGNAL_TABLE) {
  if (sig.pattern.test(taskInput)) {
    confidence = Math.max(0, Math.min(1, confidence + sig.delta));
    confidenceReason = sig.reason + ' ' + sig.delta;
    break;
  }
}

let needVerification = false;
let verificationReason = '';

const VERIFICATION_REQUIRED = [
  { pattern: /架构|重构|系统设计/, reason: '涉及核心架构' },
  { pattern: /安全|权限/, reason: '安全相关' },
  { pattern: /方案|策略|计划.*实施/, reason: '重要决策' },
];

for (const sig of VERIFICATION_REQUIRED) {
  if (sig.pattern.test(taskInput)) {
    needVerification = true;
    verificationReason = sig.reason;
    break;
  }
}

const LOW_CONFIDENCE = confidence < 0.6;
if (LOW_CONFIDENCE) {
  needVerification = true;
  if (!verificationReason) verificationReason = '置信度低于0.6，需要验证';
}

// ============================================================
// Step 4: 选择模型
// ============================================================

// ⚙️ 修改以下 model 字段为你实际配置的模型名称
const modelRules = [
  {
    categories: ['search'],
    model: '[YOUR_SEARCH_MODEL]',       // 搜索调研类
    reason: '搜索调研类任务'
  },
  {
    categories: ['code'],
    model: '[YOUR_CODE_MODEL]',         // 代码类
    reason: '代码类任务'
  },
  {
    categories: ['write'],
    model: '[YOUR_WRITE_MODEL]',        // 文案类
    reason: '文案写作类任务'
  },
  {
    categories: ['reason'],
    model: '[YOUR_REASON_MODEL]',       // 推理分析类
    reason: '推理分析类任务'
  },
  {
    categories: ['image'],
    model: '[YOUR_IMAGE_MODEL]',        // 看图类
    reason: '图像分析任务'
  },
];

let selectedModel = '[YOUR_DEFAULT_MODEL]'; // ⚙️ 修改为你的默认模型
let modelReason = '默认模型';

for (const rule of modelRules) {
  if (rule.categories.some(c => detectedCategories.includes(c))) {
    selectedModel = rule.model;
    modelReason = rule.reason;
    break;
  }
}

// ============================================================
// Step 5: 输出路由决策
// ============================================================
// v1.1.7: 动态生成 subagent 数量，而非硬编码 2 个
const generateSubagents = (split, task, model) => {
  if (!split) {
    return [{ direction: '单一方向', model, prompt: task }];
  }

  // 保守策略：最多 2 个 subagent，除非任务明确要求更多
  let agentCount = 2;
  if (task.includes('对比') && task.match(/和/g) && (task.match(/和/g).length >= 2)) {
    agentCount = 3; // "A 和 B 和 C"对比才生成 3 个
  }

  const agents = [];
  const directions = ['对象A', '对象B', '对象C', '对象D'];
  for (let i = 0; i < agentCount; i++) {
    agents.push({
      direction: directions[i],
      model,
      prompt: `${task} - 重点：${directions[i]}`,
    });
  }
  return agents;
};

const subagents = generateSubagents(shouldSplit, taskInput, selectedModel);

const decision = {
  task: taskInput,
  timestamp: new Date().toISOString(),
  confidence,
  confidenceReason,
  shouldSplit,
  splitReason: shouldSplit ? splitReason : (noSplitReason || '无拆分必要'),
  subagents,
  needVerification,
  verificationReason,
  selectedModel,
  modelReason,
  warnings: [
    ...(LOW_CONFIDENCE ? ['⚠️ 置信度低于0.6，建议谨慎操作'] : []),
    ...(needVerification ? ['🔍 需要验证agent进行对抗性审查'] : []),
    ...(shouldSplit ? [`🔀 ${subagents.length}向并行，需汇总后统一输出`] : []),
    ...(detectedCategories.includes('config') ? ['⚙️ 配置类任务：执行前必须验证路径存在，执行后必须输出验证结果'] : []),
  ],
  verificationLoop: needVerification ? {
    maxRetries: 3,
    threshold: 'P0问题必须全部解决',
    rule: '验证不通过 → 修复P0 → 再次验证 → 直到通过',
  } : null,
};

console.log(JSON.stringify(decision, null, 2));

log(`路由决策完成: ${shouldSplit ? '需拆分' : '单一'} | 模型: ${selectedModel} | 验证: ${needVerification} | 置信度: ${confidence}`);

console.log('\n===== 任务完成后提醒 =====');
console.log('💡 任务完成后运行胶囊检查：');
console.log('   bash ~/.openclaw/workspace/scripts/capsule-auto-suggest.sh "<结果>" "<原始任务>"');

// v1.1.7: 移除双保险的预检点逻辑（pre-checkpoint.js路径错误导致反复失败）
// 改为：直接在控制台输出关键决策供用户确认，不执行shell调用
if (decision.needVerification || decision.subagents.length > 1) {
  console.log('\n⚠️ 关键决策点：');
  console.log(`  • 置信度: ${confidence.toFixed(2)}`);
  console.log(`  • 需要验证: ${needVerification}`);
  console.log(`  • 派发 ${decision.subagents.length} 个 agent${decision.subagents.length > 1 ? '（多向并行）' : '（单向）'}`);
  console.log('  💡 检查上述决策是否符合预期；如有异议，可调整 SPLIT_SIGNALS 或信心评分规则');
}

// 保存决策到日志
const decisionLogFile = WORKSPACE + '/memory/subagent-routing-log.json';
fs.writeFileSync(decisionLogFile, JSON.stringify(decision, null, 2));
