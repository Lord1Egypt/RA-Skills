import { NewsItem, SignalResult } from '../types.js';
import { ISignalModel } from './interface.js';

export class OpenAISignalModel implements ISignalModel {
  constructor(private apiKey: string, private model: string, private timeoutMs: number) {}

  async analyze(news: NewsItem): Promise<SignalResult> {
    const c = new AbortController();
    const t = setTimeout(() => c.abort(), this.timeoutMs);
    try {
      const r = await fetch('https://api.openai.com/v1/chat/completions', {
        method: 'POST',
        signal: c.signal,
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: this.model,
          temperature: 0,
          response_format: { type: 'json_object' },
          messages: [
            { role: 'system', content: 'Return JSON: {sentiment,confidence,tags,impact,reason} sentiment in [-1,1]' },
            { role: 'user', content: `${news.title}\n${news.body}` }
          ]
        })
      });
      if (!r.ok) throw new Error(`openai ${r.status}`);
      const j = await r.json();
      const content = j.choices?.[0]?.message?.content ?? '{}';
      const out = JSON.parse(content);
      return {
        sentiment: Number(out.sentiment ?? 0),
        confidence: Number(out.confidence ?? 0.5),
        impact: Number(out.impact ?? 0.5),
        tags: Array.isArray(out.tags) ? out.tags : [],
        reason: String(out.reason ?? 'OpenAIModel')
      };
    } finally {
      clearTimeout(t);
    }
  }
}
