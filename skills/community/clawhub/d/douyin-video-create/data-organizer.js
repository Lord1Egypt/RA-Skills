#!/usr/bin/env node

/**
 * Data Organizer - 整理和结构化信息
 * 
 * 用法:
 *   node data-organizer.js --input raw-data.txt --output structured.json
 */

const fs = require('fs');
const path = require('path');

class DataOrganizer {
  constructor() {
    this.data = {};
  }

  /**
   * 从文本提取关键信息
   */
  extractKeyInfo(text) {
    const info = {
      title: '',
      summary: '',
      keyPoints: [],
      timeline: [],
      stakeholders: [],
      impact: '',
      lessons: []
    };

    // 简单的提取逻辑（可以用 NLP 改进）
    const lines = text.split('\n').filter(l => l.trim());
    
    if (lines.length > 0) {
      info.title = lines[0];
    }
    
    if (lines.length > 1) {
      info.summary = lines.slice(1, 3).join(' ');
    }

    return info;
  }

  /**
   * 组织信息为脚本友好的格式
   */
  organizeForScript(rawData) {
    const organized = {
      title: rawData.title || '未命名',
      content: this.formatContent(rawData),
      keyTakeaways: this.formatKeyTakeaways(rawData),
      conclusion: this.formatConclusion(rawData),
      metadata: {
        source: rawData.source || '未知',
        date: new Date().toISOString(),
        confidence: rawData.confidence || 0.8
      }
    };

    return organized;
  }

  /**
   * 格式化主体内容
   */
  formatContent(data) {
    let content = '';

    if (data.summary) {
      content += `**背景**: ${data.summary}\n\n`;
    }

    if (data.keyPoints && data.keyPoints.length > 0) {
      content += '**关键信息**:\n';
      data.keyPoints.forEach((point, idx) => {
        content += `${idx + 1}. ${point}\n`;
      });
      content += '\n';
    }

    if (data.timeline && data.timeline.length > 0) {
      content += '**时间线**:\n';
      data.timeline.forEach(event => {
        content += `- ${event.date}: ${event.description}\n`;
      });
      content += '\n';
    }

    if (data.impact) {
      content += `**影响**: ${data.impact}\n`;
    }

    return content.trim();
  }

  /**
   * 格式化关键要点
   */
  formatKeyTakeaways(data) {
    const takeaways = [];

    if (data.lessons && data.lessons.length > 0) {
      takeaways.push(...data.lessons);
    }

    if (data.keyPoints && data.keyPoints.length > 0) {
      takeaways.push(...data.keyPoints.slice(0, 3));
    }

    return takeaways.join('\n');
  }

  /**
   * 格式化结论
   */
  formatConclusion(data) {
    if (data.conclusion) {
      return data.conclusion;
    }

    let conclusion = '这个事件提醒我们需要关注';
    
    if (data.impact) {
      conclusion += `${data.impact}的问题。`;
    }

    conclusion += '希望我们能从中学到有价值的东西。';

    return conclusion;
  }

  /**
   * 从 JSON 文件加载数据
   */
  loadFromJSON(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      return JSON.parse(content);
    } catch (error) {
      console.error(`无法读取文件 ${filePath}:`, error.message);
      return null;
    }
  }

  /**
   * 保存为 JSON
   */
  saveToJSON(data, filePath) {
    try {
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2), 'utf-8');
      console.log(`✓ 已保存到 ${filePath}`);
      return true;
    } catch (error) {
      console.error(`无法保存文件 ${filePath}:`, error.message);
      return false;
    }
  }

  /**
   * 保存为 Markdown
   */
  saveToMarkdown(data, filePath) {
    try {
      let md = `# ${data.title}\n\n`;
      md += `${data.content}\n\n`;
      md += `## 关键要点\n${data.keyTakeaways}\n\n`;
      md += `## 结论\n${data.conclusion}\n`;

      fs.writeFileSync(filePath, md, 'utf-8');
      console.log(`✓ 已保存到 ${filePath}`);
      return true;
    } catch (error) {
      console.error(`无法保存文件 ${filePath}:`, error.message);
      return false;
    }
  }
}

// 命令行接口
if (require.main === module) {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i += 2) {
    const key = args[i].replace('--', '');
    const value = args[i + 1];
    options[key] = value;
  }

  const organizer = new DataOrganizer();

  if (options.input) {
    const rawData = organizer.loadFromJSON(options.input);
    
    if (rawData) {
      const organized = organizer.organizeForScript(rawData);
      
      if (options.output) {
        if (options.output.endsWith('.md')) {
          organizer.saveToMarkdown(organized, options.output);
        } else {
          organizer.saveToJSON(organized, options.output);
        }
      } else {
        console.log(JSON.stringify(organized, null, 2));
      }
    }
  } else {
    console.log('用法: node data-organizer.js --input <file> --output <file>');
  }
}

module.exports = DataOrganizer;
