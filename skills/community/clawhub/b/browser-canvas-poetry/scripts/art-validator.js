#!/usr/bin/env node

/**
 * Browser Canvas Poetry - Art Form Validator
 * 艺术形式验证器 - 检测前端作品是否符合"艺术"标准
 *
 * 使用方法:
 *   node scripts/art-validator.js "项目描述" [--detailed]
 *   node scripts/art-validator.js --interactive
 */

const readline = require('readline');

// 艺术形式评估维度
const VALIDATION_CRITERIA = {
  originality: {
    name: '原创性 (Originality)',
    weight: 25,
    description: '概念是否独特？是否有个人视角？是否避免了模板化复制？',
    indicators: [
      '概念新颖度',
      '个人视角体现',
      '对既有模式的突破',
      '创意转化深度'
    ]
  },
  intentionality: {
    name: '意图明确性 (Intentionality)',
    weight: 25,
    description: '是否有清晰的艺术概念？技术选择是否服务于概念？',
    indicators: [
      '概念清晰度',
      '主题深度',
      '技术服务于概念',
      '陈述完整性'
    ]
  },
  sensoryExperience: {
    name: '感官体验 (Sensory Experience)',
    weight: 25,
    description: '视觉是否令人驻足？交互是否有意外之喜？',
    indicators: [
      '视觉冲击力',
      '动态美感',
      '交互惊喜度',
      '情绪唤起力'
    ]
  },
  formalCompleteness: {
    name: '形式完整性 (Formal Completeness)',
    weight: 25,
    description: '作品是否自洽完整？各元素是否协调统一？',
    indicators: [
      '结构完整性',
      '元素协调性',
      '细节打磨度',
      '反复观看的耐看性'
    ]
  }
};

// 问题库
const QUESTIONS = {
  originality: [
    {
      question: '这个作品想要表达的核心概念是什么？',
      key: 'concept',
      type: 'text'
    },
    {
      question: '这个概念与市面上常见的"酷炫动画"有何不同？',
      key: 'differentiation',
      type: 'text'
    },
    {
      question: '创作者(你)对这件事有什么独特的视角或情感连接？',
      key: 'personalPerspective',
      type: 'text'
    },
    {
      question: '这个作品是否受到某件已存在的艺术作品的启发？如果是，是什么？',
      key: 'influence',
      type: 'choice',
      options: ['否，无具体参考', '某件视觉艺术作品', '某段音乐或声音', '某首诗或文学片段', '某部电影或视频', '某个技术demo']
    }
  ],
  intentionality: [
    {
      question: '请用一句话描述这个作品想表达的内容：',
      key: 'oneLiner',
      type: 'text'
    },
    {
      question: '为什么选择这种视觉风格来表达这个概念？',
      key: 'styleChoice',
      type: 'text'
    },
    {
      question: '如果只能保留一个元素，你会保留哪个？为什么？',
      key: 'essentialElement',
      type: 'text'
    },
    {
      question: '你希望观众在看到这个作品时，第一感受是什么？',
      key: 'audienceEmotion',
      type: 'text'
    }
  ],
  sensoryExperience: [
    {
      question: '这个作品在视觉上有什么最吸引人的地方？',
      key: 'visualAppeal',
      type: 'text'
    },
    {
      question: '观众可以如何与这个作品互动？',
      key: 'interaction',
      type: 'text'
    },
    {
      question: '这种互动设计会带来什么意外之喜？',
      key: 'unexpectedJoy',
      type: 'text'
    },
    {
      question: '观看超过30秒后，作品是否还有新的发现？',
      key: 'depthExploration',
      type: 'choice',
      options: ['完全没有', '有一些细节', '有很多层次', '每次都有新发现']
    }
  ],
  formalCompleteness: [
    {
      question: '你觉得这个作品在技术实现上是否完整？',
      key: 'technicalCompletion',
      type: 'choice',
      options: ['有很多bug和妥协', '基本可用但有遗憾', '完成了核心功能', '完全按计划实现']
    },
    {
      question: '如果要给这个作品打分(1-10)，你会打几分？',
      key: 'selfScore',
      type: 'number'
    },
    {
      question: '你最满意的部分是什么？',
      key: 'bestPart',
      type: 'text'
    },
    {
      question: '你最想改进的部分是什么？',
      key: 'improvementArea',
      type: 'text'
    }
  ]
};

// 评分标准
const SCORING_GUIDELINES = {
  high: '85-100',
  good: '70-84',
  moderate: '50-69',
  low: '0-49'
};

