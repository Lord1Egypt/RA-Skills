// src/llm/gemini.ts
import { LLMProvider, LLMConfig } from './types';

export class GeminiAdapter implements LLMProvider {
  private apiKey: string;
  private modelName: string;

  constructor(config: LLMConfig) {
    if (!config.apiKey) {
      throw new Error('GOOGLE_API_KEY is required for Gemini provider.');
    }
    this.apiKey = config.apiKey;
    this.modelName = config.model || 'gemini-pro';
  }

  async call(systemPrompt: string, userMessage: string): Promise<string> {
    console.log(`[Gemini] Calling ${this.modelName} (REST API v1)...`);
    
    // v1 REST API 엔드포인트
    const url = `https://generativelanguage.googleapis.com/v1/models/${this.modelName}:generateContent?key=${this.apiKey}`;

    const payload = {
      contents: [{
        parts: [{ text: `${systemPrompt}\n\n${userMessage}` }]
      }],
      generationConfig: {
        maxOutputTokens: 1024,
      }
    };

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Gemini API Error: ${response.status} ${errorText}`);
      }

      const data = (await response.json()) as any;
      
      // 응답 파싱
      if (data.candidates && data.candidates.length > 0) {
        const text = data.candidates[0].content.parts[0].text;
        return text;
      } else {
        throw new Error('No candidates returned from Gemini API.');
      }

    } catch (error) {
      console.error('[Gemini] Call failed:', error);
      throw error;
    }
  }
}
