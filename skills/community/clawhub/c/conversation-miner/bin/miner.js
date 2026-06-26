#!/usr/bin/env node

/**
 * 对话助手 CLI
 * Conversation Miner - 对话价值提取器
 */

const storage = require('../src/storage');
const summarizer = require('../src/summarizer');
const extractor = require('../src/extractor');
const exporter = require('../src/exporter');
const search = require('../src/search');

// 获取当前用户 ID
function getUserId() {
  const args = process.argv.slice(2);
  const userArg = args.find(arg => arg.startsWith('--user='));
  if (userArg) {
    return userArg.split('=')[1];
  }
  return process.env.MINER_USER || 'default';
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    showHelp();
    return;
  }
  
  switch (command) {
    case 'summarize':
      handleSummarize(args.slice(1));
      break;
    case 'extract':
      handleExtract(args.slice(1));
      break;
    case 'export':
      handleExport(args.slice(1));
      break;
    case 'search':
      handleSearch(args.slice(1));
      break;
    case 'tags':
      handleTags(args.slice(1));
      break;
    case 'test':
      runTest();
      break;
    default:
      handleNaturalLanguage(args.join(' '));
  }
}

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
💬 对话助手 (Conversation Miner)

用法：miner <命令> [参数]

命令:
  summarize [文本] [--topic 主题]     总结对话
  extract <todos|ideas|code|decisions|all> [文本]  提取信息
  export <--format markdown> [--output 文件]  导出对话
  search <关键词> [--tag 标签]        搜索对话
  tags                               查看所有标签

示例:
  miner summarize "今天讨论了项目方案..."
  miner extract todos
  miner export --format markdown --output 对话.md
  miner search "Python"
  miner search --tag "项目"

自然语言:
  miner 总结一下刚才的对话
  miner 提取待办事项
  miner 导出对话记录
`);
}

/**
 * 处理总结命令
 */
function handleSummarize(args) {
  const userId = getUserId();
  const data = storage.loadUserData(userId);
  
  // 解析参数
  let text = '';
  let topic = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--topic' && args[i + 1]) {
      topic = args[i + 1];
      i++;
    } else if (!args[i].startsWith('--')) {
      text += args[i] + ' ';
    }
  }
  
  // 如果没有提供文本，使用最近的会话
  if (!text.trim() && data.sessions.length > 0) {
    const lastSession = data.sessions[0];
    text = lastSession.content || '';
  }
  
  if (!text.trim()) {
    console.log('❌ 请提供对话内容或确保有历史会话');
    return;
  }
  
  // 总结
  const result = summarizer.summarize(text, { topic });
  
  console.log(`📊 对话总结`);
  console.log(`\n主题：${result.topic || '未识别'}`);
  console.log(`\n核心要点：`);
  result.keyPoints.forEach((point, index) => {
    console.log(`${index + 1}. ${point}`);
  });
  
  if (result.conclusions && result.conclusions.length > 0) {
    console.log(`\n关键结论：`);
    result.conclusions.forEach((c, index) => {
      console.log(`${index + 1}. ${c}`);
    });
  }
}

/**
 * 处理提取命令
 */
function handleExtract(args) {
  const userId = getUserId();
  const data = storage.loadUserData(userId);
  
  const type = args[0];
  const text = args.slice(1).join(' ');
  
  if (!type) {
    console.log('❌ 请指定提取类型：todos, ideas, code, decisions, all');
    return;
  }
  
  // 获取文本
  let content = text;
  if (!content.trim() && data.sessions.length > 0) {
    const lastSession = data.sessions[0];
    content = lastSession.content || '';
  }
  
  if (!content.trim()) {
    console.log('❌ 请提供对话内容或确保有历史会话');
    return;
  }
  
  // 提取
  const result = extractor.extractAll(content);
  
  switch (type.toLowerCase()) {
    case 'todos':
      printTodos(result.todos);
      break;
    case 'ideas':
      printIdeas(result.ideas);
      break;
    case 'code':
      printCode(result.code);
      break;
    case 'decisions':
      printDecisions(result.decisions);
      break;
    case 'all':
      printAll(result);
      break;
    default:
      console.log('❌ 未知的提取类型，支持：todos, ideas, code, decisions, all');
  }
}

/**
 * 处理导出命令
 */
function handleExport(args) {
  const userId = getUserId();
  const data = storage.loadUserData(userId);
  
  // 解析参数
  let format = 'markdown';
  let output = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--format' && args[i + 1]) {
      format = args[i + 1];
      i++;
    } else if (args[i] === '--output' && args[i + 1]) {
      output = args[i + 1];
      i++;
    }
  }
  
  // 使用最近的会话
  if (data.sessions.length === 0) {
    console.log('❌ 没有历史会话');
    return;
  }
  
  const session = data.sessions[0];
  
  // 导出
  const content = exporter.exportToMarkdown(session);
  
  if (output) {
    const result = exporter.exportToFile(content, output);
    if (result.success) {
      console.log(`✅ 导出成功：${result.path} (${result.size} 字节)`);
    } else {
      console.log(`❌ 导出失败：${result.error}`);
    }
  } else {
    console.log(content);
  }
}

/**
 * 处理搜索命令
 */
function handleSearch(args) {
  const userId = getUserId();
  const data = storage.loadUserData(userId);
  
  // 解析参数
  let query = '';
  let tags = [];
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--tag' && args[i + 1]) {
      tags.push(args[i + 1]);
      i++;
    } else if (!args[i].startsWith('--')) {
      query += args[i] + ' ';
    }
  }
  
  // 搜索
  const results = search.searchSessions(data.sessions, query.trim(), { tags });
  
  if (results.length === 0) {
    console.log('📭 没有找到匹配的对话');
    return;
  }
  
  console.log(`🔍 搜索结果 (${results.length} 个)\n`);
  
  results.forEach((session, index) => {
    console.log(`${index + 1}. ${session.title || '未命名'}`);
    console.log(`   日期：${session.date}`);
    console.log(`   主题：${session.topic || '未分类'}`);
    if (session.summary) {
      console.log(`   总结：${session.summary.slice(0, 100)}...`);
    }
    if (session.tags && session.tags.length > 0) {
      console.log(`   标签：${session.tags.join(', ')}`);
    }
    console.log();
  });
}

/**
 * 处理标签命令
 */
function handleTags() {
  const userId = getUserId();
  const data = storage.loadUserData(userId);
  
  const tags = search.getAllTags(data.sessions);
  
  if (tags.length === 0) {
    console.log('🏷️ 暂无标签');
    return;
  }
  
  console.log(`🏷️ 所有标签 (${tags.length}个)\n`);
  tags.forEach(tag => {
    console.log(`- #${tag}`);
  });
}

