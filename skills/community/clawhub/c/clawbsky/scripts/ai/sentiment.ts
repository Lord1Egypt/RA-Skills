/**
 * Sentiment Analysis Module
 * Analyzes post engagement sentiment using local LLM
 */

import { getOllamaClient } from '../llm.js';
import type { OllamaResponse } from '../llm.js';

export interface SentimentResult {
  sentiment: 'positive' | 'negative' | 'neutral';
  score: number;
  summary: string;
  emojis: string[];
}

/**
 * Analyze sentiment of a post or engagement
 */
export async function analyzeSentiment(text: string): Promise<SentimentResult> {
  const ollama = getOllamaClient();
  
  const prompt = `Analyze the sentiment of this text. Respond in JSON format:
{
  "sentiment": "positive" or "negative" or "neutral",
  "score": 0-10,
  "summary": "2-3 sentence summary",
  "emojis": ["emoji1", "emoji2"]
}

Text to analyze: "${text}"`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }],
    format: 'json'
  });

  try {
    const result = JSON.parse(response.message.content);
    return {
      sentiment: result.sentiment || 'neutral',
      score: result.score || 5,
      summary: result.summary || '',
      emojis: result.emojis || []
    };
  } catch {
    return {
      sentiment: 'neutral',
      score: 5,
      summary: 'Unable to determine sentiment',
      emojis: ['😐']
    };
  }
}

/**
 * Analyze multiple posts and return overall sentiment
 */
export async function analyzeFeedSentiment(posts: string[]): Promise<SentimentResult> {
  const ollama = getOllamaClient();
  
  const prompt = `Analyze the overall sentiment of these ${posts.length} posts. Respond in JSON:
{
  "sentiment": "positive" or "negative" or "neutral",
  "score": 0-10,
  "summary": "2-3 sentence summary",
  "emojis": ["emoji1", "emoji2"]
}

Posts:
${posts.map((p, i) => `${i + 1}. "${p}"`).join('\n')}`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }],
    format: 'json'
  });

  try {
    const result = JSON.parse(response.message.content);
    return {
      sentiment: result.sentiment || 'neutral',
      score: result.score || 5,
      summary: result.summary || '',
      emojis: result.emojis || []
    };
  } catch {
    return {
      sentiment: 'neutral',
      score: 5,
      summary: 'Unable to determine sentiment',
      emojis: ['😐']
    };
  }
}