class ArtValidator {
  constructor() {
    this.answers = {};
    this.scores = {};
  }

  // 创建交互式命令行界面
  createInterface(question) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });

    return new Promise((resolve) => {
      if (question.type === 'choice') {
        console.log(`\n📌 ${question.question}`);
        question.options.forEach((opt, idx) => {
          console.log(`   ${idx + 1}. ${opt}`);
        });
        rl.question('\n请选择 (输入数字): ', (answer) => {
          const idx = parseInt(answer) - 1;
          resolve(question.options[idx] || answer);
          rl.close();
        });
      } else if (question.type === 'number') {
        rl.question(`\n📌 ${question.question} (1-10): `, (answer) => {
          resolve(parseInt(answer) || 5);
          rl.close();
        });
      } else {
        rl.question(`\n📌 ${question.question}\n> `, (answer) => {
          resolve(answer);
          rl.close();
        });
      }
    });
  }

  // 运行交互式验证
  async runInteractive() {
    console.log('\n🎨 Browser Canvas Poetry - 艺术形式验证器');
    console.log('═'.repeat(50));
    console.log('请诚实地回答以下问题，帮助我们评估你的作品。\n');

    for (const [category, questions] of Object.entries(QUESTIONS)) {
      console.log(`\n${'═'.repeat(50)}`);
      console.log(`📂 ${VALIDATION_CRITERIA[category].name}`);
      console.log(`   ${VALIDATION_CRITERIA[category].description}\n`);

      let categoryTotal = 0;
      let categoryCount = 0;

      for (const question of questions) {
        const answer = await this.createInterface(question);
        this.answers[`${category}_${question.key}`] = answer;

        // 自动评分
        if (question.type === 'choice') {
          const score = this.calculateChoiceScore(question.key, answer, category);
          categoryTotal += score;
          categoryCount++;
        } else if (question.type === 'number') {
          categoryTotal += answer * 2.5; // 转换为25分制
          categoryCount++;
        }
      }

      this.scores[category] = Math.round(categoryTotal / categoryCount);
    }

    this.generateReport();
  }

  // 计算选择题分数
  calculateChoiceScore(key, answer, category) {
    // 根据具体问题调整评分逻辑
    if (key === 'depthExploration') {
      const options = ['完全没有', '有一些细节', '有很多层次', '每次都有新发现'];
      return (options.indexOf(answer) + 1) * 6.25;
    }
    if (key === 'technicalCompletion') {
      const options = ['有很多bug和妥协', '基本可用但有遗憾', '完成了核心功能', '完全按计划实现'];
      return (options.indexOf(answer) + 1) * 6.25;
    }
    if (key === 'influence') {
      if (answer.includes('否')) return 25;
      return 20; // 有参考但经过转化
    }
    return 15; // 默认中等分数
  }

  // 生成验证报告
  generateReport() {
    console.log('\n');
    console.log('═'.repeat(50));
    console.log('📊 艺术形式验证报告');
    console.log('═'.repeat(50));

    let totalScore = 0;

    for (const [category, score] of Object.entries(this.scores)) {
      const criteria = VALIDATION_CRITERIA[category];
      const percentage = (score / criteria.weight * 100).toFixed(0);

      let emoji = '⚪';
      if (percentage >= 85) emoji = '🟢';
      else if (percentage >= 70) emoji = '🟡';
      else if (percentage >= 50) emoji = '🟠';
      else emoji = '🔴';

      console.log(`\n${emoji} ${criteria.name}`);
      console.log(`   得分: ${score}/${criteria.weight} (${percentage}%)`);
      console.log(`   ${criteria.description}`);

      totalScore += score;
    }

    const finalScore = totalScore;
    const maxScore = 100;
    const percentage = (finalScore / maxScore * 100).toFixed(0);

    console.log('\n' + '═'.repeat(50));
    console.log(`\n🎯 总分: ${finalScore}/${maxScore}`);

    let verdict = '';
    let verdictEmoji = '';

    if (finalScore >= 80) {
      verdict = '优秀的浏览器原生艺术作品';
      verdictEmoji = '🌟';
    } else if (finalScore >= 60) {
      verdict = '具有良好的艺术潜质，建议进一步深化';
      verdictEmoji = '✨';
    } else if (finalScore >= 40) {
      verdict = '偏向功能性/工具性设计，艺术表达需加强';
      verdictEmoji = '💡';
    } else {
      verdict = '可能更偏向技术演示或概念验证';
      verdictEmoji = '🔧';
    }

    console.log(`\n${verdictEmoji} 鉴定结果: ${verdict}`);
    console.log('═'.repeat(50));

    // 生成改进建议
    this.generateSuggestions();
  }

  // 生成改进建议
  generateSuggestions() {
    console.log('\n📝 改进建议\n');

    const suggestions = {
      originality: {
        low: '尝试为你的作品添加一个独特的个人视角或情感连接',
        medium: '考虑如何在现有概念上做出更有辨识度的表达',
        high: '保持你的原创精神，但可以思考如何让概念更普世共鸣'
      },
      intentionality: {
        low: '明确你的创作意图，思考"为什么"比"怎么做"更重要',
        medium: '审视你的技术选择是否真正服务于概念表达',
        high: '你的意图很清晰，可以尝试更多的隐喻和层次'
      },
      sensoryExperience: {
        low: '增加视觉冲击力或交互的意外之喜',
        medium: '考虑增加观看的深度，让作品值得反复探索',
        high: '感官体验很好，可以考虑加入更多感官维度'
      },
      formalCompleteness: {
        low: '完善技术实现，打磨细节',
        medium: '考虑如何让各元素更加协调统一',
        high: '形式已经很完整，可以更大胆地实验'
      }
    };

    for (const [category, score] of Object.entries(this.scores)) {
      const criteria = VALIDATION_CRITERIA[category];
      const percentage = (score / criteria.weight * 100);

      let level = 'low';
      if (percentage >= 85) level = 'high';
      else if (percentage >= 70) level = 'medium';

      if (level !== 'high') {
        console.log(`💭 ${criteria.name}: ${suggestions[category][level]}`);
      }
    }

    console.log('\n');
  }

  // 快速验证（基于描述文本）
  quickValidate(description) {
    console.log('\n🔍 快速艺术形式评估\n');
    console.log('输入描述:', description);
    console.log('');

    const keywords = {
      art: ['表达', '情感', '诗意', '意境', '灵魂', '记忆', '孤独', '时间', '永恒'],
      tech: ['动画', '交互', '粒子', '效果', '响应', '流畅', '炫酷', '动态'],
      weak: ['按钮', '表单', '登录', '注册', '购物', '列表', '表格', '菜单']
    };

    let artScore = 0;
    let techScore = 0;
    let weakScore = 0;

    for (const word of keywords.art) {
      if (description.includes(word)) artScore++;
    }
    for (const word of keywords.tech) {
      if (description.includes(word)) techScore++;
    }
    for (const word of keywords.weak) {
      if (description.includes(word)) weakScore++;
    }

    if (weakScore > 0) {
      console.log('⚠️ 检测到功能性关键词，可能更偏向工具性设计');
      console.log('   功能性元素: ' + keywords.weak.filter(w => description.includes(w)).join(', '));
    }

    if (artScore >= 3) {
      console.log('✅ 包含丰富的艺术性关键词');
      console.log('   艺术元素: ' + keywords.art.filter(w => description.includes(w)).join(', '));
    }

    if (techScore >= 2) {
      console.log('ℹ️ 包含技术实现描述');
    }

    const estimatedScore = Math.min(100, artScore * 20 + techScore * 10 + weakScore * -15 + 40);

    console.log(`\n📊 预估艺术性得分: ${estimatedScore}/100`);

    if (estimatedScore >= 70) {
      console.log('🎨 初步判断: 具有艺术作品潜质，建议进行完整验证');
    } else if (estimatedScore >= 50) {
      console.log('💡 初步判断: 有一定艺术性，可考虑深化概念');
    } else {
      console.log('🔧 初步判断: 可能更偏向功能性项目');
    }

    console.log('\n运行完整验证: node scripts/art-validator.js --interactive');
  }
}

// 主程序
function main() {
  const args = process.argv.slice(2);
  const validator = new ArtValidator();

  if (args.includes('--interactive') || args.includes('-i')) {
    validator.runInteractive();
  } else if (args.length > 0) {
    const description = args.filter(a => !a.startsWith('--')).join(' ');
    validator.quickValidate(description);
  } else {
    console.log(`
🎨 Browser Canvas Poetry - 艺术形式验证器

使用方法:
  node scripts/art-validator.js "项目描述"    # 快速评估
  node scripts/art-validator.js --interactive  # 完整交互式验证
  node scripts/art-validator.js --help         # 显示帮助
    `);
  }
}

main();