/**
 * 打印待办
 */
function printTodos(todos) {
  if (todos.length === 0) {
    console.log('✅ 没有待办事项');
    return;
  }
  
  console.log(`✅ 待办事项 (${todos.length}个)\n`);
  todos.forEach((todo, index) => {
    const checkbox = todo.done ? '[x]' : '[ ]';
    const priority = todo.priority ? ` - 优先级：${todo.priority}` : '';
    console.log(`${index + 1}. ${checkbox} ${todo.content}${priority}`);
  });
}

/**
 * 打印想法
 */
function printIdeas(ideas) {
  if (ideas.length === 0) {
    console.log('💡 没有想法');
    return;
  }
  
  console.log(`💡 想法/灵感 (${ideas.length}个)\n`);
  ideas.forEach((idea, index) => {
    console.log(`${index + 1}. 💡 ${idea.content}`);
  });
}

/**
 * 打印代码
 */
function printCode(codeList) {
  if (codeList.length === 0) {
    console.log('💻 没有代码片段');
    return;
  }
  
  console.log(`💻 代码片段 (${codeList.length}个)\n`);
  codeList.forEach((code, index) => {
    console.log(`${index + 1}. ${code.description || '代码'} (${code.language || 'text'})`);
  });
}

/**
 * 打印决策
 */
function printDecisions(decisions) {
  if (decisions.length === 0) {
    console.log('🎯 没有决策');
    return;
  }
  
  console.log(`🎯 关键决策 (${decisions.length}个)\n`);
  decisions.forEach((decision, index) => {
    console.log(`${index + 1}. 🎯 ${decision.content}`);
  });
}

/**
 * 打印全部
 */
function printAll(result) {
  printTodos(result.todos);
  console.log();
  printIdeas(result.ideas);
  console.log();
  printDecisions(result.decisions);
  console.log();
  printCode(result.code);
}

/**
 * 处理自然语言
 */
function handleNaturalLanguage(input) {
  const text = input.toLowerCase();
  
  if (text.includes('总结') || text.includes('概括')) {
    handleSummarize([]);
    return;
  }
  
  if (text.includes('待办') || text.includes('todo')) {
    handleExtract(['todos']);
    return;
  }
  
  if (text.includes('想法') || text.includes('灵感')) {
    handleExtract(['ideas']);
    return;
  }
  
  if (text.includes('代码')) {
    handleExtract(['code']);
    return;
  }
  
  if (text.includes('决策') || text.includes('决定')) {
    handleExtract(['decisions']);
    return;
  }
  
  if (text.includes('导出')) {
    handleExport(['--format', 'markdown']);
    return;
  }
  
  if (text.includes('搜索') || text.includes('查找')) {
    handleSearch([]);
    return;
  }
  
  showHelp();
}

/**
 * 运行测试
 */
function runTest() {
  console.log('🧪 运行测试...\n');
  
  const testContent = `
今天讨论了项目技术方案。

需要完成的任务：
1. [ ] 完成需求文档
2. [ ] 搭建项目框架
3. [ ] 实现用户登录

想法：
- 可以用游戏化方式提升用户留存
- 考虑添加 AI 助手功能

决定：
- 技术栈：Node.js + PostgreSQL
- 部署方案：Docker + AWS

代码示例：
\`\`\`javascript
const express = require('express');
const app = express();
\`\`\`
`;
  
  console.log('=== 测试总结 ===');
  const summary = summarizer.summarize(testContent);
  console.log(`主题：${summary.topic}`);
  console.log(`要点：${summary.keyPoints.join(', ')}`);
  console.log();
  
  console.log('=== 测试提取 ===');
  const extracted = extractor.extractAll(testContent);
  console.log(`待办：${extracted.todos.length}个`);
  console.log(`想法：${extracted.ideas.length}个`);
  console.log(`决策：${extracted.decisions.length}个`);
  console.log(`代码：${extracted.code.length}个`);
  console.log();
  
  console.log('✅ 测试完成！');
}

// 运行主函数
main();
