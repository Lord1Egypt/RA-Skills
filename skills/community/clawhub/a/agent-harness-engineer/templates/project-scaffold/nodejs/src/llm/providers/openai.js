/**
 * ============================================
 * 类型: 核心框架
 * 模块: llm.providers.openai
 * 说明: OpenAI GPT客户端实现
 * 修改建议: 如需扩展，继承OpenAIClient并覆盖方法
 * ============================================

const OpenAI = require('openai');
const { LLMClient, ToolCall, LLMResponse } = require('../client');

class OpenAIClient extends LLMClient {
  constructor(config) {
    super(config);
    this.client = new OpenAI({
      apiKey: config.apiKey,
      baseURL: config.baseUrl
    });
  }
  
  async chat(messages, tools) {
    const openaiMessages = messages.map(msg => ({
      role: msg.role,
      content: msg.content
    }));
    
    const response = await this.client.chat.completions.create({
      model: this.model,
      max_tokens: this.maxTokens,
      temperature: this.temperature,
      messages: openaiMessages,
      tools: tools || []
    });
    
    const message = response.choices[0].message;
    const content = message.content || '';
    const toolCalls = [];
    
    if (message.tool_calls) {
      for (const tc of message.tool_calls) {
        toolCalls.push(new ToolCall(
          tc.id,
          tc.function.name,
          JSON.parse(tc.function.arguments)
        ));
      }
    }
    
    return new LLMResponse(
      content,
      toolCalls,
      {
        promptTokens: response.usage.prompt_tokens,
        completionTokens: response.usage.completion_tokens
      },
      response.model
    );
  }
  
  validateConfig() {
    return !!this.config.apiKey;
  }
}

module.exports = { OpenAIClient };
