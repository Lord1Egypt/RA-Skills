#!/usr/bin/env node
/**
 * Session Compactor - 上下文压缩核心逻辑
 * 将长会话压缩为摘要，保留最近上下文
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { pathToFileURL } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============ 配置 ============
const DEFAULT_CONFIG = {
  preserveRecent: 4,      // 保留最近N条消息
  maxTokens: 80000,       // 超过此token数触发压缩
  summaryMaxTokens: 2000,  // 摘要最大token数
  storePath: './.clawsession.json'
};

// ============ 工具函数 ============

/**
 * 估算消息的token数（简化估算）
 */
function estimateMessageTokens(msg) {
  let chars = 0;
  
  if (typeof msg.content === 'string') {
    chars = msg.content.length;
  } else if (msg.content) {
    chars = JSON.stringify(msg.content).length;
  }
  
  // 工具调用额外开销
  let toolOverhead = 0;
  if (msg.toolUse) {
    toolOverhead = 50;
  }
  
  return Math.ceil(chars / 4) + toolOverhead;
}

/**
 * 估算整个会话的token数
 */
function estimateSessionTokens(messages) {
  return messages.reduce((sum, msg) => sum + estimateMessageTokens(msg), 0);
}

/**
 * 截断文本到指定长度
 */
function truncate(text, maxChars) {
  if (text.length <= maxChars) return text;
  return text.slice(0, maxChars - 1) + '…';
}

/**
 * 从文本中提取文件路径
 */
function extractFilePaths(text) {
  const patterns = [
    /\b[\w\-./\\]+\.(rs|py|ts|tsx|js|jsx|json|md|txt|yml|yaml|toml|html|css)\b/gi,
    /[\w\-./\\]+SKILL\.md/gi,
    /[\w\-./\\]+skills\/[\w\-./\\]+/gi,
  ];
  
  const files = new Set();
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(text)) !== null) {
      const file = match[0];
      // 过滤掉太短或太长的
      if (file.length > 5 && file.length < 200 && !file.startsWith('//')) {
        files.add(file);
      }
    }
  }
  
  return Array.from(files).slice(0, 10);
}

/**
 * 提取关键工具调用
 */
function extractToolCalls(messages) {
  const tools = new Map();
  
  for (const msg of messages) {
    if (msg.toolUse) {
      const name = msg.toolUse.name || msg.toolUse.tool_name || 'unknown';
      tools.set(name, (tools.get(name) || 0) + 1);
    }
  }
  
  return Array.from(tools.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([name, count]) => `${name}(x${count})`)
    .join(', ');
}

/**
 * 提取待办事项关键词
 */
function extractPendingWork(messages) {
  const keywords = ['todo', 'next', 'pending', 'follow up', 'remaining', '待办', '下一步'];
  const pending = [];
  
  for (const msg of messages) {
    if (msg.role === 'user' || msg.role === 'assistant') {
      const text = typeof msg.content === 'string' ? msg.content : '';
      const lower = text.toLowerCase();
      
      if (keywords.some(k => lower.includes(k))) {
        pending.push(truncate(text.replace(/\n/g, ' '), 100));
      }
    }
  }
  
  return pending.slice(0, 3);
}

/**
 * 提取最近的用户请求
 */
function extractRecentUserRequests(messages, limit = 3) {
  const requests = [];
  
  for (const msg of messages) {
    if (msg.role === 'user' && msg.content) {
      const text = typeof msg.content === 'string' ? msg.content : '';
      if (text.trim().length > 0) {
        requests.push(truncate(text.replace(/\n/g, ' '), 150));
      }
    }
  }
  
  return requests.slice(-limit).reverse();
}

/**
 * 生成压缩后的摘要文本
 */
function generateSummary(messages, config, existingSummary = null) {
  const lines = ['<summary>'];
  const compactionCount = existingSummary 
    ? (extractCompactionCount(existingSummary) || 0) + 1 
    : 1;
  
  lines.push(`**压缩次数**: ${compactionCount}`);
  lines.push(`**原始消息数**: ${messages.length}`);
  
  // 关键工具
  const toolCalls = extractToolCalls(messages);
  if (toolCalls) {
    lines.push(`**工具调用**: ${toolCalls}`);
  }
  
  // 关键文件
  const allTexts = messages
    .filter(m => m.content && typeof m.content === 'string')
    .map(m => m.content)
    .join(' ');
  const files = extractFilePaths(allTexts);
  if (files.length > 0) {
    lines.push(`**涉及文件**: ${files.join(', ')}`);
  }
  
  // 最近用户请求
  const recentRequests = extractRecentUserRequests(messages);
  if (recentRequests.length > 0) {
    lines.push('');
    lines.push('### 最近用户请求');
    recentRequests.forEach((req, i) => {
      lines.push(`${i + 1}. ${req}`);
    });
  }
  
  // 待完成事项
  const pending = extractPendingWork(messages);
  if (pending.length > 0) {
    lines.push('');
    lines.push('### 待完成事项');
    pending.forEach(item => {
      lines.push(`- ${item}`);
    });
  }
  
  lines.push('</summary>');
  
  return lines.join('\n');
}

