#!/usr/bin/env node

/**
 * Script Generator - 从信息生成视频脚本
 * 
 * 用法:
 *   node script-generator.js --topic "张雪峰猝死" --style "深度分析"
 *   node script-generator.js --input data.json --output script.md
 */

const fs = require('fs');
const path = require('path');

// 脚本模板库
const SCRIPT_TEMPLATES = {
  // 深度分析型
  'analysis': {
    intro: `
【开场】
大家好，我是{avatar_name}。
今天我们来聊一个引发广泛讨论的话题：{topic}

这个事件背后反映了什么？我们能学到什么？
让我们一起来看看。
    `.trim(),
    
    body: `
【主体】
{content}
    `.trim(),
    
    conclusion: `
【结尾】
这个事件提醒我们：
{key_takeaways}

感谢你的观看。如果你有想法，欢迎在评论区分享。
    `.trim()
  },

  // 故事型
  'story': {
    intro: `
【开场】
这是一个真实发生的故事。
{topic}
    `.trim(),
    
    body: `
【故事】
{content}
    `.trim(),
    
    conclusion: `
【结尾】
{conclusion_text}
    `.trim()
  },

  // 教育型
  'educational': {
    intro: `
【开场】
你知道吗？{topic}

今天我们来深入了解这个话题。
    `.trim(),
    
    body: `
【知识点】
{content}
    `.trim(),
    
    conclusion: `
【总结】
记住这些要点：
{key_points}
    `.trim()
  }
};

// 脚本生成器
class ScriptGenerator {
  constructor(options = {}) {
    this.topic = options.topic || '未命名话题';
    this.style = options.style || 'analysis';
    this.avatarName = options.avatarName || 'AI助手';
    this.duration = options.duration || 60; // 秒
    this.language = options.language || 'zh-CN';
  }

  /**
   * 从结构化数据生成脚本
   */
  generateFromData(data) {
    const template = SCRIPT_TEMPLATES[this.style] || SCRIPT_TEMPLATES['analysis'];
    
    const script = {
      title: data.title || this.topic,
      duration: this.duration,
      language: this.language,
      sections: []
    };

    // 开场
    script.sections.push({
      type: 'intro',
      text: template.intro
        .replace('{avatar_name}', this.avatarName)
        .replace('{topic}', this.topic),
      duration: Math.ceil(this.duration * 0.1)
    });

    // 主体
    script.sections.push({
      type: 'body',
      text: template.body
        .replace('{content}', data.content || ''),
      duration: Math.ceil(this.duration * 0.7)
    });

    // 结尾
    script.sections.push({
      type: 'conclusion',
      text: template.conclusion
        .replace('{key_takeaways}', data.keyTakeaways || '')
        .replace('{conclusion_text}', data.conclusion || ''),
      duration: Math.ceil(this.duration * 0.2)
    });

    return script;
  }

  /**
   * 生成 Markdown 格式的脚本
   */
  toMarkdown(script) {
    let md = `# ${script.title}\n\n`;
    md += `**时长**: ${script.duration}秒\n`;
    md += `**语言**: ${script.language}\n\n`;

    script.sections.forEach((section, idx) => {
      md += `## 第 ${idx + 1} 部分 - ${section.type.toUpperCase()}\n`;
      md += `*时长: ${section.duration}秒*\n\n`;
      md += `${section.text}\n\n`;
      md += `---\n\n`;
    });

    return md;
  }

  /**
   * 生成 JSON 格式的脚本（用于数字人 API）
   */
  toJSON(script) {
    return {
      title: script.title,
      duration: script.duration,
      language: this.language,
      avatar: {
        name: this.avatarName,
        style: 'professional'
      },
      scenes: script.sections.map((section, idx) => ({
        id: `scene_${idx}`,
        type: section.type,
        duration: section.duration,
        text: section.text,
        voiceSettings: {
          speed: 1.0,
          pitch: 1.0,
          emotion: 'neutral'
        }
      }))
    };
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

  const generator = new ScriptGenerator({
    topic: options.topic || '示例话题',
    style: options.style || 'analysis',
    avatarName: options.avatar || 'AI助手',
    duration: parseInt(options.duration) || 60
  });

  // 示例数据
  const sampleData = {
    title: options.topic || '示例话题',
    content: options.content || '这是示例内容。',
    keyTakeaways: options.takeaways || '这是关键要点。',
    conclusion: options.conclusion || '感谢观看。'
  };

  const script = generator.generateFromData(sampleData);
  
  if (options.format === 'json') {
    console.log(JSON.stringify(generator.toJSON(script), null, 2));
  } else {
    console.log(generator.toMarkdown(script));
  }
}

module.exports = ScriptGenerator;
