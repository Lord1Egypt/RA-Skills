/**
 * run_all.js - 一键执行完整流程
 * 
 * 使用方式：
 * node scripts/run_all.js --topic "Claude Code" --slides 10 --output "report.pptx"
 * 
 * 可选参数：
 * --session-id    会话 ID（不提供则自动生成）
 * --from-step     从指定步骤开始 (1-5)
 * --only-step     只执行指定步骤
 */
const path = require('path');
const fs = require('fs');

// 加载配置
process.chdir(path.resolve(__dirname, '..'));
const config = require('../lib/config');
const loggerModule = require('../lib/logger');
const fileUtils = require('../lib/file_utils');

// ============================================================
// 命令行参数
// ============================================================
const args = process.argv.slice(2);
const params = {};
for (let i = 0; i < args.length; i++) {
  if (args[i].startsWith('--')) {
    const key = args[i].substring(2);
    params[key] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
  }
}

const TOPIC = params.topic || 'AI 技术趋势';
const SESSION_ID = params['session-id'] || Date.now().toString();
const SLIDES = parseInt(params.slides) || 10;
const OUTPUT = params.output || `${TOPIC.replace(/\s+/g, '_')}_report.pptx`;
const FROM_STEP = parseInt(params['from-step']) || 1;
const ONLY_STEP = parseInt(params['only-step']) || null;

// ============================================================
// 初始化
// ============================================================
fileUtils.ensureDir(config.REPORTS_ROOT);
const dirs = fileUtils.createSessionDirs(SESSION_ID);
const log = new loggerModule.Logger(SESSION_ID);

console.log('\n' + '='.repeat(60));
console.log('🚀 PPT Insight Generator - 完整流程');
console.log('='.repeat(60));
console.log(`📌 主题: ${TOPIC}`);
console.log(`📌 目标: ${SLIDES} 页`);
console.log(`📌 会话: ${SESSION_ID}`);
console.log(`📌 目录: ${dirs.base}`);
console.log('='.repeat(60) + '\n');

// ============================================================
// 流程定义
// ============================================================
const steps = [
  {
    id: 1,
    name: '内容搜索',
    description: '围绕主题搜索大量相关内容，构建知识基础',
    script: './01_search_and_collect.js',
    options: { topic: TOPIC }
  },
  {
    id: 2,
    name: '洞察提炼',
    description: '从收集的内容中提炼关键观点',
    script: './02_extract_insights.js',
    options: {}
  },
  {
    id: 3,
    name: '目录+内容生成',
    description: '基于洞察生成 PPT 结构并撰写每页详细内容',
    script: './03_generate_content.js',
    options: { slides: SLIDES }
  },
  {
    id: 4,
    name: '反思优化',
    description: '检查内容质量并优化空洞表述',
    script: './04_optimize_content.js',
    options: {}
  },
  {
    id: 5,
    name: 'PPT生成',
    description: '将内容转换为 PPT 文件',
    script: './05_generate_ppt.js',
    options: { output: OUTPUT }
  }
];

// ============================================================
// 执行流程
// ============================================================
async function runPipeline() {
  const startTime = Date.now();
  const results = [];

  // 确定要执行的步骤
  let stepsToRun = steps;
  if (ONLY_STEP) {
    stepsToRun = steps.filter(s => s.id === ONLY_STEP);
  } else if (FROM_STEP > 1) {
    stepsToRun = steps.filter(s => s.id >= FROM_STEP);
  }

  for (const step of stepsToRun) {
    console.log(`\n${'─'.repeat(60)}`);
    console.log(`▶ 步骤 ${step.id}/5: ${step.name}`);
    console.log(`  ${step.description}`);
    console.log(`${'─'.repeat(60)}`);

    try {
      const stepStart = Date.now();
      
      // 根据步骤选择合适的加载方式
      let stepModule;
      switch (step.id) {
        case 1:
          stepModule = require('./01_search_and_collect.js');
          const result1 = await stepModule.run(TOPIC, step.options);
          results.push({ step: step.id, status: 'success', result: result1 });
          break;
        case 2:
          stepModule = require('./02_extract_insights.js');
          const result2 = await stepModule.run(SESSION_ID);
          results.push({ step: step.id, status: 'success', result: result2 });
          break;
        case 3:
          stepModule = require('./03_generate_content.js');
          const result3 = await stepModule.run(SESSION_ID, SLIDES);
          results.push({ step: step.id, status: 'success', result: result3 });
          break;
        case 4:
          stepModule = require('./04_optimize_content.js');
          const result4 = await stepModule.run(SESSION_ID);
          results.push({ step: step.id, status: 'success', result: result4 });
          break;
        case 5:
          stepModule = require('./05_generate_ppt.js');
          const result5 = await stepModule.run(SESSION_ID, OUTPUT);
          results.push({ step: step.id, status: 'success', result: result5 });
          break;
      }

      const stepDuration = ((Date.now() - stepStart) / 1000).toFixed(1);
      console.log(`\n✅ 步骤 ${step.id} 完成 (${stepDuration}s)`);

    } catch (error) {
      console.error(`\n❌ 步骤 ${step.id} 失败: ${error.message}`);
      results.push({ step: step.id, status: 'failed', error: error.message });
      
      // 询问是否继续
      if (step.id < 5) {
        console.log('\n是否继续执行后续步骤? (y/n)');
        // 在非交互模式下，直接停止
        console.log('非交互模式，停止执行');
        break;
      }
    }
  }

  // 输出总结
  const totalDuration = ((Date.now() - startTime) / 1000).toFixed(1);
  console.log('\n' + '='.repeat(60));
  console.log('📊 执行总结');
  console.log('='.repeat(60));
  
  for (const r of results) {
    const icon = r.status === 'success' ? '✅' : '❌';
    console.log(`${icon} 步骤 ${r.step}: ${r.status}`);
  }
  
  console.log(`\n⏱️  总耗时: ${totalDuration}s`);
  console.log(`📁 会话目录: ${dirs.base}`);
  
  // 如果最后一步成功，输出文件位置
  const lastSuccess = [...results].reverse().find(r => r.status === 'success');
  if (lastSuccess?.result?.filePath) {
    console.log(`\n🎉 PPT 已生成: ${lastSuccess.result.filePath}`);
  }
  
  console.log('='.repeat(60));

  // 保存执行报告
  const report = {
    sessionId: SESSION_ID,
    topic: TOPIC,
    targetSlides: SLIDES,
    startTime: new Date(startTime).toISOString(),
    endTime: new Date().toISOString(),
    totalDuration: parseFloat(totalDuration),
    steps: results,
    finalOutput: lastSuccess?.result?.filePath
  };
  fileUtils.writeJson(path.join(dirs.base, 'execution_report.json'), report);

  return results;
}

// ============================================================
// 直接执行
// ============================================================
runPipeline().catch(err => {
  console.error('执行失败:', err);
  process.exit(1);
});
