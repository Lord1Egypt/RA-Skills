/**
 * 速查表生成器 - Markdown 渲染器
 * 
 * 将模板数据渲染为格式化的 Markdown 输出
 */

const templates = require('./templates');

/**
 * 渲染速查表
 * @param {string} topic - 主题关键词
 * @returns {string} Markdown 格式的速查表
 */
function renderCheatSheet(topic) {
  // 1. 查找匹配的模板
  const template = findTemplate(topic);
  
  if (template) {
    return renderFromTemplate(template);
  } else {
    return generateByAI(topic);
  }
}

/**
 * 查找匹配的模板
 * @param {string} topic - 主题关键词
 * @returns {object|null} 匹配的模板或 null
 */
function findTemplate(topic) {
  const topicLower = topic.toLowerCase();
  
  for (const key in templates) {
    const template = templates[key];
    // 检查关键词匹配
    for (const keyword of template.keywords) {
      if (topicLower.includes(keyword.toLowerCase())) {
        return template;
      }
    }
    // 检查 ID 匹配
    if (topicLower.includes(template.id.toLowerCase())) {
      return template;
    }
  }
  
  return null;
}

/**
 * 从模板渲染
 * @param {object} template - 模板对象
 * @returns {string} Markdown 格式
 */
function renderFromTemplate(template) {
  let output = `# 📋 ${template.title}\n\n`;
  output += `*版本：v1.0.0 | 最后更新：2026-03-23*\n\n`;
  output += `---\n\n`;
  
  for (const section of template.sections) {
    output += `## ${section.name}\n\n`;
    
    if (section.type === 'checklist') {
      for (const item of section.items) {
        output += `- [ ] ${item}\n`;
      }
      output += '\n';
    } 
    else if (section.type === 'commands') {
      output += '```bash\n';
      for (const item of section.items) {
        output += `${item.cmd.padEnd(50)} # ${item.desc}\n`;
      }
      output += '```\n\n';
    }
    else if (section.type === 'code') {
      output += '```yaml\n';
      output += section.content;
      output += '\n```\n\n';
    }
    else if (section.type === 'faq') {
      for (const item of section.items) {
        output += `**Q**: ${item.q}\n\n`;
        output += `**A**: ${item.a}\n\n`;
      }
    }
    else if (section.type === 'tips') {
      for (const item of section.items) {
        output += `💡 ${item}\n\n`;
      }
    }
  }
  
  return output.trim();
}

/**
 * AI 生成速查表（当没有模板时）
 * @param {string} topic - 主题
 * @returns {string} 提示用户 AI 生成
 */
function generateByAI(topic) {
  return `📋 ${topic} 速查表（AI 生成）

> ⚠️ 当前没有"${topic}"的内置模板，以下是 AI 生成的参考内容：

## 🚀 核心内容

（AI 根据知识库生成）

## 💡 建议

如果你想获得更高质量的速查表，可以：
1. 贡献模板到技能库
2. 使用已有的模板（npm/Git/OpenClaw 技能开发）
3. 手动整理后分享给我们

---

*提示：内置模板经过实战验证，质量更高。欢迎贡献新模板！*`;
}

/**
 * 获取所有可用模板列表
 * @returns {array} 模板列表
 */
function listTemplates() {
  return Object.values(templates).map(t => ({
    id: t.id,
    title: t.title,
    keywords: t.keywords
  }));
}

/**
 * 搜索模板
 * @param {string} keyword - 搜索关键词
 * @returns {object} 搜索结果（exact: 精确匹配，partial: 部分匹配）
 */
function searchTemplates(keyword) {
  const keywordLower = keyword.toLowerCase();
  const results = {
    exact: [],    // 标题或关键词匹配
    partial: []   // 内容匹配
  };
  
  for (const key in templates) {
    const template = templates[key];
    let score = 0;
    let matches = [];
    
    // 检查标题匹配（50 分）
    if (template.title.toLowerCase().includes(keywordLower)) {
      score += 50;
      matches.push('标题');
    }
    
    // 检查关键词匹配（每个 20 分，最高 60 分）
    for (const kw of template.keywords) {
      if (kw.toLowerCase().includes(keywordLower)) {
        score += 20;
        matches.push(`关键词:${kw}`);
        if (score >= 70) break; // 关键词匹配最高 60 分
      }
    }
    
    // 检查 ID 匹配（30 分）
    if (template.id.toLowerCase().includes(keywordLower)) {
      score += 30;
      matches.push('ID');
    }
    
    // 如果标题/关键词/ID 有匹配，加入精确匹配
    if (score >= 50) {
      results.exact.push({
        template: {
          id: template.id,
          title: template.title,
          keywords: template.keywords
        },
        score: Math.min(score, 100),
        matches: matches
      });
    } else {
      // 否则搜索内容（部分匹配）
      const contentMatches = searchInContent(template, keywordLower);
      if (contentMatches.length > 0) {
        results.partial.push({
          template: {
            id: template.id,
            title: template.title,
            keywords: template.keywords
          },
          score: 30 + contentMatches.length * 5, // 内容匹配每个 5 分，最高 30 分
          matches: contentMatches.slice(0, 3) // 只显示前 3 个匹配
        });
      }
    }
  }
  
  // 按匹配度排序
  results.exact.sort((a, b) => b.score - a.score);
  results.partial.sort((a, b) => b.score - a.score);
  
  return results;
}

/**
 * 在模板内容中搜索关键词
 * @param {object} template - 模板对象
 * @param {string} keyword - 搜索关键词
 * @returns {array} 匹配的内容片段
 */
function searchInContent(template, keyword) {
  const matches = [];
  
  for (const section of template.sections) {
    if (section.name.toLowerCase().includes(keyword)) {
      matches.push(section.name);
    }
    
    if (section.type === 'checklist' || section.type === 'tips') {
      for (const item of section.items) {
        if (item.toLowerCase && item.toLowerCase().includes(keyword)) {
          matches.push(`${section.name}: ${item.substring(0, 30)}...`);
          break; // 每个模块只记录一个匹配
        }
      }
    } else if (section.type === 'commands') {
      for (const item of section.items) {
        if (item.cmd.toLowerCase().includes(keyword) || item.desc.toLowerCase().includes(keyword)) {
          matches.push(`${section.name}: ${item.desc}`);
          break;
        }
      }
    } else if (section.type === 'faq') {
      for (const item of section.items) {
        if (item.q.toLowerCase().includes(keyword) || item.a.toLowerCase().includes(keyword)) {
          matches.push(`${section.name}: ${item.q}`);
          break;
        }
      }
    }
  }
  
  return matches;
}

module.exports = {
  renderCheatSheet,
  listTemplates,
  searchTemplates
};
