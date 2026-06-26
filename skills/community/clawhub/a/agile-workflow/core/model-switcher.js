#!/usr/bin/env node
/**
 * 模型切换器 v7.18
 * 
 * 核心功能:
 * 1. 根据 Token 数自动选择模型
 * 2. 超限自动分片
 * 3. 成本优化建议
 */

const TokenCounter = require('./token-counter');
const AutoChunker = require('./auto-chunker');

// 🔌 FileManager 约束注入器集成
let ModelConstraintInjector;
try {
  const injectorPath = require('path').join(process.cwd(), 'skills/file-manager/core/model-constraint-injector.js');
  ModelConstraintInjector = require(injectorPath).ModelConstraintInjector;
} catch (e) {
  console.warn('⚠️ ModelConstraintInjector 未找到，约束注入可能不可用:', e.message);
  ModelConstraintInjector = null;
}

class ModelSwitcher {
  constructor(config = {}) {
    // ✅ 真实数据来自 /home/ubutu/.openclaw/openclaw.json
    // 更新时间：2026-03-13
    this.models = config.models || {
      'economy': { 
        name: 'qwen3.5-plus', 
        limit: 800000,  // ✅ 官方：1M context，保留 20% 余量
        cost: '低',
        description: '经济型，context 1M',
        source: 'official',
        contextWindow: 1000000
      },
      'standard': { 
        name: 'deepseek-chat', 
        limit: 160000,  // ✅ 官方：200K context，保留 20% 余量
        cost: '中',
        description: '标准型，context 200K',
        source: 'official',
        contextWindow: 200000
      },
      'premium': { 
        name: 'qwen3-max-2026-01-23', 
        limit: 200000,  // ✅ 官方：262K context，保留 20% 余量
        cost: '高',
        description: '高级型，context 262K',
        source: 'official',
        contextWindow: 262144
      }
    };
    this.counter = new TokenCounter();
    this.chunker = new AutoChunker();
    
    // 🔌 初始化约束注入器
    if (ModelConstraintInjector) {
      this.constraintInjector = new ModelConstraintInjector({
        workspace: config.workspace || '/home/ubutu/.openclaw/workspace'
      });
      console.log('✅ ModelConstraintInjector 已初始化');
    } else {
      this.constraintInjector = null;
    }
  }

  /**
   * 根据 Token 数选择模型
   */
  selectModel(tokenCount) {
    const safetyMargin = 0.8;  // 保留 20% 余量
    
    for (const [tier, model] of Object.entries(this.models)) {
      if (tokenCount < model.limit * safetyMargin) {
        return {
          tier,
          ...model,
          needChunk: false
        };
      }
    }
    
    // 超过最大模型，需要分片
    return {
      tier: 'chunked',
      name: 'auto-chunk',
      limit: this.chunker.maxTokenPerChunk,
      needChunk: true,
      description: '自动分片模式'
    };
  }

  /**
   * 自动选择并调用（带约束注入）
   */
  async autoCall(messages, callFunc, options = {}) {
    const tokenCount = this.counter.calculateMessageToken(messages);
    const model = this.selectModel(tokenCount);
    
    console.log(`📊 Token 计数：${tokenCount}`);
    console.log(`🤖 选择模型：${model.name} (${model.tier})`);
    console.log(`📝 说明：${model.description}`);
    
    // 🔌 注入约束（如果可用）
    let injectedMessages = messages;
    if (this.constraintInjector && options.agentType) {
      console.log(`🔒 正在注入约束: agentType=${options.agentType}, model=${model.name}`);
      
      // 在 system message 中注入约束
      const systemMessage = messages.find(m => m.role === 'system');
      if (systemMessage) {
        const originalPrompt = systemMessage.content;
        const injectedPrompt = this.constraintInjector.injectConstraints(originalPrompt, {
          agentType: options.agentType,
          model: model.name,
          includeFileManager: true
        });
        systemMessage.content = injectedPrompt;
        console.log(`✅ 约束已注入到 System Prompt`);
      }
    }
    
    if (model.needChunk) {
      // 需要分片
      console.log(`⚠️ Token 超限，启用自动分片`);
      return await this.chunker.smartProcess(injectedMessages, callFunc, options);
    }
    
    // 直接调用
    console.log(`✅ 直接调用 ${model.name}（带约束）`);
    return await callFunc(injectedMessages, model);
  }

  /**
   * 切换模型并注入约束
   * @param {string} model - 目标模型
   * @param {object} agent - Agent 实例
   * @param {object} tools - 工具列表
   */
  async switchModelWithConstraints(model, agent, tools = {}) {
    if (!this.constraintInjector) {
      console.warn('⚠️ ModelConstraintInjector 不可用，使用基础切换');
      return { model, systemPrompt: agent.systemPrompt, tools };
    }
    
    console.log(`🔄 切换模型：${model}`);
    return await this.constraintInjector.switchModelWithConstraints(model, agent, tools);
  }

  /**
   * 获取成本估算
   */
  getCostEstimate(tokenCount) {
    const model = this.selectModel(tokenCount);
    
    // 简化成本估算（实际价格需查询 API）
    const costPer1K = {
      'economy': 0.002,
      'standard': 0.01,
      'premium': 0.05
    };
    
    const cost = (tokenCount / 1000) * (costPer1K[model.tier] || 0.01);
    
    return {
      model: model.name,
      tier: model.tier,
      token: tokenCount,
      estimatedCost: cost.toFixed(4),
      currency: 'USD'
    };
  }

  /**
   * 优化建议
   */
  getOptimizationAdvice(messages) {
    const tokenCount = this.counter.calculateMessageToken(messages);
    const model = this.selectModel(tokenCount);
    const advice = [];
    
    if (model.needChunk) {
      advice.push({
        type: 'chunk',
        priority: 'high',
        message: 'Token 数过大，已自动启用分片处理'
      });
    }
    
    if (model.tier === 'premium') {
      advice.push({
        type: 'summarize',
        priority: 'medium',
        message: '使用高级模型，建议摘要历史对话以降低成本'
      });
    }
    
    if (model.tier === 'economy' && tokenCount < 10000) {
      advice.push({
        type: 'batch',
        priority: 'low',
        message: 'Token 数较小，可批量处理多个任务以节省成本'
      });
    }
    
    return {
      token: tokenCount,
      model: model.name,
      advice
    };
  }
}

module.exports = ModelSwitcher;

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const [command, tokenCount] = args;
  
  if (!command) {
    console.log('用法：node model-switcher.js <命令> [token 数]');
    console.log('命令：select, cost, advice');
    process.exit(1);
  }
  
  const switcher = new ModelSwitcher();
  
  if (command === 'select') {
    const tokens = parseInt(tokenCount) || 50000;
    const model = switcher.selectModel(tokens);
    console.log(`Token 数：${tokens}`);
    console.log(`推荐模型：${model.name} (${model.tier})`);
    console.log(`说明：${model.description}`);
  }
  
  if (command === 'cost') {
    const tokens = parseInt(tokenCount) || 50000;
    const cost = switcher.getCostEstimate(tokens);
    console.log(`Token 数：${cost.token}`);
    console.log(`模型：${cost.model}`);
    console.log(`预估成本：$${cost.estimatedCost}`);
  }
  
  if (command === 'advice') {
    const messages = [{ content: '测试消息'.repeat(1000) }];
    const advice = switcher.getOptimizationAdvice(messages);
    console.log(`Token 数：${advice.token}`);
    console.log(`模型：${advice.model}`);
    console.log(`优化建议:`);
    advice.advice.forEach(a => {
      console.log(`  [${a.priority}] ${a.message}`);
    });
  }
}
