#!/usr/bin/env node
/**
 * Agent Runtime - 智能体运行时系统（简化版）
 * 整合工具注册、权限控制、Hook拦截、上下文压缩、Usage追踪
 */

import { fileURLToPath } from 'url';
import { pathToFileURL } from 'url';
import path from 'path';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ============ 常量 ============

const AgentType = {
  EXPLORE: 'explore',
  PLAN: 'plan',
  VERIFICATION: 'verify',
  GENERAL: 'general'
};

const PermissionLevel = {
  READ: 'read',
  WRITE: 'write',
  DANGER: 'danger',
  ADMIN: 'admin'
};

// ============ Token 估算 ============

function estimateTokens(text) {
  if (!text || typeof text !== 'string') return 0;
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const otherChars = text.length - chineseChars;
  return chineseChars + Math.ceil(otherChars / 4);
}

// ============ 工具注册表（简化版）============

class SimpleToolRegistry {
  constructor() {
    this.tools = new Map();
    this.nameIndex = new Map();
  }

  register(config) {
    this.tools.set(config.name, config);
    this.nameIndex.set(config.name.toLowerCase(), config);
    for (const alias of config.aliases || []) {
      this.nameIndex.set(alias.toLowerCase(), config);
    }
  }

  get(name) {
    return this.nameIndex.get(name.toLowerCase());
  }

  search(input, options = {}) {
    const tokens = (input || '').toLowerCase().split(/\s+/).filter(t => t.length > 0);
    if (tokens.length === 0) return [];

    const matches = [];
    const seen = new Set();

    for (const [name, tool] of this.tools) {
      if (seen.has(name)) continue;

      let score = 0;
      const nameLower = name.toLowerCase();
      const descLower = (tool.description || '').toLowerCase();
      const keywordsLower = (tool.keywords || []).map(k => k.toLowerCase());

      for (const token of tokens) {
        if (keywordsLower.some(k => k.includes(token) || token.includes(k))) score += 2;
        else if (nameLower.includes(token)) score += 1.5;
        else if (descLower.includes(token)) score += 0.5;
      }

      if (score > 0) {
        matches.push({ tool, score, matchType: 'keyword' });
        seen.add(name);
      }
    }

    return matches.sort((a, b) => b.score - a.score);
  }

  list() {
    return Array.from(this.tools.values());
  }
}

// ============ Usage Tracker（简化版）============

class SimpleUsageTracker {
  constructor(config = {}) {
    this.maxTotalTokens = config.maxTotalTokens || 100000;
    this.maxTurns = config.maxTurns || 50;
    this.totalInput = 0;
    this.totalOutput = 0;
    this.turnCount = 0;
  }

  record(inputTokens, outputTokens) {
    this.totalInput += inputTokens;
    this.totalOutput += outputTokens;
    this.turnCount++;
    return this.getStats();
  }

  getStats() {
    const total = this.totalInput + this.totalOutput;
    return {
      totalInputTokens: this.totalInput,
      totalOutputTokens: this.totalOutput,
      totalTokens: total,
      turnCount: this.turnCount,
      budgetUsedPercent: (total / this.maxTotalTokens) * 100
    };
  }

  checkBudget() {
    const total = this.totalInput + this.totalOutput;
    return {
      exceeded: total >= this.maxTotalTokens || this.turnCount >= this.maxTurns,
      totalPercent: total / this.maxTotalTokens
    };
  }
}

// ============ Hook Runner（简化版）============

class SimpleHookRunner {
  constructor(config = {}) {
    this.preHooks = config.preToolUse || [];
    this.postHooks = config.postToolUse || [];
  }

  async runPreToolUse(toolName, input) {
    // 简化实现：直接允许
    return { allowed: true, denied: false, messages: [] };
  }

  async runPostToolUse(toolName, input, output, isError) {
    return { allowed: true, denied: false, messages: [] };
  }
}

// ============ Session Compactor（简化版）============

class SimpleSessionCompactor {
  constructor(config = {}) {
    this.maxTokens = config.maxTokens || 80000;
    this.preserveRecent = config.preserveRecent || 4;
    this.messages = [];
    this.compactionCount = 0;
  }

  addMessage(role, content) {
    this.messages.push({ role, content, timestamp: new Date().toISOString() });
  }

  shouldCompact() {
    const totalTokens = this.messages.reduce((sum, m) => sum + estimateTokens(m.content || ''), 0);
    return totalTokens > this.maxTokens * 0.8;
  }

  compact() {
    // 简化实现：只保留最近的N条
    this.messages = this.messages.slice(-this.preserveRecent);
    this.compactionCount++;
  }

