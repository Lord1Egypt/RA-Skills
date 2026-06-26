#!/usr/bin/env node

/**
 * Freelance-Proposal-Writer
 * AI-powered proposal generator for Freelancer/Upwork
 * 
 * Features:
 * - AI-generated投标 proposals
 * - Client analysis & matching
 * - Success rate optimization
 * - Template library
 */

const { Command } = require('commander');
const chalk = require('chalk');
const ora = require('ora');
const inquirer = require('inquirer');
const fs = require('fs');
const path = require('path');

const program = new Command();

// Proposal templates library
const TEMPLATES = {
  standard: {
    name: '标准投标提案',
    description: '适用于大多数项目的标准提案',
    structure: [
      '个性化开场白',
      '展示相关经验',
      '提出解决方案',
      '明确交付时间',
      '呼吁行动'
    ],
    template: `Hi {{clientName}},

I've carefully reviewed your project "{{projectTitle}}" and I'm excited about the opportunity to help.

With {{years}}+ years of experience in {{skills}}, I've successfully delivered {{similarProjects}} similar projects. Here's how I can help you:

• {{solution1}}
• {{solution2}}
• {{solution3}}

I can complete this project within {{timeline}} and will provide {{deliverables}}.

I'd love to discuss more details. Are you available for a quick call this week?

Best regards,
{{yourName}}`
  },
  
  premium: {
    name: '高端定制提案',
    description: '针对高预算项目的详细提案',
    structure: [
      '深度需求分析',
      '详细解决方案',
      '案例展示',
      '分阶段交付计划',
      '投资回报说明'
    ],
    template: `Dear {{clientName}},

After analyzing your project "{{projectTitle}}", I understand you're looking for {{keyNeed}}.

**Why I'm the right fit:**
- {{achievement1}}
- {{achievement2}}
- {{achievement3}}

**My Approach:**
Phase 1: {{phase1}} ({{time1}})
Phase 2: {{phase2}} ({{time2}})
Phase 3: {{phase3}} ({{time3}})

**Investment:** {{price}}
**Expected ROI:** {{roi}}

I've attached relevant case studies. Let's schedule a call to discuss how we can achieve {{clientGoal}}.

Best,
{{yourName}}
{{portfolioLink}}`
  },
  
  quick: {
    name: '快速响应提案',
    description: '简洁快速的投标提案',
    structure: [
      '直接开场',
      '核心能力',
      '快速交付承诺'
    ],
    template: `Hi {{clientName}},

I can help you with {{projectTitle}}.

✓ {{skill1}}
✓ {{skill2}}
✓ {{skill3}}

Ready to start immediately. Can deliver within {{timeline}}.

Let's chat!
{{yourName}}`
  },
  
  followup: {
    name: '跟进提案',
    description: '用于跟进未回复的投标',
    structure: [
      '友好提醒',
      '补充信息',
      '再次呼吁'
    ],
    template: `Hi {{clientName}},

Just following up on my proposal for "{{projectTitle}}".

I wanted to share an additional idea: {{newIdea}}

This could help you {{benefit}}.

Still very interested in working together. Are you still reviewing proposals?

Best,
{{yourName}}`
  },
  
  referral: {
    name: '推荐提案',
    description: '通过推荐渠道的提案',
    structure: [
      '提及推荐人',
      '建立信任',
      '快速推进'
    ],
    template: `Hi {{clientName}},

{{referrerName}} suggested I reach out regarding "{{projectTitle}}".

I've previously worked with {{referrerName}} on {{similarWork}}, and they thought my {{skill}} would be a great fit for your needs.

I'd love to learn more about your project. When would be a good time to connect?

Best regards,
{{yourName}}
{{portfolioLink}}`
  }
};

// Success optimization tips
const OPTIMIZATION_TIPS = {
  opening: [
    '前 3 句必须抓住注意力',
    '使用客户姓名增加个性化',
    '提及具体项目细节显示认真阅读',
    '避免通用开场白如"I am interested"'
  ],
  body: [
    '展示相关案例和成果',
    '用数据说话（完成率、满意度等）',
    '提出具体问题显示专业度',
    '聚焦客户痛点而非自我吹嘘'
  ],
  closing: [
    '明确的行动呼吁',
    '提供多种联系方式',
    '表达真实兴趣',
    '避免过于急切'
  ],
  length: [
    '理想长度：150-300 字',
    '超过 400 字转化率下降',
    '少于 100 字显得不够重视',
    '段落间留白提高可读性'
  ],
  keywords: [
    '包含职位描述中的关键词',
    '突出核心技能匹配',
    '使用行业术语显示专业',
    '避免过度使用 jargon'
  ]
};

// Client analysis framework
function analyzeClient(clientData) {
  const analysis = {
    painPoints: [],
    preferences: [],
    redFlags: [],
    matchScore: 0,
    recommendations: []
  };
  
  // Analyze job posting patterns
  if (clientData.budget) {
    if (clientData.budget < 500) {
      analysis.redFlags.push('预算较低，可能期望过高');
      analysis.recommendations.push('明确范围，避免范围蔓延');
    } else if (clientData.budget > 5000) {
      analysis.recommendations.push('高端定位，强调专业性和 ROI');
    }
  }
  
  if (clientData.urgency) {
    analysis.painPoints.push('时间紧迫');
    analysis.recommendations.push('强调快速响应和交付能力');
  }
  
  if (clientData.previousHires) {
    if (clientData.previousHires > 10) {
      analysis.preferences.push('经验丰富的自由职业者');
    }
  }
  
  // Calculate match score
  analysis.matchScore = Math.min(100, 
    (analysis.recommendations.length * 20) + 
    (analysis.painPoints.length * 15)
  );
  
  return analysis;
}

