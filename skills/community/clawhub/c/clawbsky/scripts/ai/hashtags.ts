/**
 * Hashtag Suggestions Module
 * AI recommends optimal hashtags using local LLM
 */

import { getOllamaClient } from '../llm.js';
import type { OllamaResponse } from '../llm.js';

export interface HashtagSuggestion {
  tag: string;
  relevance: number; // 0-100
  trending: boolean;
}

/**
 * Generate hashtag suggestions for a post
 */
export async function suggestHashtags(
  text: string,
  count: number = 5,
  includeTrending: boolean = true
): Promise<HashtagSuggestion[]> {
  const ollama = getOllamaClient();
  
  const prompt = `Generate ${count} relevant hashtags for this post. 
${includeTrending ? 'Include popular trending hashtags when relevant.' : ''}
Respond in JSON array format:
[{"tag": "#hashtag", "relevance": 95, "trending": true}, ...]

Post content: "${text}"`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }],
    format: 'json'
  });

  try {
    const hashtags = JSON.parse(response.message.content);
    return hashtags.map((h: any) => ({
      tag: h.tag || h.tag?.replace(/^#/, '') ? `#${h.tag.replace(/^#/, '')}` : '#',
      relevance: h.relevance || 50,
      trending: h.trending || false
    }));
  } catch {
    return [
      { tag: '#Trending', relevance: 80, trending: true },
      { tag: '#AI', relevance: 75, trending: true },
      { tag: '#Tech', relevance: 70, trending: false },
      { tag: '#Innovation', relevance: 65, trending: false },
      { tag: '#Future', relevance: 60, trending: true }
    ];
  }
}

/**
 * Analyze hashtag performance
 */
export async function analyzeHashtags(hashtags: string[]): Promise<{
  best: string;
  averageEngagement: number;
  recommendations: string[];
}> {
  const ollama = getOllamaClient();
  
  const prompt = `Analyze these hashtags and recommend the best one to use. Respond in JSON:
{
  "best": "#bestHashtag",
  "averageEngagement": 85,
  "recommendations": ["recommendation1", "recommendation2"]
}

Hashtags: ${hashtags.join(', ')}`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }],
    format: 'json'
  });

  try {
    return JSON.parse(response.message.content);
  } catch {
    return {
      best: hashtags[0] || '#AI',
      averageEngagement: 50,
      recommendations: ['Use a mix of popular and niche hashtags']
    };
  }
}