#!/usr/bin/env node

/**
 * 微信公众号文章排版优化工具
 * 支持段落优化、标题层级、可读性增强
 */

const fs = require('fs');
const path = require('path');

// 配置
const defaultConfig = {
  style: 'minimal',           // minimal | professional | casual
  maxParagraph: 300,          // 最大段落字数
  maxSentence: 80,            // 最大句子字数
  addSpacing: true,           // 增加段落间距
  noEmoji: true,              // 去除emoji
  noImages: false,            // 去除图片
  headingStyle: {
    h1: { prefix: '# ', suffix: '', bold: true },
    h2: { prefix: '## ', suffix: '', bold: true },
    h3: { prefix: '### ', suffix: '', bold: false }
  }
};

// 排版风格配置
const styleConfigs = {
  minimal: {
    maxParagraph: 300,
    addSpacing: true,
    noEmoji: true,
    noImages: true,
    emphasisStyle: 'bold'
  },
  professional: {
    maxParagraph: 400,
    addSpacing: true,
    noEmoji: true,
    noImages: false,
    emphasisStyle: 'bold'
  },
  casual: {
    maxParagraph: 250,
    addSpacing: true,
    noEmoji: false,
    noImages: false,
    emphasisStyle: 'italic'
  }
};

// 去除emoji
function removeEmoji(text) {
  return text.replace(/[\u{1F600}-\u{1F64F}]|[\u{1F300}-\u{1F5FF}]|[\u{1F680}-\u{1F6FF}]|[\u{1F700}-\u{1F77F}]|[\u{1F780}-\u{1F7FF}]|[\u{1F800}-\u{1F8FF}]|[\u{1F900}-\u{1F9FF}]|[\u{1FA00}-\u{1FA6F}]|[\u{1FA70}-\u{1FAFF}]|[\u{2600}-\u{26FF}]|[\u{2700}-\u{27BF}]/gu, '');
}

// 去除图片
function removeImages(text) {
  return text.replace(/!\[.*?\]\(.*?\)/g, '').replace(/<img[^>]*>/g, '');
}

// 拆分长段落
function splitParagraph(text, maxLength) {
  if (text.length <= maxLength) {
    return [text];
  }
  
  const sentences = text.split(/[。！？；]/);
  const paragraphs = [];
  let currentParagraph = '';
  
  for (const sentence of sentences) {
    if (sentence.trim()) {
      const newParagraph = currentParagraph ? currentParagraph + sentence + '。' : sentence + '。';
      
      if (newParagraph.length > maxLength) {
        if (currentParagraph) {
          paragraphs.push(currentParagraph.trim());
        }
        currentParagraph = sentence + '。';
      } else {
        currentParagraph = newParagraph;
      }
    }
  }
  
  if (currentParagraph) {
    paragraphs.push(currentParagraph.trim());
  }
  
  return paragraphs;
}

