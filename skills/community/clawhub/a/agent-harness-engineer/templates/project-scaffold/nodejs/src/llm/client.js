/**
 * ============================================
 * 类型: 核心框架
 * 模块: llm.client
 * 说明: LLM客户端抽象接口
 * 修改建议: 如需添加新供应商，继承LLMClient并实现抽象方法
 * ============================================

class LLMClient {
  constructor(config) {
    this.config = config;
    this.model = config.model;
    this.maxTokens = config.maxTokens || 4096;
    this.temperature = config.temperature || 0.7;
  }
  
  async chat(messages, tools) {
    throw new Error('Not implemented');
  }
  
  validateConfig() {
    return true;
  }
}

class Message {
  constructor(role, content) {
    this.role = role;
    this.content = content;
  }
}

class ToolCall {
  constructor(id, name, arguments) {
    this.id = id;
    this.name = name;
    this.arguments = arguments;
  }
}

class LLMResponse {
  constructor(content, toolCalls = [], usage = {}, model = '') {
    this.content = content;
    this.toolCalls = toolCalls;
    this.usage = usage;
    this.model = model;
  }
}

module.exports = { LLMClient, Message, ToolCall, LLMResponse };