  getStatus() {
    const tokens = this.messages.reduce((sum, m) => sum + estimateTokens(m.content || ''), 0);
    return {
      messageCount: this.messages.length,
      tokens,
      compactionCount: this.compactionCount,
      needsCompact: this.shouldCompact()
    };
  }
}

// ============ Agent Runtime ============

class AgentRuntime {
  constructor(config = {}) {
    this.config = {
      agentType: config.agentType || AgentType.GENERAL,
      maxTokens: config.maxTokens || 100000,
      maxTurns: config.maxTurns || 50,
      ...config
    };

    // 初始化组件
    this.registry = new SimpleToolRegistry();
    this.usageTracker = new SimpleUsageTracker({
      maxTotalTokens: this.config.maxTokens,
      maxTurns: this.config.maxTurns
    });
    this.hookRunner = new SimpleHookRunner();
    this.compactor = new SimpleSessionCompactor({
      maxTokens: this.config.maxTokens
    });

    this.messages = [];
    this.turnCount = 0;

    // 注册内置工具
    this._registerBuiltinTools();
  }

  _registerBuiltinTools() {
    this.registry.register({
      name: 'read_file',
      aliases: ['read', 'cat'],
      description: '读取文件内容',
      permission: 'read',
      agentTypes: ['explore', 'plan', 'general'],
      keywords: ['file', 'read', '读取', '文件', '内容'],
      execute: async (ctx, input) => {
        const filePath = typeof input === 'string' ? input : input.path;
        if (!filePath) return { error: 'path required' };
        try {
          const content = fs.readFileSync(filePath, 'utf-8');
          return { success: true, content, size: content.length };
        } catch (e) {
          return { success: false, error: e.message };
        }
      }
    });

    this.registry.register({
      name: 'bash',
      aliases: ['shell', 'exec'],
      description: '执行Shell命令',
      permission: 'danger',
      agentTypes: ['verification', 'general'],
      keywords: ['bash', 'shell', '命令', '执行', '终端'],
      execute: async (ctx, input) => {
        const { spawn } = await import('child_process');
        const command = typeof input === 'string' ? input : input.command;
        if (!command) return { error: 'command required' };

        return new Promise((resolve) => {
          const child = spawn('cmd', ['/C', command], { shell: true });
          let stdout = '', stderr = '';
          child.stdout.on('data', d => stdout += d);
          child.stderr.on('data', d => stderr += d);
          child.on('close', code => resolve({
            command,
            exitCode: code,
            stdout,
            stderr,
            success: code === 0
          }));
        });
      }
    });

    this.registry.register({
      name: 'search',
      aliases: ['find', 'grep'],
      description: '搜索文件内容',
      permission: 'read',
      agentTypes: ['explore', 'plan'],
      keywords: ['search', 'find', 'grep', '搜索', '查找'],
      execute: async (ctx, input) => {
        const pattern = typeof input === 'string' ? input : input.pattern;
        return { success: true, message: `Searching for: ${pattern}`, pattern };
      }
    });

    this.registry.register({
      name: 'todo',
      aliases: ['task', 'checklist'],
      description: '待办事项管理',
      permission: 'write',
      agentTypes: ['plan', 'general'],
      keywords: ['todo', 'task', '待办', '任务'],
      execute: async (ctx, input) => {
        return { success: true, message: 'Todo updated', input };
      }
    });
  }

  /**
   * 运行单轮对话
   */
  async runTurn(userMessage) {
    this.turnCount++;

    // 记录消息
    this.messages.push({ role: 'user', content: userMessage });
    this.compactor.addMessage('user', userMessage);

    // 估算输入 token
    const inputTokens = estimateTokens(userMessage);

    // 搜索匹配的工具
    const matches = this.registry.search(userMessage);

    let output = '';
    let toolResults = [];

    // 执行匹配的工具
    for (const match of matches.slice(0, 3)) {
      const tool = match.tool;

      // Pre Hook
      const preResult = await this.hookRunner.runPreToolUse(tool.name, {});
      if (preResult.denied) {
        output += `\n[${tool.name}] blocked by hook\n`;
        continue;
      }

      // 执行
      const result = await tool.execute({}, {});

      // Post Hook
      await this.hookRunner.runPostToolUse(tool.name, {}, result, !result.success);

      toolResults.push({ tool: tool.name, result });
      output += `\n[${tool.name}]: ${JSON.stringify(result)}\n`;
    }

    // 如果没有工具匹配，生成响应
    if (toolResults.length === 0) {
      output = `我收到了: ${userMessage}\n\n根据你的请求，我找到了以下可能的操作:\n`;
      if (matches.length > 0) {
        output += matches.slice(0, 5).map(m =>
          `- ${m.tool.name}: ${m.tool.description} (得分: ${m.score})`
        ).join('\n');
      } else {
        output += '(没有找到匹配的工具)';
      }
    }

    // 记录助手消息
    this.messages.push({ role: 'assistant', content: output });
    this.compactor.addMessage('assistant', output);

    // 记录 usage
    const outputTokens = estimateTokens(output);
    const usage = this.usageTracker.record(inputTokens, outputTokens);

    // 检查压缩
    if (this.compactor.shouldCompact()) {
      this.compactor.compact();
    }

    return {
      output,
      matches: matches.slice(0, 5).map(m => ({
        name: m.tool.name,
        score: m.score,
        description: m.tool.description
      })),
      toolResults,
      usage,
      turnCount: this.turnCount
    };
  }

