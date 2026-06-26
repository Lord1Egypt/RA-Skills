#!/usr/bin/env node
/**
 * 学术润色检查清单
 * 基于五级写作体系的快速检查工具
 * 
 * 用法：
 *   node polish-checklist.js "待检查文本"
 *   node polish-checklist.js --file 论文片段.txt
 *   node polish-checklist.js --interactive
 */

// ==================== AI痕迹词库 ====================

const AI_MARKERS = {
  // 高频连接词（需要替换）
  connectors: [
    { word: '因此', count: 0, alternatives: ['由此观之', '这意味着', '换言之', '由此可见'] },
    { word: '从而', count: 0, alternatives: ['进而', '继而', '由此'] },
    { word: '所以', count: 0, alternatives: ['由此', '基于此', '有鉴于此'] },
    { word: '但是', count: 0, alternatives: ['然而', '反观', '值得注意的是', '但更值得追问的是'] },
    { word: '不过', count: 0, alternatives: ['然而', '反观'] },
    { word: '而且', count: 0, alternatives: ['此外', '与此同时', '进而'] },
    { word: '此外', count: 0, alternatives: ['与此同时', '在此基础上'] },
    { word: '首先', count: 0, alternatives: ['首先', '其一', '从...开始'] },
    { word: '其次', count: 0, alternatives: ['其次', '其二', '继而'] },
    { word: '最后', count: 0, alternatives: ['最后', '最终', '由此观之'] },
    { word: '总之', count: 0, alternatives: ['由此观之', '综上所述', '总而言之'] },
    { word: '综上所述', count: 0, alternatives: ['由此观之', '综上所述'] }
  ],
  
  // 对称结构（需要打破）
  symmetryPatterns: [
    { pattern: /一方面[，、](.+?)[，、]另一方面[，、]/g, description: '一方面...另一方面...' },
    { pattern: /不仅(.+?)，而且(.+?)[。；]/g, description: '不仅...而且...' },
    { pattern: /首先(.+?)其次(.+?)再次(.+?)[。；]/g, description: '首先...其次...再次...' },
    { pattern: /虽然(.+?)，但是(.+?)[。；]/g, description: '虽然...但是...' }
  ],
  
  // 抽象套话（需要删除或具体化）
  abstractPhrases: [
    '这是一个复杂的问题',
    '值得进一步研究',
    '具有重要的理论意义',
    '具有重要的现实意义',
    '从某种程度上讲',
    '在一定程度上',
    '不可否认的是',
    '毫无疑问',
    '众所周知',
    '显而易见'
  ],
  
  // 绝对化词汇（需要限定）
  absoluteWords: [
    { word: '必然', suggestion: '某种程度上必然' },
    { word: '完全', suggestion: '几乎' },
    { word: '绝对', suggestion: '几乎可以说' },
    { word: '所有', suggestion: '诸多' },
    { word: '全部', suggestion: '几乎' },
    { word: '总是', suggestion: '往往' },
    { word: '从不', suggestion: '很少' }
  ]
};

// ==================== 检查函数 ====================

class PolishChecker {
  constructor(text) {
    this.original = text;
    this.text = text;
    this.issues = [];
    this.score = 100;
  }

  // 主检查流程
  check() {
    this.checkConnectors();
    this.checkSymmetry();
    this.checkAbstractPhrases();
    this.checkAbsoluteWords();
    this.checkSentenceLength();
    this.checkFirstPerson();
    this.checkRhythm();
    
    return {
      score: Math.max(0, this.score),
      issues: this.issues,
      summary: this.generateSummary()
    };
  }

  // 检查连接词
  checkConnectors() {
    AI_MARKERS.connectors.forEach(marker => {
      const regex = new RegExp(marker.word, 'g');
      const matches = this.text.match(regex);
      if (matches) {
        marker.count = matches.length;
        if (matches.length > 2) {
          this.score -= matches.length * 2;
          this.issues.push({
            type: '高频连接词',
            severity: 'medium',
            content: `"${marker.word}"出现${matches.length}次，建议替换为：${marker.alternatives.join('、')}`,
            suggestion: marker.alternatives[0]
          });
        }
      }
    });
  }

