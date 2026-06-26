/**
 * Agent-SBTI: SBTI 测试答题系统
 * 
 * 使用方法:
 * node test.js                    # 交互式测试
 * node test.js --answer 1,2,3... # 批量答题
 */

const fs = require('fs');
const path = require('path');

// 加载题目数据
const DATA_DIR = path.join(__dirname, '..', 'data');
const questions = require(path.join(DATA_DIR, 'questions.json'));
const results = require(path.join(DATA_DIR, 'results.json'));
const dimensions = require(path.join(DATA_DIR, 'dimensions.json'));

// 维度分数累加器
let dimensionScores = {};

// 初始化维度分数
function initDimensions() {
  dimensionScores = {};
  dimensions.forEach(dim => {
    dimensionScores[dim.n] = 0;
  });
}

// 计算维度分数
function calcDimensionScore(answers) {
  initDimensions();
  
  answers.forEach((answerIdx, qIndex) => {
    const question = questions[qIndex];
    if (!question || !question.o || !question.o[answerIdx]) return;
    
    const scores = question.o[answerIdx].s;
    Object.entries(scores).forEach(([dimName, score]) => {
      if (dimensionScores[dimName] !== undefined) {
        dimensionScores[dimName] += score;
      }
    });
  });
  
  return dimensionScores;
}

// 识别人格类型
function detectPersonality(dimensionScores) {
  // 获取最高分和最低分的维度
  const entries = Object.entries(dimensionScores);
  
  // 简单算法：根据总分和极端维度判断
  const total = entries.reduce((sum, [, v]) => sum + v, 0);
  const avg = total / entries.length;
  
  // 检查极端维度
  const extremes = entries.filter(([, v]) => v <= 2 || v >= 4);
  
  // 判断逻辑
  if (dimensionScores['工具人倾向'] >= 4 && dimensionScores['打工人觉悟'] <= 2) {
    return 'ATM';
  }
  if (dimensionScores['摆烂力'] >= 4 && dimensionScores['打工人觉悟'] >= 4) {
    return 'MALO';
  }
  if (dimensionScores['情绪稳定性（反向）'] >= 4 && dimensionScores['内心戏浓度'] >= 3) {
    return 'FUCK';
  }
  if (dimensionScores['社恐指数'] >= 4 && dimensionScores['工具人倾向'] <= 2) {
    return 'DEAD';
  }
  if (dimensionScores['嘴硬程度'] >= 4 && dimensionScores['玻璃心厚度'] <= 2) {
    return 'SHIT';
  }
  
  // 默认：根据总分最低维度
  const sorted = entries.sort((a, b) => a[1] - b[1]);
  const lowest = sorted[0][0];
  
  if (lowest.includes('工具') || lowest.includes('打工人')) return 'ATM';
  if (lowest.includes('社恐')) return 'DEAD';
  if (lowest.includes('情绪')) return 'FUCK';
  if (lowest.includes('摆烂')) return 'MALO';
  
  return 'SHIT';
}

// 获取人格描述
function getPersonalityDesc(personality) {
  return results[personality] || results['DEAD'];
}

// 交互式测试
async function interactiveTest() {
  const readline = require('readline');
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });
  
  const question = (txt) => new Promise(resolve => rl.question(txt, resolve));
  
  console.log('\n🎭 Agent-SBTI 人格测试\n');
  console.log('='.repeat(40));
  console.log('共 20 道题，每题 4 个选项\n');
  
  const answers = [];
  
  for (let i = 0; i < questions.length; i++) {
    const q = questions[i];
    console.log(`\n第 ${i + 1}/20 题:`);
    console.log(q.q);
    console.log('');
    
    q.o.forEach((opt, idx) => {
      console.log(`  ${idx + 1}. ${opt.t}`);
    });
    
    let answer;
    while (true) {
      answer = await question('\n请输入选项 (1-4): ');
      const num = parseInt(answer);
      if (num >= 1 && num <= 4) {
        answers.push(num - 1);
        break;
      }
      console.log('请输入 1-4 之间的数字');
    }
  }
  
  rl.close();
  
  // 计算结果
  const dimScores = calcDimensionScore(answers);
  const personality = detectPersonality(dimScores);
  const desc = getPersonalityDesc(personality);
  
  // 输出结果
  console.log('\n' + '='.repeat(40));
  console.log('\n🎉 测试完成！\n');
  console.log(`你的 SBTI 人格类型: ${desc.n} (${personality})`);
  console.log(`\n"${desc.slogan}"`);
  console.log('\n详细描述:');
  desc.desc.forEach((d, i) => {
    console.log(`  ${i + 1}. ${d}`);
  });
  
  console.log('\n📊 维度得分:');
  Object.entries(dimScores)
    .sort((a, b) => b[1] - a[1])
    .forEach(([dim, score]) => {
      console.log(`  ${dim}: ${score}`);
    });
  
  return {
    answers,
    dimensions: dimScores,
    personality,
    description: desc
  };
}

// 批量答题模式
function batchTest(answerStr) {
  const answers = answerStr.split(',').map(n => parseInt(n.trim()) - 1);
  
  if (answers.length !== 20) {
    console.error('需要 20 个答案');
    process.exit(1);
  }
  
  const dimScores = calcDimensionScore(answers);
  const personality = detectPersonality(dimScores);
  const desc = getPersonalityDesc(personality);
  
  console.log('\n🎭 测试结果:');
  console.log(`人格类型: ${desc.n} (${personality})`);
  console.log(`Slogan: "${desc.slogan}"`);
  console.log('\n维度得分:');
  Object.entries(dimScores)
    .sort((a, b) => b[1] - a[1])
    .forEach(([dim, score]) => {
      console.log(`  ${dim}: ${score}`);
    });
  
  return { answers, dimensions: dimScores, personality, description: desc };
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args[0] === '--answer' && args[1]) {
    batchTest(args[1]);
  } else {
    interactiveTest().catch(console.error);
  }
}

module.exports = {
  calcDimensionScore,
  detectPersonality,
  getPersonalityDesc,
  questions,
  dimensions,
  results
};