// 格式化标题
function formatHeading(line, level, config) {
  const content = line.replace(/^#+\s*/, '').trim();
  const style = config.headingStyle[`h${level}`];
  
  if (style) {
    return `${style.prefix}${content}${style.suffix}`;
  }
  
  return line;
}

// 优化列表
function formatList(lines, startIndex, config) {
  const formatted = [];
  let i = startIndex;
  
  while (i < lines.length) {
    const line = lines[i].trim();
    
    if (line.startsWith('* ') || line.startsWith('- ') || /^\d+\.\s/.test(line)) {
      formatted.push(line);
      i++;
    } else {
      break;
    }
  }
  
  return { lines: formatted, nextIndex: i };
}

// 主格式化函数
function formatArticle(content, config = {}) {
  const mergedConfig = { ...defaultConfig, ...config, ...styleConfigs[config.style || 'minimal'] };
  
  let processedContent = content;
  
  // 去除emoji
  if (mergedConfig.noEmoji) {
    processedContent = removeEmoji(processedContent);
  }
  
  // 去除图片
  if (mergedConfig.noImages) {
    processedContent = removeImages(processedContent);
  }
  
  const lines = processedContent.split('\n');
  const formatted = [];
  let i = 0;
  
  while (i < lines.length) {
    const line = lines[i].trim();
    
    // 空行处理
    if (line === '') {
      if (formatted.length > 0 && formatted[formatted.length - 1] !== '') {
        if (mergedConfig.addSpacing) {
          formatted.push('');  // 双空行
        }
        formatted.push('');
      }
      i++;
      continue;
    }
    
    // 标题处理
    if (line.startsWith('# ')) {
      formatted.push('');
      formatted.push(formatHeading(line, 1, mergedConfig));
      formatted.push('');
      i++;
      continue;
    }
    
    if (line.startsWith('## ')) {
      formatted.push('');
      formatted.push(formatHeading(line, 2, mergedConfig));
      formatted.push('');
      i++;
      continue;
    }
    
    if (line.startsWith('### ')) {
      formatted.push('');
      formatted.push(formatHeading(line, 3, mergedConfig));
      formatted.push('');
      i++;
      continue;
    }
    
    // 列表处理
    if (line.startsWith('* ') || line.startsWith('- ') || /^\d+\.\s/.test(line)) {
      const result = formatList(lines, i, mergedConfig);
      formatted.push('');
      formatted.push(...result.lines);
      formatted.push('');
      i = result.nextIndex;
      continue;
    }
    
    // 引用处理
    if (line.startsWith('> ')) {
      formatted.push('');
      formatted.push(line);
      formatted.push('');
      i++;
      continue;
    }
    
    // 分割线处理
    if (line === '---' || line === '***') {
      formatted.push('');
      formatted.push(line);
      formatted.push('');
      i++;
      continue;
    }
    
    // 普通段落处理
    const paragraphs = splitParagraph(line, mergedConfig.maxParagraph);
    
    for (const paragraph of paragraphs) {
      formatted.push(paragraph);
      if (mergedConfig.addSpacing) {
        formatted.push('');
      }
    }
    
    i++;
  }
  
  // 清理多余的空行
  const cleaned = [];
  let consecutiveEmpty = 0;
  
  for (const line of formatted) {
    if (line === '') {
      consecutiveEmpty++;
      if (consecutiveEmpty <= 2) {
        cleaned.push(line);
      }
    } else {
      consecutiveEmpty = 0;
      cleaned.push(line);
    }
  }
  
  return cleaned.join('\n');
}

// 分析文章
function analyzeArticle(content) {
  const lines = content.split('\n');
  const stats = {
    totalLines: lines.length,
    totalWords: 0,
    paragraphs: 0,
    headings: 0,
    lists: 0,
    quotes: 0,
    avgParagraphLength: 0,
    readingTime: 0,
    suggestions: []
  };
  
  let totalParagraphLength = 0;
  let inCodeBlock = false;
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    if (trimmed.startsWith('```')) {
      inCodeBlock = !inCodeBlock;
      continue;
    }
    
    if (!inCodeBlock) {
      if (trimmed.startsWith('#')) {
        stats.headings++;
      } else if (trimmed.startsWith('* ') || trimmed.startsWith('- ') || /^\d+\.\s/.test(trimmed)) {
        stats.lists++;
      } else if (trimmed.startsWith('> ')) {
        stats.quotes++;
      } else if (trimmed.length > 0) {
        stats.paragraphs++;
        totalParagraphLength += trimmed.length;
      }
      
      stats.totalWords += trimmed.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '').length;
    }
  }
  
  stats.avgParagraphLength = stats.paragraphs > 0 ? Math.round(totalParagraphLength / stats.paragraphs) : 0;
  stats.readingTime = Math.ceil(stats.totalWords / 300); // 300字/分钟
  
  // 生成建议
  if (stats.avgParagraphLength > 300) {
    stats.suggestions.push('建议缩短段落长度，提高可读性');
  }
  
  if (stats.headings < 3 && stats.totalWords > 1000) {
    stats.suggestions.push('建议添加更多标题，增强结构感');
  }
  
  if (stats.lists < 2 && stats.totalWords > 800) {
    stats.suggestions.push('建议使用列表展示要点，提升可读性');
  }
  
  if (stats.readingTime > 10) {
    stats.suggestions.push('文章较长，建议添加内容摘要或分段发布');
  }
  
  return stats;
}

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);
  
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
微信公众号文章排版优化工具

使用方法:
  node format-article.js <输入文件> [输出文件] [选项]

选项:
  --style <风格>      排版风格: minimal | professional | casual (默认: minimal)
  --analyze          仅分析文章结构
  --help             显示帮助

示例:
  # 格式化文章
  node format-article.js input.md output.md

  # 使用专业风格
  node format-article.js input.md output.md --style professional

  # 仅分析
  node format-article.js input.md --analyze
    `);
    process.exit(0);
  }
  
  if (args.length < 1) {
    console.error('❌ 请指定输入文件');
    process.exit(1);
  }
  
  const inputFile = args[0];
  const outputFile = args[1] && !args[1].startsWith('--') ? args[1] : null;
  
  // 解析选项
  const config = {};
  const styleIndex = args.indexOf('--style');
  if (styleIndex !== -1 && args[styleIndex + 1]) {
    config.style = args[styleIndex + 1];
  }
  
  const analyzeOnly = args.includes('--analyze');
  
  // 读取文件
  if (!fs.existsSync(inputFile)) {
    console.error(`❌ 文件不存在: ${inputFile}`);
    process.exit(1);
  }
  
  const content = fs.readFileSync(inputFile, 'utf8');
  
  // 分析文章
  const stats = analyzeArticle(content);
  
  console.log('📊 文章分析结果:');
  console.log(`   总字数: ${stats.totalWords}字`);
  console.log(`   段落数: ${stats.paragraphs}`);
  console.log(`   标题数: ${stats.headings}`);
  console.log(`   列表项: ${stats.lists}`);
  console.log(`   引用块: ${stats.quotes}`);
  console.log(`   平均段落长度: ${stats.avgParagraphLength}字`);
  console.log(`   预计阅读时间: ${stats.readingTime}分钟`);
  
  if (stats.suggestions.length > 0) {
    console.log('\n💡 优化建议:');
    stats.suggestions.forEach((s, i) => console.log(`   ${i + 1}. ${s}`));
  }
  
  if (analyzeOnly) {
    process.exit(0);
  }
  
  // 格式化文章
  const formatted = formatArticle(content, config);
  
  // 输出结果
  if (outputFile) {
    fs.writeFileSync(outputFile, formatted, 'utf8');
    console.log(`\n✅ 文章已格式化并保存到: ${outputFile}`);
  } else {
    console.log('\n📝 格式化结果:\n');
    console.log(formatted);
  }
}

module.exports = {
  formatArticle,
  analyzeArticle,
  removeEmoji,
  removeImages,
  splitParagraph
};