  /**
   * 获取状态
   */
  getStatus() {
    return {
      agentType: this.config.agentType,
      turnCount: this.turnCount,
      messageCount: this.messages.length,
      usage: this.usageTracker.getStats(),
      compactStatus: this.compactor.getStatus(),
      toolCount: this.registry.list().length
    };
  }

  /**
   * 重置
   */
  reset() {
    this.messages = [];
    this.turnCount = 0;
    this.compactor = new SimpleSessionCompactor({ maxTokens: this.config.maxTokens });
    this.usageTracker = new SimpleUsageTracker({
      maxTotalTokens: this.config.maxTokens,
      maxTurns: this.config.maxTurns
    });
  }
}

// ============ 导出 ============

export { AgentRuntime, AgentType, PermissionLevel };

// ============ CLI ============

function printHelp() {
  console.log(`
Agent Runtime - 智能体运行时系统
================================

用法:
  node agent-runtime.mjs <command> [options]

命令:
  status            显示运行时状态
  tools             列出可用工具
  search <query>    搜索工具
  run <message>     运行单轮对话
  reset             重置运行时

示例:
  node agent-runtime.mjs status
  node agent-runtime.mjs search "读文件"
  node agent-runtime.mjs run "读取 README.md"
`);
}

async function main(args) {
  const runtime = new AgentRuntime();

  const cmd = args[0];

  if (cmd === 'status') {
    const status = runtime.getStatus();
    console.log('\n📊 Agent Runtime 状态\n');
    console.log(`  代理类型: ${status.agentType}`);
    console.log(`  对话轮次: ${status.turnCount}`);
    console.log(`  消息数量: ${status.messageCount}`);
    console.log(`  工具数量: ${status.toolCount}`);
    console.log(`\n  Token 使用:`);
    console.log(`    输入: ${status.usage.totalInputTokens}`);
    console.log(`    输出: ${status.usage.totalOutputTokens}`);
    console.log(`    总计: ${status.usage.totalTokens}`);
    console.log(`    预算使用: ${status.usage.budgetUsedPercent.toFixed(2)}%`);
    console.log(`\n  压缩状态:`);
    console.log(`    消息数: ${status.compactStatus.messageCount}`);
    console.log(`    压缩次数: ${status.compactStatus.compactionCount}`);
    return 0;
  }

  if (cmd === 'tools') {
    const tools = runtime.registry.list();
    console.log(`\n可用工具 (${tools.length}):\n`);
    for (const tool of tools) {
      console.log(`  ${tool.name}`);
      console.log(`    ${tool.description}`);
      console.log(`    权限: ${tool.permission} | 代理: ${tool.agentTypes.join(', ')}`);
      console.log();
    }
    return 0;
  }

  if (cmd === 'search') {
    const query = args.slice(1).join(' ');
    if (!query) {
      console.log('请提供搜索关键词');
      return 1;
    }
    const matches = runtime.registry.search(query);
    console.log(`\n搜索 "${query}" 的结果:\n`);
    if (matches.length === 0) {
      console.log('  无匹配结果');
    }
    for (const match of matches) {
      console.log(`  ${match.tool.name} (得分: ${match.score})`);
      console.log(`    ${match.tool.description}`);
      console.log();
    }
    return 0;
  }

  if (cmd === 'run') {
    const message = args.slice(1).join(' ');
    if (!message) {
      console.log('请提供要处理的消息');
      return 1;
    }
    console.log(`\n处理: "${message}"\n`);
    const result = await runtime.runTurn(message);
    console.log('输出:', result.output);
    console.log('\n匹配工具:', result.matches.map(m => m.name).join(', ') || '无');
    console.log('Token使用:', result.usage.totalTokens);
    return 0;
  }

  if (cmd === 'reset') {
    runtime.reset();
    console.log('✅ 运行时已重置');
    return 0;
  }

  printHelp();
  return 0;
}

// ============ CLI 入口 ============

const cliArgs = process.argv.slice(2);
if (cliArgs[0] === '--help' || cliArgs[0] === '-h') {
  printHelp();
} else {
  main(cliArgs).then(code => process.exit(code));
}
