/**
 * 导出模块
 * 负责将对话导出为 Markdown 等格式
 */

const fs = require('fs');
const path = require('path');

/**
 * 导出为 Markdown
 * @param {Object} session - 会话数据
 * @param {Object} options - 选项
 * @returns {string} Markdown 内容
 */
function exportToMarkdown(session, options = {}) {
  const { includeContent = true } = options;
  
  let md = `# ${session.title || '对话记录'}\n\n`;
  
  // 基本信息
  md += `## 基本信息\n\n`;
  md += `- 时间：${formatDate(session.date || new Date())}\n`;
  md += `- 主题：${session.topic || '未分类'}\n`;
  if (session.duration) {
    md += `- 时长：${session.duration}\n`;
  }
  md += `\n`;
  
  // 总结
  if (session.summary) {
    md += `## 总结\n\n`;
    md += `${session.summary}\n\n`;
  }
  
  // 待办事项
  if (session.todos && session.todos.length > 0) {
    md += `## 待办事项\n\n`;
    session.todos.forEach((todo, index) => {
      const checkbox = todo.done ? '[x]' : '[ ]';
      const priority = todo.priority ? ` - 优先级：${todo.priority}` : '';
      md += `${index + 1}. ${checkbox} ${todo.content}${priority}\n`;
    });
    md += `\n`;
  }
  
  // 想法/灵感
  if (session.ideas && session.ideas.length > 0) {
    md += `## 想法/灵感\n\n`;
    session.ideas.forEach((idea, index) => {
      md += `${index + 1}. 💡 ${idea.content}\n`;
    });
    md += `\n`;
  }
  
  // 关键决策
  if (session.decisions && session.decisions.length > 0) {
    md += `## 关键决策\n\n`;
    session.decisions.forEach((decision, index) => {
      md += `${index + 1}. 🎯 ${decision.content}\n`;
    });
    md += `\n`;
  }
  
  // 代码片段
  if (session.code && session.code.length > 0) {
    md += `## 代码片段\n\n`;
    session.code.forEach((code, index) => {
      const lang = code.language || 'text';
      md += `### 代码 ${index + 1}\n\n`;
      if (code.description) {
        md += `${code.description}\n\n`;
      }
      md += `\`\`\`${lang}\n${code.content}\n\`\`\`\n\n`;
    });
  }
  
  // 链接
  if (session.links && session.links.length > 0) {
    md += `## 链接\n\n`;
    session.links.forEach((link, index) => {
      md += `${index + 1}. ${link.url}${link.description ? ` - ${link.description}` : ''}\n`;
    });
    md += `\n`;
  }
  
  // 标签
  if (session.tags && session.tags.length > 0) {
    md += `## 标签\n\n`;
    md += session.tags.map(tag => `#${tag}`).join(' ') + `\n`;
  }
  
  // 原始内容（可选）
  if (includeContent && session.content) {
    md += `\n---\n\n`;
    md += `## 原始对话\n\n`;
    md += session.content;
  }
  
  return md;
}

/**
 * 导出到文件
 * @param {string} content - 文件内容
 * @param {string} outputPath - 输出路径
 * @returns {Object} 结果
 */
function exportToFile(content, outputPath) {
  try {
    // 确保目录存在
    const dir = path.dirname(outputPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(outputPath, content, 'utf-8');
    
    return {
      success: true,
      path: outputPath,
      size: content.length
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 格式化日期
 * @param {string|Date} date - 日期
 * @returns {string} 格式化后的日期
 */
function formatDate(date) {
  const d = new Date(date);
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  
  return `${year}-${month}-${day} ${hours}:${minutes}`;
}

module.exports = {
  exportToMarkdown,
  exportToFile,
  formatDate
};
