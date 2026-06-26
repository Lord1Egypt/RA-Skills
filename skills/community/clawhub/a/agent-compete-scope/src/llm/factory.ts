// src/llm/factory.ts
import { LLMProvider } from './types';
import { AnthropicAdapter } from './anthropic';
import { GeminiAdapter } from './gemini';
import { GroqAdapter } from './groq';

export class LLMFactory {
  static create(provider?: string): LLMProvider {
    const p = (provider || process.env.LLM_PROVIDER || 'groq').toLowerCase();

    switch (p) {
      case 'anthropic':
        return new AnthropicAdapter({ apiKey: process.env.ANTHROPIC_API_KEY });
      case 'gemini':
      case 'google':
        return new GeminiAdapter({ 
          apiKey: process.env.GOOGLE_API_KEY, 
          model: 'gemini-1.5-flash-latest' 
        });
      case 'groq':
        return new GroqAdapter({ 
          apiKey: process.env.GROQ_API_KEY,
          model: 'llama-3.3-70b-versatile'
        });
      default:
        console.warn(`[LLMFactory] Unknown provider "${p}", falling back to Groq.`);
        return new GroqAdapter({ apiKey: process.env.GROQ_API_KEY });
    }
  }
}