  // 检查对称结构
  checkSymmetry() {
    AI_MARKERS.symmetryPatterns.forEach(pattern => {
      const matches = this.text.match(pattern.pattern);
      if (matches && matches.length > 0) {
        this.score -= matches.length * 5;
        this.issues.push({
          type: '对称结构',
          severity: 'high',
          content: `检测到"${pattern.description}"结构${matches.length}处，建议打破对仗`,
          suggestion: '改为递进或分段呈现'
        });
      }
    });
  }

  // 检查抽象套话
  checkAbstractPhrases() {
    AI_MARKERS.abstractPhrases.forEach(phrase => {
      if (this.text.includes(phrase)) {
        this.score -= 3;
        this.issues.push({
          type: '抽象套话',
          severity: 'medium',
          content: `检测到套话："${phrase}"`,
          suggestion: '删除或给出具体判断'
        });
      }
    });
  }

  // 检查绝对化词汇
  checkAbsoluteWords() {
    AI_MARKERS.absoluteWords.forEach(item => {
      const regex = new RegExp(item.word, 'g');
      const matches = this.text.match(regex);
      if (matches) {
        this.score -= matches.length * 2;
        this.issues.push({
          type: '绝对化表述',
          severity: 'low',
          content: `检测到绝对化词汇："${item.word}"`,
          suggestion: `建议改为"${item.suggestion}"`
        });
      }
    });
  }

  // 检查句子长度
  checkSentenceLength() {
    const sentences = this.text.split(/[。！？；]/);
    let longSentences = 0;
    
    sentences.forEach(sent => {
      if (sent.length > 80) {
        longSentences++;
      }
    });
    
    if (longSentences > 3) {
      this.score -= longSentences * 2;
      this.issues.push({
        type: '句长分布',
        severity: 'medium',
        content: `检测到${longSentences}个过长句子（>80字），建议拆分`,
        suggestion: '长句后接短句，制造呼吸感'
      });
    }
  }

  // 检查第一人称
  checkFirstPerson() {
    const firstPerson = /我|我们|笔者|本文/g;
    const matches = this.text.match(firstPerson);
    if (matches && matches.length > 0) {
      this.score -= matches.length * 3;
      this.issues.push({
        type: '第一人称',
        severity: 'high',
        content: `检测到${matches.length}处第一人称表述`,
        suggestion: '改为客观陈述或使用"这一研究"等替代'
      });
    }
  }

  // 检查节奏感
  checkRhythm() {
    const paragraphs = this.text.split(/\n\n/);
    if (paragraphs.length < 3 && this.text.length > 500) {
      this.issues.push({
        type: '段落结构',
        severity: 'medium',
        content: '段落过少，建议分段增加呼吸感',
        suggestion: '每段一个核心论点，长短交替'
      });
    }
  }

  // 生成总结
  generateSummary() {
    const highIssues = this.issues.filter(i => i.severity === 'high').length;
    const mediumIssues = this.issues.filter(i => i.severity === 'medium').length;
    const lowIssues = this.issues.filter(i => i.severity === 'low').length;
    
    let grade = '';
    if (this.score >= 90) grade = '优秀';
    else if (this.score >= 80) grade = '良好';
    else if (this.score >= 70) grade = '中等';
    else if (this.score >= 60) grade = '及格';
    else grade = '需要大幅修改';
    
    return {
      grade,
      highIssues,
      mediumIssues,
      lowIssues,
      totalIssues: this.issues.length
    };
  }
}

// ==================== 输出格式化 ====================

