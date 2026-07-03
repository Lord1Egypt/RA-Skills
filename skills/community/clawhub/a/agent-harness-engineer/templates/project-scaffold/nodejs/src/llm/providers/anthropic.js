/**
 * ============================================
 * 类型: 核心框架
 * 模块: llm.providers.anthropic
 * 说明: Anthropic Claude客户端实现
 * 修改建议: 如需扩展，继承AnthropicClient并覆盖方法
 * ============================================

const Anthropic = require('@anthropic-ai/sdk');
const { LLMClient, ToolCall, LLMResponse } = require('../client');

class AnthropicClient extends LLMClient {
  constructor(config) {
    super(config);
    this.client = new Anthropic({
      apiKey: config.apiKey,
      baseURL: config.baseUrl
    });
  }
  
  async chat(messages, tools) {
    const anthropicMessages = messages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));
    
    const response = await this.client.messages.create({
      model: this.model,
      max_tokens: this.maxTokens,
      temperature: this.temperature,
      messages: anthropicMessages,
      tools: tools || []
    });
    
    let content = '';
    const toolCalls = [];
    
    for (const block of response.content) {
      if (block.type === 'text') {
        content += block.text;
      } else if (block.type === 'tool_use') {
        toolCalls.push(new ToolCall(
          block.id,
          block.name,
          block.input
        ));
      }
    }
    
    return new LLMResponse(
      content,
      toolCalls,
      {
        promptTokens: response.usage.input_tokens,
        completionTokens: response.usage.output_tokens
      },
      response.model
    );
  }
  
  validateConfig() {
    return !!this.config.apiKey;
  }
}

module.exports = { AnthropicClient };
