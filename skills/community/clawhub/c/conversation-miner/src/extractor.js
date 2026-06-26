/**
 * 信息提取模块
 * 负责从对话中提取待办、想法、代码、决策等结构化信息
 */

/**
 * 提取所有类型信息
 * @param {string} content - 对话内容
 * @returns {Object} 提取结果
 */
function extractAll(content) {
  return {
    todos: extractTodos(content),
    ideas: extractIdeas(content),
    decisions: extractDecisions(content),
    code: extractCode(content),
    links: extractLinks(content)
  };
}

/**
 * 提取待办事项
 * @param {string} content - 对话内容
 * @returns {Array<Object>} 待办列表
 */
function extractTodos(content) {
  const todos = [];
  const lines = content.split('\n');
  
  // 待办关键词
  const todoPatterns = [
    /^(?:需要 | 要 | 应该 | 必须 | 记得 | 别忘了？)\s*[：:]\s*(.+)/i,
    /^(?:todo|to do|task|任务)\s*[：:]\s*(.+)/i,
    /^\s*[-*•]\s*\[\s*\]\s*(.+)/,
    /^\s*\d+\.\s*\[\s*\]\s*(.+)/,
    /^(?:待办 | 代办 | 要做 | 要做的事)\s*[：:]\s*(.+)/i
  ];
  
  lines.forEach((line, index) => {
    const trimmed = line.trim();
    
    for (const pattern of todoPatterns) {
      const match = trimmed.match(pattern);
      if (match) {
        const todo = {
          id: `todo_${Date.now()}_${index}`,
          content: match[1].trim(),
          priority: detectPriority(trimmed),
          done: false,
          createdAt: new Date().toISOString()
        };
        
        // 尝试提取截止日期
        const deadline = extractDeadline(trimmed);
        if (deadline) {
          todo.deadline = deadline;
        }
        
        todos.push(todo);
        break;
      }
    }
  });
  
  return todos;
}

/**
 * 提取想法/灵感
 * @param {string} content - 对话内容
 * @returns {Array<Object>} 想法列表
 */
function extractIdeas(content) {
  const ideas = [];
  const lines = content.split('\n');
  
  // 想法关键词
  const ideaPatterns = [
    /^(?:想法 | 灵感 | 创意 | 点子 | 思路)\s*[：:]\s*(.+)/i,
    /^(?:idea|thought|think|maybe|perhaps|说不定)\s*[：:]\s*(.+)/i,
    /^(?:也许 | 或许 | 可能 | 要不要 | 不如)\s*(.+)/i,
    /^(?:💡|🤔|💭)\s*(.+)/
  ];
  
  lines.forEach((line, index) => {
    const trimmed = line.trim();
    
    for (const pattern of ideaPatterns) {
      const match = trimmed.match(pattern);
      if (match) {
        ideas.push({
          id: `idea_${Date.now()}_${index}`,
          content: match[1].trim(),
          createdAt: new Date().toISOString()
        });
        break;
      }
    }
  });
  
  return ideas;
}

/**
 * 提取决策
 * @param {string} content - 对话内容
 * @returns {Array<Object>} 决策列表
 */
function extractDecisions(content) {
  const decisions = [];
  const lines = content.split('\n');
  
  // 决策关键词
  const decisionPatterns = [
    /^(?:决定 | 确定 | 选定 | 采用 | 选择 | 同意)\s*[：:]\s*(.+)/i,
    /^(?:decision|decided|choose|selected|adopted)\s*[：:]\s*(.+)/i,
    /^(?:我们就 | 那就 | 好了就 | 这样吧|ok 就)\s*(.+)/i,
    /^(?:🎯|✅|👌)\s*(.+)/
  ];
  
  lines.forEach((line, index) => {
    const trimmed = line.trim();
    
    for (const pattern of decisionPatterns) {
      const match = trimmed.match(pattern);
      if (match) {
        decisions.push({
          id: `decision_${Date.now()}_${index}`,
          content: match[1].trim(),
          createdAt: new Date().toISOString()
        });
        break;
      }
    }
  });
  
  return decisions;
}

/**
 * 提取代码片段
 * @param {string} content - 对话内容
 * @returns {Array<Object>} 代码列表
 */