// Generate proposal using AI
async function generateProposal(options) {
  const spinner = ora('正在生成提案...').start();
  
  setTimeout(() => {
    spinner.stop();
    
    const template = TEMPLATES[options.template || 'standard'];
    let proposal = template.template;
    
    // Replace placeholders
    proposal = proposal
      .replace(/{{clientName}}/g, options.clientName || 'Hiring Manager')
      .replace(/{{projectTitle}}/g, options.projectTitle || 'your project')
      .replace(/{{years}}/g, options.experience || '5')
      .replace(/{{skills}}/g, options.skills || 'relevant skills')
      .replace(/{{similarProjects}}/g, options.projectCount || '50+')
      .replace(/{{timeline}}/g, options.timeline || '2 weeks')
      .replace(/{{yourName}}/g, options.yourName || 'Your Name');
    
    console.log(chalk.green('\n✓ 提案生成成功！\n'));
    console.log(chalk.blue('─'.repeat(60)));
    console.log(proposal);
    console.log(chalk.blue('─'.repeat(60)));
    
    // Save to file
    if (options.save) {
      const filename = `proposal-${Date.now()}.md`;
      fs.writeFileSync(filename, proposal);
      console.log(chalk.gray(`\n已保存到：${filename}`));
    }
  }, 1500);
}

// Optimize existing proposal
async function optimizeProposal(proposalText) {
  const spinner = ora('正在分析提案...').start();
  
  setTimeout(() => {
    spinner.stop();
    
    console.log(chalk.green('\n✓ 优化建议\n'));
    
    const wordCount = proposalText.split(/\s+/).length;
    
    console.log(chalk.yellow('📊 基础分析:'));
    console.log(`  字数：${wordCount} ${wordCount < 150 ? chalk.red('(过短)') : wordCount > 400 ? chalk.red('(过长)') : chalk.green('(合适)')}`);
    console.log(`  段落数：${proposalText.split('\n\n').length}`);
    
    console.log(chalk.yellow('\n💡 优化建议:'));
    
    if (wordCount > 400) {
      console.log(chalk.red('  ⚠ 提案过长，建议精简到 300 字以内'));
    }
    
    if (!proposalText.includes('Hi') && !proposalText.includes('Dear')) {
      console.log(chalk.red('  ⚠ 缺少个性化称呼'));
    }
    
    if (!proposalText.includes('?')) {
      console.log(chalk.yellow('  💡 建议添加问题以增加互动'));
    }
    
    console.log(chalk.yellow('\n📋 检查清单:'));
    OPTIMIZATION_TIPS.opening.forEach(tip => {
      console.log(`  ${chalk.gray('○')} ${tip}`);
    });
    
  }, 1200);
}

// List templates
function listTemplates() {
  console.log(chalk.blue('\n📋 提案模板库\n'));
  
  Object.entries(TEMPLATES).forEach(([key, template]) => {
    console.log(chalk.green(`  ${key.toUpperCase()}`));
    console.log(chalk.white(`  ${template.name}`));
    console.log(chalk.gray(`  ${template.description}`));
    console.log(chalk.gray(`  结构：${template.structure.join(' → ')}\n`));
  });
}

// CLI Commands
program
  .name('freelance-proposal')
  .description('AI-powered Freelancer/Upwork proposal generator')
  .version('1.0.0');

program
  .command('write')
  .description('生成投标提案')
  .option('-j, --job <description>', '职位描述')
  .option('-s, --skills <skills>', '你的技能')
  .option('-t, --template <type>', '模板类型', 'standard')
  .option('-n, --name <name>', '客户姓名')
  .option('--save', '保存到文件')
  .action((options) => {
    if (!options.job) {
      console.log(chalk.red('请提供职位描述：--job "description"'));
      process.exit(1);
    }
    generateProposal(options);
  });

program
  .command('analyze')
  .description('分析客户/职位')
  .option('-c, --client <data>', '客户信息')
  .option('-b, --budget <amount>', '预算')
  .action((options) => {
    const analysis = analyzeClient({
      budget: options.budget,
      urgency: options.client?.includes('urgent'),
      previousHires: 5
    });
    
    console.log(chalk.blue('\n📊 客户分析\n'));
    console.log(`匹配度：${chalk.green(analysis.matchScore + '%')}`);
    
    if (analysis.painPoints.length) {
      console.log(chalk.yellow('\n痛点:'));
      analysis.painPoints.forEach(p => console.log(`  • ${p}`));
    }
    
    if (analysis.recommendations.length) {
      console.log(chalk.green('\n建议:'));
      analysis.recommendations.forEach(r => console.log(`  • ${r}`));
    }
    
    if (analysis.redFlags.length) {
      console.log(chalk.red('\n警示:'));
      analysis.redFlags.forEach(r => console.log(`  ⚠ ${r}`));
    }
  });

program
  .command('optimize')
  .description('优化现有提案')
  .argument('<proposal>', '提案内容')
  .action((proposal) => {
    optimizeProposal(proposal);
  });

program
  .command('templates')
  .description('列出可用模板')
  .action(listTemplates);

program
  .command('tips')
  .description('显示成功率优化技巧')
  .action(() => {
    console.log(chalk.blue('\n💡 成功率优化技巧\n'));
    
    Object.entries(OPTIMIZATION_TIPS).forEach(([category, tips]) => {
      console.log(chalk.green(`${category.toUpperCase()}:`));
      tips.forEach(tip => console.log(`  ${chalk.gray('•')} ${tip}`));
      console.log();
    });
  });

program.parse();
