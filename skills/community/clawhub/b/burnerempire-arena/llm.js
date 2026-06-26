// Arena Agent - LLM Decision Engine
// Calls OpenRouter for strategic game decisions with reasoning

import { appendFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import {
  OPENROUTER_API_KEY, OPENROUTER_BASE_URL,
  ARENA_LLM_MODEL, LLM_MAX_TOKENS, LLM_TEMPERATURE, LOGS_DIR,
} from './config.js';

const MAX_RETRIES = 2;
const RETRY_BACKOFF_MS = 1000;

export class LLMClient {
  constructor(model = ARENA_LLM_MODEL) {
    this.model = model;
    this.totalCalls = 0;
    this.totalTokens = 0;
  }

  async decide(systemPrompt, userPrompt, options = {}) {
    if (!OPENROUTER_API_KEY) {
      return { action: null, reasoning: 'LLM not configured (no API key)', fallback: true };
    }

    const messages = [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userPrompt },
    ];

    const body = {
      model: this.model,
      messages,
      max_tokens: options.max_tokens || LLM_MAX_TOKENS,
      temperature: options.temperature ?? LLM_TEMPERATURE,
      response_format: { type: 'json_object' },
    };

    // Disable Qwen3 hidden thinking tokens (billed but discarded)
    if (this.model.includes('qwen3')) {
      body.chat_template_kwargs = { enable_thinking: false };
    }

    let lastError;
    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
      try {
        const res = await fetch(`${OPENROUTER_BASE_URL}/chat/completions`, {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://burnerempire.com',
            'X-Title': 'Arena Agent',
          },
          body: JSON.stringify(body),
        });

        if (res.status === 429 || res.status >= 500) {
          const wait = RETRY_BACKOFF_MS * Math.pow(2, attempt);
          await new Promise(r => setTimeout(r, wait));
          lastError = new Error(`HTTP ${res.status}`);
          continue;
        }

        if (!res.ok) {
          const text = await res.text();
          throw new Error(`OpenRouter ${res.status}: ${text}`);
        }

        const data = await res.json();
        const content = data.choices?.[0]?.message?.content || '';
        const usage = data.usage || {};

        this.totalCalls++;
        this.totalTokens += (usage.prompt_tokens || 0) + (usage.completion_tokens || 0);

        // Log usage
        this._logUsage(usage, content.length);

        // Parse JSON response
        try {
          const parsed = JSON.parse(content);
          if (parsed.reasoning && parsed.reasoning.length > 500) {
            parsed.reasoning = parsed.reasoning.slice(0, 500) + '...';
          }
          return {
            ...parsed,
            _tokens: (usage.prompt_tokens || 0) + (usage.completion_tokens || 0),
            fallback: false,
          };
        } catch {
          // LLM returned non-JSON, extract what we can
          return {
            action: null,
            reasoning: content.slice(0, 500),
            fallback: true,
            _raw: content,
          };
        }
      } catch (err) {
        lastError = err;
        if (attempt < MAX_RETRIES) {
          await new Promise(r => setTimeout(r, RETRY_BACKOFF_MS * Math.pow(2, attempt)));
        }
      }
    }

    return {
      action: null,
      reasoning: `LLM error: ${lastError?.message}`,
      fallback: true,
    };
  }

  _logUsage(usage, responseLen) {
    try {
      mkdirSync(LOGS_DIR, { recursive: true });
      const entry = {
        t: new Date().toISOString(),
        model: this.model,
        input_tokens: usage.prompt_tokens || 0,
        output_tokens: usage.completion_tokens || 0,
        response_len: responseLen,
      };
      appendFileSync(join(LOGS_DIR, 'llm-usage.jsonl'), JSON.stringify(entry) + '\n');
    } catch {}
  }

  getStats() {
    return { calls: this.totalCalls, tokens: this.totalTokens, model: this.model };
  }
}
