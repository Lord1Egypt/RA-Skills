#!/usr/bin/env node

/**
 * Provider 和 Prompt 缓存配置更新脚本
 * 
 * 使用方法：node update-providers-config.js
 */

const fs = require('fs');
const path = require('path');

const configPath = path.join(__dirname, '../../../openclaw.json');

console.log('📝 读取配置文件...');
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

console.log('➕ 添加新 Providers...');

// 添加 Anthropic Provider
config.models.providers.anthropic = {
  baseUrl: 'https://api.anthropic.com/v1',
  apiKey: '${ANTHROPIC_API_KEY}',
  api: 'anthropic-completions',
  models: [
    {
      id: 'claude-sonnet-4-20250514',
      name: 'Claude Sonnet 4',
      reasoning: false,
      input: ['text', 'image'],
      cost: { input: 0.003, output: 0.015, cacheRead: 0.0003, cacheWrite: 0.003 },
      contextWindow: 200000,
      maxTokens: 65536
    },
    {
      id: 'claude-opus-4-20250514',
      name: 'Claude Opus 4',
      reasoning: false,
      input: ['text', 'image'],
      cost: { input: 0.015, output: 0.075, cacheRead: 0.0015, cacheWrite: 0.015 },
      contextWindow: 200000,
      maxTokens: 65536
    }
  ]
};

// 添加 OpenAI Provider
config.models.providers.openai = {
  baseUrl: 'https://api.openai.com/v1',
  apiKey: '${OPENAI_API_KEY}',
  api: 'openai-completions',
  models: [
    {
      id: 'gpt-4o',
      name: 'GPT-4o',
      reasoning: false,
      input: ['text', 'image'],
      cost: { input: 0.005, output: 0.015, cacheRead: 0.0005, cacheWrite: 0.005 },
      contextWindow: 128000,
      maxTokens: 16384
    },
    {
      id: 'gpt-4o-mini',
      name: 'GPT-4o Mini',
      reasoning: false,
      input: ['text', 'image'],
      cost: { input: 0.00015, output: 0.0006, cacheRead: 0.000015, cacheWrite: 0.00015 },
      contextWindow: 128000,
      maxTokens: 16384
    }
  ]
};

// 添加 DeepSeek Provider
config.models.providers.deepseek = {
  baseUrl: 'https://api.deepseek.com/v1',
  apiKey: '${DEEPSEEK_API_KEY}',
  api: 'openai-completions',
  models: [
    {
      id: 'deepseek-chat',
      name: 'DeepSeek Chat',
      reasoning: false,
      input: ['text'],
      cost: { input: 0.00027, output: 0.0011, cacheRead: 0.000027, cacheWrite: 0.00027 },
      contextWindow: 128000,
      maxTokens: 65536
    },
    {
      id: 'deepseek-coder',
      name: 'DeepSeek Coder',
      reasoning: false,
      input: ['text'],
      cost: { input: 0.00027, output: 0.0011, cacheRead: 0.000027, cacheWrite: 0.00027 },
      contextWindow: 128000,
      maxTokens: 65536
    }
  ]
};

console.log('🔄 更新现有 Provider 缓存配置...');

// 更新 modelstudio 缓存配置
config.models.providers.modelstudio.models.forEach(model => {
  if (!model.cost.cacheRead) {
    model.cost.cacheRead = model.cost.input * 0.1;
    model.cost.cacheWrite = model.cost.input * 0.5;
  }
});

// 更新 bailian 缓存配置
config.models.providers.bailian.models.forEach(model => {
  if (!model.cost.cacheRead) {
    model.cost.cacheRead = model.cost.input * 0.1;
    model.cost.cacheWrite = model.cost.input * 0.5;
  }
});

console.log('🔗 更新 Fallback 链...');

// 更新默认 fallback 链
config.agents.defaults.model.fallbacks = [
  'modelstudio/qwen3.5-plus',
  'deepseek/deepseek-chat',
  'bailian/qwen3.5-plus',
  'anthropic/claude-sonnet-4-20250514',
  'openai/gpt-4o-mini'
];

console.log('💾 保存配置文件...');
fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

console.log('✅ 配置更新完成！');
console.log('');
console.log('📊 新增 Provider:');
console.log('   - Anthropic (2 models)');
console.log('   - OpenAI (2 models)');
console.log('   - DeepSeek (2 models)');
console.log('');
console.log('🔗 新 Fallback 链:');
console.log('   1. modelstudio/qwen3.5-plus');
console.log('   2. deepseek/deepseek-chat');
console.log('   3. bailian/qwen3.5-plus');
console.log('   4. anthropic/claude-sonnet-4');
console.log('   5. openai/gpt-4o-mini');
console.log('');
console.log('⚠️  注意：请设置以下环境变量:');
console.log('   - ANTHROPIC_API_KEY');
console.log('   - OPENAI_API_KEY');
console.log('   - DEEPSEEK_API_KEY');
