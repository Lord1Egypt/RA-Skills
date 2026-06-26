#!/usr/bin/env node

/**
 * Design Analysis Skill - 综合测试套件
 */

const path = require('path');
const { execSync } = require('child_process');

// 测试配置
const TEST_CASES = [
  {
    name: "基础使用 - 自动分析",
    input: "TEST_01.DesignAnalysis",
    output: "TEST_01_OUTPUT.html",
    title: "测试1 - 自动分析"
  },
  {
    name: "自定义标题和尺寸",
    input: "TEST_01.DesignAnalysis",
    output: "TEST_02_OUTPUT.html",
    title: "测试2 - 自定义参数",
    dimensions: { width: 1280, height: 720 }
  }
];

// 创建测试文件夹
function setupTestEnvironment() {
  console.log('🔧 设置测试环境...');

  // 创建测试文件夹（如果不存在）
  const testInput = path.join(__dirname, 'TEST_01.DesignAnalysis');
  if (!require('fs').existsSync(testInput)) {
    console.log(`⚠️  测试文件夹不存在: ${testInput}`);
    console.log(`   请创建该文件夹并放入测试图片，或修改TEST_CASES中的路径`);
    return false;
  }

  console.log('✅ 测试环境就绪');
  return true;
}

// 运行单个测试
async function runTest(testCase, skillPath) {
  console.log(`\n🧪 运行测试: ${testCase.name}`);
  console.log('─'.repeat(50));

  const args = [
    'node',
    skillPath,
    path.resolve(testCase.input),
    path.resolve(testCase.output)
  ];

  if (testCase.title) {
    args.push(testCase.title);
  }

  try {
    const result = execSync(args.join(' '), { encoding: 'utf8' });
    console.log(result);

    // 检查输出文件
    const outputPath = path.resolve(testCase.output);
    const exists = require('fs').existsSync(outputPath);
    const stats = exists ? require('fs').statSync(outputPath) : null;

    console.log(`\n📊 测试结果:`);
    console.log(`   输出文件: ${exists ? '✅' : '❌'} ${testCase.output}`);
    console.log(`   文件大小: ${stats ? stats.size : 0} bytes`);

    return exists;
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
    return false;
  }
}

// 主测试流程
async function main() {
  console.log('╔════════════════════════════════════════╗');
  console.log('║  Design Analysis Skill - 测试套件      ║');
  console.log('╚════════════════════════════════════════╝');

  const skillPath = path.join(__dirname, 'run.js');

  if (!setupTestEnvironment()) {
    process.exit(1);
  }

  let passed = 0;
  let failed = 0;

  for (const testCase of TEST_CASES) {
    const success = await runTest(testCase, skillPath);
    if (success) {
      passed++;
      console.log('✅ 测试通过\n');
    } else {
      failed++;
      console.log('❌ 测试失败\n');
    }
  }

  console.log('═'.repeat(50));
  console.log(`📈 测试总结: ${passed} 通过, ${failed} 失败`);
  console.log('═'.repeat(50));

  process.exit(failed > 0 ? 1 : 0);
}

main().catch(error => {
  console.error('测试套件异常:', error);
  process.exit(1);
});