function extractCode(content) {
  const codeBlocks = [];
  
  // 匹配 Markdown 代码块
  const codeBlockPattern = /```(\w+)?\n([\s\S]*?)```/g;
  let match;
  
  while ((match = codeBlockPattern.exec(content)) !== null) {
    codeBlocks.push({
      id: `code_${Date.now()}_${codeBlocks.length}`,
      language: match[1] || 'text',
      code: match[2].trim(),
      createdAt: new Date().toISOString()
    });
  }
  
  // 匹配行内代码（单行）
  const inlineCodePattern = /`([^`]+)`/g;
  while ((match = inlineCodePattern.exec(content)) !== null) {
    const code = match[1].trim();
    // 只提取看起来像代码的内容
    if (code.includes('(') || code.includes('=') || code.includes('.') || code.length > 5) {
      codeBlocks.push({
        id: `code_${Date.now()}_${codeBlocks.length}`,
        language: 'inline',
        code: code,
        createdAt: new Date().toISOString()
      });
    }
  }
  
  return codeBlocks;
}

/**
 * 提取链接
 * @param {string} content - 对话内容
 * @returns {Array<Object>} 链接列表
 */
function extractLinks(content) {
  const links = [];
  const urlPattern = /(https?:\/\/[^\s<>"{}|\\^`\[\]]+)/g;
  let match;
  
  while ((match = urlPattern.exec(content)) !== null) {
    const url = match[1];
    links.push({
      id: `link_${Date.now()}_${links.length}`,
      url: url,
      createdAt: new Date().toISOString()
    });
  }
  
  return links;
}

/**
 * 检测优先级
 * @param {string} text - 文本
 * @returns {string} 优先级
 */
function detectPriority(text) {
  const lower = text.toLowerCase();
  
  if (lower.includes('紧急') || lower.includes('优先') || lower.includes('priority') || lower.includes('urgent')) {
    return '高';
  }
  if (lower.includes('重要') || lower.includes('important')) {
    return '中';
  }
  
  return '低';
}

/**
 * 提取截止日期
 * @param {string} text - 文本
 * @returns {string|null} 截止日期
 */
function extractDeadline(text) {
  // 匹配日期格式：YYYY-MM-DD, YYYY/MM/DD, MM/DD, 明天，下周等
  const datePatterns = [
    /(\d{4}[-/]\d{1,2}[-/]\d{1,2})/,
    /(\d{1,2}月\d{1,2}日)/,
    /(明天|后天|本周五|下周一|下周|月底|年底)/
  ];
  
  for (const pattern of datePatterns) {
    const match = text.match(pattern);
    if (match) {
      return match[1];
    }
  }
  
  return null;
}

/**
 * 格式化提取结果
 * @param {Object} extracted - 提取结果
 * @param {string} type - 类型 (todos/ideas/decisions/code/all)
 * @returns {string} 格式化的输出
 */
function formatExtracted(extracted, type = 'all') {
  let output = '';
  
  if (type === 'todos' || type === 'all') {
    const todos = extracted.todos || [];
    if (todos.length > 0 || type === 'todos') {
      output += `✅ 待办事项 (${todos.length}个)\n\n`;
      todos.forEach((todo, index) => {
        const priority = todo.priority === '高' ? '🔴' : todo.priority === '中' ? '🟡' : '🟢';
        const deadline = todo.deadline ? ` | 截止：${todo.deadline}` : '';
        output += `${index + 1}. [ ] ${todo.content} - 优先级：${priority}${deadline}\n`;
      });
      output += '\n';
    }
  }
  
  if (type === 'ideas' || type === 'all') {
    const ideas = extracted.ideas || [];
    if (ideas.length > 0 || type === 'ideas') {
      output += `💡 想法/灵感 (${ideas.length}个)\n\n`;
      ideas.forEach((idea, index) => {
        output += `${index + 1}. ${idea.content}\n`;
      });
      output += '\n';
    }
  }
  
  if (type === 'decisions' || type === 'all') {
    const decisions = extracted.decisions || [];
    if (decisions.length > 0 || type === 'decisions') {
      output += `🎯 关键决策 (${decisions.length}个)\n\n`;
      decisions.forEach((decision, index) => {
        output += `${index + 1}. ${decision.content}\n`;
      });
      output += '\n';
    }
  }
  
  if (type === 'code' || type === 'all') {
    const code = extracted.code || [];
    if (code.length > 0 || type === 'code') {
      output += `💻 代码片段 (${code.length}个)\n\n`;
      code.forEach((block, index) => {
        output += `${index + 1}. ${block.language === 'inline' ? '行内代码' : block.language + ' 代码'}:\n`;
        output += `\`\`\`${block.language}\n${block.code}\n\`\`\`\n\n`;
      });
    }
  }
  
  return output.trim();
}

module.exports = {
  extractAll,
  extractTodos,
  extractIdeas,
  extractDecisions,
  extractCode,
  extractLinks,
  formatExtracted,
  detectPriority,
  extractDeadline
};