function formatOutput(result) {
  const { score, issues, summary } = result;
  
  let output = `
╔══════════════════════════════════════════════════════════╗
║           学术润色检查清单 v1.0                     ║
╚══════════════════════════════════════════════════════════╝

📊 综合评分: ${score}/100 (${summary.grade})

📋 问题统计:
   严重问题: ${summary.highIssues} 个
   中等问题: ${summary.mediumIssues} 个
   轻微问题: ${summary.lowIssues} 个
   总计: ${summary.totalIssues} 个问题

`;

  if (issues.length > 0) {
    output += `🔍 详细问题:\n`;
    
    // 按严重程度分组
    const high = issues.filter(i => i.severity === 'high');
    const medium = issues.filter(i => i.severity === 'medium');
    const low = issues.filter(i => i.severity === 'low');
    
    if (high.length > 0) {
      output += `\n【严重】\n`;
      high.forEach((issue, idx) => {
        output += `  ${idx + 1}. [${issue.type}] ${issue.content}\n`;
        output += `     建议: ${issue.suggestion}\n\n`;
      });
    }
    
    if (medium.length > 0) {
      output += `【中等】\n`;
      medium.forEach((issue, idx) => {
        output += `  ${idx + 1}. [${issue.type}] ${issue.content}\n`;
        output += `     建议: ${issue.suggestion}\n\n`;
      });
    }
    
    if (low.length > 0) {
      output += `【轻微】\n`;
      low.forEach((issue, idx) => {
        output += `  ${idx + 1}. [${issue.type}] ${issue.content}\n`;
        output += `     建议: ${issue.suggestion}\n\n`;
      });
    }
  } else {
    output += `✅ 未检测到明显AI痕迹！\n`;
  }

  output += `
💡 通用建议:
• 检查是否打破了对称结构（"一方面...另一方面..."）
• 确保"因此""从而""进而"等词不密集重复
• 长短句交替，避免匀速行文
• 加入限定词（"某种程度上""一定程度上"）
• 适当使用隐喻（"逐鹿""蛰伏""游离""缝合"）
• 分段处理，每段一个核心论点

📖 详细指南:
• style-guide.md - 完整风格指南
• dai-jinhua-framework.md - 批判写作方法
• questioning-library.md - 追问库模板
`;

  return output;
}

// ==================== CLI 界面 ====================

function printHelp() {
  console.log(`
╔══════════════════════════════════════════════════════════╗
║       学术润色检查清单 v1.0                       ║
╚══════════════════════════════════════════════════════════╝

用法:
  node polish-checklist.js "待检查的文本内容"
  node polish-checklist.js --file 论文片段.txt
  node polish-checklist.js --interactive
  node polish-checklist.js --help

检查项目:
  • 高频连接词（"因此""从而""但是"等）
  • 对称结构（"一方面...另一方面..."等）
  • 抽象套话（"这是一个复杂的问题"等）
  • 绝对化表述（"必然""完全""绝对"等）
  • 句子长度（检测过长句子）
  • 第一人称（"我""我们""笔者"等）
  • 段落结构（呼吸感检查）

示例:
  node polish-checklist.js "深度媒介化时代，青年亚文化已经呈现出..."
`);
}

// ==================== 主程序 ====================

function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args.includes('--help')) {
    printHelp();
    return;
  }
  
  let text = '';
  
  // 从文件读取
  if (args.includes('--file')) {
    const fs = require('fs');
    const fileIndex = args.findIndex(a => a === '--file');
    const filePath = args[fileIndex + 1];
    if (!filePath) {
      console.error('错误: 请指定文件路径');
      process.exit(1);
    }
    try {
      text = fs.readFileSync(filePath, 'utf8');
    } catch (e) {
      console.error(`错误: 无法读取文件 ${filePath}`);
      process.exit(1);
    }
  } else {
    // 从命令行参数读取
    text = args.join(' ');
  }
  
  // 执行检查
  const checker = new PolishChecker(text);
  const result = checker.check();
  
  // 输出结果
  console.log(formatOutput(result));
}

// 如果是直接运行此文件
if (require.main === module) {
  main();
}

module.exports = { PolishChecker, AI_MARKERS };