/**
 * 从现有摘要中提取压缩次数
 */
function extractCompactionCount(summaryText) {
  const match = summaryText.match(/\*\*压缩次数\*\*:\s*(\d+)/);
  return match ? parseInt(match[1], 10) : null;
}

/**
 * 从现有摘要中提取之前的内容
 */
function extractPreviousSummary(summaryText) {
  const match = summaryText.match(/<summary>([\s\S]*?)<\/summary>/);
  if (!match) return null;
  
  const content = match[1];
  // 提取第一次压缩之后的所有内容
  const parts = content.split(/(?=\*\*压缩次数\*\*:)/);
  if (parts.length <= 1) return null;
  
  return parts.slice(1).join('').trim();
}

// ============ SessionCompactor 类 ============

class SessionCompactor {
  constructor(config = {}) {
    this.config = { ...DEFAULT_CONFIG, ...config };
    this.session = this._loadSession();
  }
  
  /**
   * 加载会话数据
   */
  _loadSession() {
    try {
      if (fs.existsSync(this.config.storePath)) {
        const data = fs.readFileSync(this.config.storePath, 'utf-8');
        return JSON.parse(data);
      }
    } catch (e) {
      console.error('加载会话失败:', e.message);
    }
    
    return this._createEmptySession();
  }
  
  /**
   * 创建空会话
   */
  _createEmptySession() {
    return {
      version: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      messages: [],
      compactionCount: 0,
      totalTokens: 0
    };
  }
  
  /**
   * 保存会话数据
   */
  _saveSession() {
    this.session.updatedAt = new Date().toISOString();
    fs.writeFileSync(
      this.config.storePath,
      JSON.stringify(this.session, null, 2),
      'utf-8'
    );
  }
  
  /**
   * 估算当前会话token数
   */
  estimateTokens() {
    return estimateSessionTokens(this.session.messages);
  }
  
  /**
   * 检查是否需要压缩
   */
  shouldCompact() {
    // 检查是否已经有压缩摘要
    const hasCompactedSummary = this.session.messages.some(
      m => m.role === 'system' && m.content?.includes('<summary>')
    );
    
    // 有压缩摘要时，提高阈值（避免反复压缩）
    const threshold = hasCompactedSummary 
      ? this.config.maxTokens * 1.5 
      : this.config.maxTokens;
    
    return this.estimateTokens() >= threshold;
  }
  
  /**
   * 获取会话状态
   */
  getStatus() {
    const tokens = this.estimateTokens();
    const messageCount = this.session.messages.length;
    const compactionCount = this.session.compactionCount || 0;
    const needsCompact = this.shouldCompact();
    
    return {
      tokens,
      messageCount,
      compactionCount,
      needsCompact,
      threshold: this.config.maxTokens,
      utilizationPercent: Math.round((tokens / this.config.maxTokens) * 100)
    };
  }
  
  /**
   * 执行压缩
   */
  compact() {
    if (!this.shouldCompact()) {
      return { success: false, reason: 'not_needed' };
    }
    
    const messages = this.session.messages;
    
    // 查找现有的压缩摘要
    let existingSummary = null;
    let summaryIndex = -1;
    
    for (let i = 0; i < messages.length; i++) {
      if (messages[i].role === 'system' && messages[i].content?.includes('<summary>')) {
        existingSummary = messages[i].content;
        summaryIndex = i;
        break;
      }
    }
    
    // 确定要压缩的范围
    const preserveRecent = this.config.preserveRecent;
    const keepFrom = messages.length - preserveRecent;
    
    // 收集要压缩的消息
    const toCompact = existingSummary
      ? messages.slice(0, summaryIndex)
      : messages.slice(0, keepFrom);
    
    const toPreserve = messages.slice(keepFrom);
    
    if (toCompact.length === 0) {
      return { success: false, reason: 'nothing_to_compact' };
    }
    
    // 生成新的压缩摘要
    let newSummary;
    if (existingSummary) {
      // 增量压缩：合并摘要
      const previousContent = extractPreviousSummary(existingSummary);
      newSummary = `<summary>\n${previousContent}\n\n### 新压缩 (${new Date().toLocaleString('zh-CN')})\n${generateSummary(toCompact, this.config)}`;
    } else {
      // 首次压缩
      newSummary = generateSummary(toCompact, this.config, existingSummary);
    }
    
    // 构建新的消息列表
    const newMessages = [
      {
        role: 'system',
        content: `<summary>\n${newSummary}\n\n### 最近消息（未压缩）\n---\n</summary>`,
        timestamp: new Date().toISOString()
      },
      ...toPreserve
    ];
    
    // 更新会话
    const removedCount = toCompact.length;
    this.session.messages = newMessages;
    this.session.compactionCount = (this.session.compactionCount || 0) + 1;
    this.session.totalTokens = estimateSessionTokens(newMessages);
    this._saveSession();
    
    return {
      success: true,
      removedCount,
      preservedCount: preserveRecent,
      newTotalTokens: this.session.totalTokens,
      compactionCount: this.session.compactionCount
    };
  }
  
