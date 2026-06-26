// src/llm/groq.ts
import OpenAI from 'openai';
import { LLMProvider, LLMConfig } from './types';

export class GroqAdapter implements LLMProvider {
  private client: OpenAI;
  private model: string;

  constructor(config: LLMConfig) {
    if (!config.apiKey) {
      throw new Error('GROQ_API_KEY is required for Groq provider.');
    }
    this.client = new OpenAI({
      apiKey: config.apiKey,
      baseURL: 'https://api.groq.com/openai/v1',
    });
    this.model = config.model || 'llama-3.3-70b-versatile';
  }

  async call(systemPrompt: string, userMessage: string): Promise<string> {
    console.log(`[Groq] Calling ${this.model}...`);
    try {
      const response = await this.client.chat.completions.create({
        model: this.model,
        messages: [
          { role: 'system', content: systemPrompt },
          { role: 'user', content: userMessage },
        ],
        temperature: 0.1, // 분석용이므로 낮은 온도 설정
      });

      const content = response.choices[0]?.message?.content;
      if (!content) {
        throw new Error('Groq response did not contain text.');
      }
      return content;
    } catch (error) {
      console.error('[Groq] Call failed:', error);
      throw error;
    }
  }
}
