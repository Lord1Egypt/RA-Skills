/**
 * ============================================
 * 类型: 核心框架
 * 模块: llm.factory
 * 说明: LLM客户端工厂函数
 * 修改建议: 如需添加新供应商，在providers对象中添加
 * ============================================

const { AnthropicClient } = require('./providers/anthropic');
const { OpenAIClient } = require('./providers/openai');
const { LocalClient } = require('./providers/local');

function createLLMClient(config) {
  const provider = (config.provider || 'anthropic').toLowerCase();
  
  const providers = {
    anthropic: AnthropicClient,
    openai: OpenAIClient,
    azure: OpenAIClient,
    local: LocalClient
  };
  
  if (!providers[provider]) {
    throw new Error(`Unknown provider: ${provider}. Supported: ${Object.keys(providers).join(', ')}`);
  }
  
  const client = new providers[provider](config);
  
  if (!client.validateConfig()) {
    throw new Error(`Invalid configuration for provider: ${provider}`);
  }
  
  return client;
}

module.exports = { createLLMClient };
