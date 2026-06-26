// src/llm/anthropic.ts
import Anthropic from '@anthropic-ai/sdk';
import { LLMProvider, LLMConfig } from './types';

export class AnthropicAdapter implements LLMProvider {
  private client: Anthropic;
  private model: string;
  private maxTokens: number;

  constructor(config: LLMConfig) {
    if (!config.apiKey) {
      throw new Error('ANTHROPIC_API_KEY is required for Anthropic provider.');
    }
    this.client = new Anthropic({ apiKey: config.apiKey });
    this.model = config.model || 'claude-3-5-sonnet-20240620';
    this.maxTokens = config.maxTokens || 1024;
  }

  async call(systemPrompt: string, userMessage: string): Promise<string> {
    console.log(`[Anthropic] Calling ${this.model}...`);
    try {
      const response = await this.client.messages.create({
        model: this.model,
        max_tokens: this.maxTokens,
        system: systemPrompt,
        messages: [{ role: 'user', content: userMessage }],
      });

      const textBlock = response.content.find(block => block.type === 'text');
      if (!textBlock || textBlock.type !== 'text') {
        throw new Error('Anthropic response did not contain text.');
      }
      return textBlock.text;
    } catch (error) {
      console.error('[Anthropic] Call failed:', error);
      throw error;
    }
  }
}
