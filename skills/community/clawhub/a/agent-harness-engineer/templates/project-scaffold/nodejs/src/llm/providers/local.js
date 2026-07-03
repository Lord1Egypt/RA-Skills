/**
 * ============================================
 * 类型: 核心框架
 * 模块: llm.providers.local
 * 说明: 本地模型客户端实现（兼容OpenAI API）
 * 修改建议: 如需扩展，继承LocalClient并覆盖方法
 * ============================================

const axios = require('axios');
const { LLMClient, LLMResponse } = require('../client');

class LocalClient extends LLMClient {
  constructor(config) {
    super(config);
    this.baseUrl = config.baseUrl || 'http://localhost:11434';
  }
  
  async chat(messages, tools) {
    const payload = {
      model: this.model,
      messages: messages.map(msg => ({
        role: msg.role,
        content: msg.content
      })),
      max_tokens: this.maxTokens,
      temperature: this.temperature
    };
    
    const response = await axios.post(
      `${this.baseUrl}/v1/chat/completions`,
      payload
    );
    
    const data = response.data;
    const message = data.choices[0].message;
    
    return new LLMResponse(
      message.content || '',
      [],
      data.usage || {},
      this.model
    );
  }
  
  validateConfig() {
    return !!this.config.baseUrl;
  }
}

module.exports = { LocalClient };