  /**
   * 添加消息到会话
   */
  addMessage(role, content, metadata = {}) {
    this.session.messages.push({
      role,
      content,
      timestamp: new Date().toISOString(),
      ...metadata
    });
    this.session.totalTokens = this.estimateTokens();
    this._saveSession();
  }
  
  /**
   * 获取最近N条消息
   */
  getRecentMessages(count = 10) {
    return this.session.messages.slice(-count);
  }
  
  /**
   * 获取完整会话
   */
  getSession() {
    return this.session;
  }
}

// ============ CLI 界面 ============

function printStatus(compactor) {
  const status = compactor.getStatus();
  console.log('\n📊 会话状态');
  console.log('─'.repeat(40));
  console.log(`消息数:     ${status.messageCount}`);
  console.log(`Token估算:  ${status.tokens.toLocaleString()} / ${status.threshold.toLocaleString()}`);
  console.log(`利用率:     ${status.utilizationPercent}%`);
  console.log(`压缩次数:   ${status.compactionCount}`);
  console.log(`需要压缩:   ${status.needsCompact ? '⚠️ 是' : '✅ 否'}`);
  console.log('─'.repeat(40));
}

function runCLI(args) {
  const compactor = new SessionCompactor();
  
  if (args[0] === 'status') {
    printStatus(compactor);
    return;
  }
  
  if (args[0] === 'run' || args[0] === 'compact') {
    console.log('🔍 检查压缩需求...');
    
    if (!compactor.shouldCompact() && !args.includes('--force')) {
      console.log('✅ 会话长度正常，无需压缩');
      printStatus(compactor);
      return;
    }
    
    console.log('⚙️  执行压缩...');
    const result = compactor.compact();
    
    if (result.success) {
      console.log(`\n✅ 压缩完成!`);
      console.log(`   删除了 ${result.removedCount} 条消息`);
      console.log(`   保留了 ${result.preservedCount} 条最近消息`);
      console.log(`   压缩后约 ${result.newTotalTokens.toLocaleString()} tokens`);
      console.log(`   累计压缩次数: ${result.compactionCount}`);
    } else {
      console.log(`❌ 压缩失败: ${result.reason}`);
    }
    return;
  }
  
  if (args[0] === 'history') {
    console.log('\n📜 压缩历史');
    console.log('─'.repeat(40));
    const count = compactor.session.compactionCount || 0;
    console.log(`累计压缩次数: ${count}`);
    
    const summaryMsg = compactor.session.messages.find(
      m => m.role === 'system' && m.content?.includes('<summary>')
    );
    if (summaryMsg) {
      console.log('\n📋 当前摘要预览:');
      console.log(summaryMsg.content.slice(0, 500) + '...');
    }
    return;
  }
  
  // 默认：显示状态
  printStatus(compactor);
  console.log('\n用法:');
  console.log('  node compact.mjs status     # 查看状态');
  console.log('  node compact.mjs compact    # 执行压缩');
  console.log('  node compact.mjs history    # 查看历史');
}

// 导出模块
export { SessionCompactor, estimateSessionTokens, estimateMessageTokens };

// CLI 入口（仅在直接运行时执行）
const isMain = import.meta.url === pathToFileURL(process.argv[1]).href;
if (isMain) {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h')) {
    console.log('Session Compactor - 上下文压缩工具');
    console.log('');
    console.log('用法:');
    console.log('  node compact.mjs [command]');
    console.log('');
    console.log('命令:');
    console.log('  status   查看当前会话状态');
    console.log('  compact  执行压缩（必要时）');
    console.log('  history  查看压缩历史');
    console.log('');
    console.log('选项:');
    console.log('  --force  强制压缩');
    console.log('  --help   显示帮助');
  } else {
    runCLI(args);
  }
}
