#!/usr/bin/env node

/**
 * 学习提取器 - 从任务执行结果中提取可复用模式
 * 
 * 功能：
 * 1. 分析任务执行结果
 * 2. 提取成功模式（什么做得好）
 * 3. 提取失败教训（什么需要改进）
 * 4. 生成结构化知识
 * 
 * 用法：
 *   node extractor.js <task-id> [result-json]
 */

const fs = require('fs');
const path = require('path');

// 工作空间根目录
const WORKSPACE = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.jvs/.openclaw/workspace');
const PATTERNS_PATH = path.join(WORKSPACE, 'instincts/patterns.jsonl');
const LESSONS_PATH = path.join(WORKSPACE, 'instincts/lessons.jsonl');
const QUEUE_PATH = path.join(WORKSPACE, 'tasks/queue.json');

/**
 * 加载任务队列
 */
function loadQueue() {
  try {
    const data = fs.readFileSync(QUEUE_PATH, 'utf-8');
    return JSON.parse(data);
  } catch (error) {
    console.error('❌ 无法加载任务队列:', error.message);
    return null;
  }
}

/**
 * 提取模式
 */
function extractPattern(task, result) {
  console.log('\n🧠 开始提取模式...');
  console.log(`   任务：${task.title}`);
  console.log(`   结果：${result.success ? '成功' : '失败'}`);
  
  const pattern = {
    id: `pattern_${Date.now()}`,
    type: result.success ? 'success_pattern' : 'failure_pattern',
    taskId: task.id,
    title: `${task.title} - ${result.success ? '成功模式' : '失败教训'}`,
    description: task.description,
    category: categorizeTask(task),
    steps: extractSteps(task, result),
    keyInsights: extractKeyInsights(task, result),
    prerequisites: task.dependencies || [],
    tags: task.tags || [],
    confidence: 0.5, // 初始自信度
    usedCount: 0,
    successCount: result.success ? 1 : 0,
    failCount: result.success ? 0 : 1,
    lastUsedAt: null,
    createdAt: new Date().toISOString(),
    sourceTask: {
      id: task.id,
      title: task.title,
      phase: task.phase
    }
  };
  
  console.log(`✅ 模式提取完成`);
  console.log(`   ID: ${pattern.id}`);
  console.log(`   类型：${pattern.type}`);
  console.log(`   自信度：${pattern.confidence}`);
  
  return pattern;
}

/**
 * 分类任务
 */
function categorizeTask(task) {
  const categoryMap = {
    'hook': ['hook', 'session', 'automation'],
    'quality': ['quality', 'testing', 'security'],
    'loop': ['loop', 'automation', 'monitoring'],
    'instinct': ['instinct', 'learning', 'evolution'],
    'skill': ['skill', 'tool', 'capability']
  };
  
  const tags = task.tags || [];
  
  for (const [category, keywords] of Object.entries(categoryMap)) {
    if (tags.some(tag => keywords.includes(tag))) {
      return category;
    }
  }
  
  return 'general';
}

/**
 * 提取步骤
 */
function extractSteps(task, result) {
  // 根据任务类型生成通用步骤模板
  const stepTemplates = {
    'hook': [
      '1. 创建 handlers/xxx.js 文件',
      '2. 实现 execute(payload) 函数',
      '3. 在 registry.json 注册',
      '4. 测试执行'
    ],
    'command': [
      '1. 创建 commands/xxx.js 文件',
      '2. 实现命令逻辑',
      '3. 添加帮助信息',
      '4. 测试命令'
    ],
    'skill': [
      '1. 分析技能需求',
      '2. 设计技能结构',
      '3. 实现 SKILL.md',
      '4. 测试技能'
    ]
  };
  
  const category = categorizeTask(task);
  return stepTemplates[category] || [
    '1. 分析任务需求',
    '2. 设计实现方案',
    '3. 执行实现',
    '4. 测试验证'
  ];
}

/**
 * 提取关键洞察
 */
function extractKeyInsights(task, result) {
  const insights = [];
  
  if (result.success) {
    insights.push('✅ 任务成功完成');
    insights.push('💡 关键成功因素：按步骤执行、依赖检查');
  } else {
    insights.push('❌ 任务执行失败');
    if (result.message) {
      insights.push(`⚠️  失败原因：${result.message}`);
    }
    insights.push('💡 改进建议：检查依赖、增加错误处理');
  }
  
  return insights;
}

/**
 * 保存模式
 */
function savePattern(pattern) {
  const line = JSON.stringify(pattern) + '\n';
  fs.appendFileSync(PATTERNS_PATH, line);
  console.log(`📝 模式已保存到：${PATTERNS_PATH}`);
}

/**
 * 提取教训（失败时使用）
 */
function extractLesson(task, result) {
  const lesson = {
    id: `lesson_${Date.now()}`,
    taskId: task.id,
    title: `${task.title} - 失败教训`,
    description: result.message || '任务执行失败',
    rootCause: '待分析',
    solution: '待制定',
    preventions: [
      '检查依赖是否满足',
      '增加错误处理',
      '添加超时保护'
    ],
    severity: 'medium',
    createdAt: new Date().toISOString()
  };
  
  const line = JSON.stringify(lesson) + '\n';
  fs.appendFileSync(LESSONS_PATH, line);
  console.log(`📝 教训已保存到：${LESSONS_PATH}`);
  
  return lesson;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  const taskId = args[0];
  const resultJson = args[1];
  
  if (!taskId) {
    console.log('用法：node extractor.js <task-id> [result-json]');
    console.log('\n示例:');
    console.log('  node extractor.js task_001 \'{"success":true,"message":"完成"}\'');
    process.exit(0);
  }
  
  const queue = loadQueue();
  if (!queue) {
    process.exit(1);
  }
  
  const task = queue.tasks.find(t => t.id === taskId);
  if (!task) {
    console.error(`❌ 任务不存在：${taskId}`);
    process.exit(1);
  }
  
  const result = resultJson ? JSON.parse(resultJson) : { success: true, message: '完成' };
  
  // 提取模式或教训
  if (result.success) {
    const pattern = extractPattern(task, result);
    savePattern(pattern);
  } else {
    extractLesson(task, result);
    const pattern = extractPattern(task, result);
    savePattern(pattern);
  }
  
  console.log('\n✅ 学习提取完成');
}

// 运行主函数
main().catch(error => {
  console.error('❌ 学习提取器错误:', error.message);
  console.error(error.stack);
  process.exit(1);
});
