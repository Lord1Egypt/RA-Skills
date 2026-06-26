/**
 * Auto-Reply Bot Module
 * Reply to mentions with AI-generated responses
 */

import { getOllamaClient } from '../llm.js';
import type { OllamaResponse } from '../llm.js';

export interface ReplyConfig {
  enabled: boolean;
  tone: 'professional' | 'casual' | 'funny' | 'helpful';
  autoLike: boolean;
  keywords?: string[];
  excludeUsers?: string[];
}

const defaultConfig: ReplyConfig = {
  enabled: true,
  tone: 'helpful',
  autoLike: true,
  keywords: [],
  excludeUsers: []
};

/**
 * Generate an AI reply to a post
 */
export async function generateAutoReply(
  postText: string,
  author: string,
  config: ReplyConfig = defaultConfig
): Promise<string> {
  const ollama = getOllamaClient();
  
  const toneInstructions = {
    professional: 'Be professional and concise.',
    casual: 'Be friendly and casual.',
    funny: 'Be witty and humorous.',
    helpful: 'Be helpful and informative.'
  };

  const prompt = `Generate a ${config.tone} reply to this Bluesky post. 
${toneInstructions[config.tone]}
Keep it under 280 characters.

Post by @${author}: "${postText}"

Your reply:`;

  try {
    const response: OllamaResponse = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch (error) {
    console.error('Error generating auto-reply:', error);
    return `Thanks for sharing @${author}!`;
  }
}

/**
 * Generate reply suggestions (for manual review)
 */
export async function generateReplySuggestions(
  postText: string,
  author: string,
  count: number = 3
): Promise<string[]> {
  const ollama = getOllamaClient();
  
  const prompt = `Generate ${count} different replies to this Bluesky post. 
Return as a JSON array of strings. Each reply should be different in tone/style.
Keep each reply under 280 characters.

Post by @${author}: "${postText}"

JSON array:`;

  try {
    const response: OllamaResponse = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }],
      format: 'json'
    });

    const replies = JSON.parse(response.message.content);
    return replies;
  } catch (error) {
    console.error('Error generating reply suggestions:', error);
    return [
      `Thanks for sharing!`,
      `Really interesting point @${author}!`,
      `Could you tell me more?`
    ];
  }
}

/**
 * Check if post matches keyword triggers
 */
export function matchesKeywords(text: string, keywords: string[]): boolean {
  if (!keywords || keywords.length === 0) return true;
  const lowerText = text.toLowerCase();
  return keywords.some(keyword => lowerText.includes(keyword.toLowerCase()));
}

/**
 * AI-powered follow-back
 */
export async function generateFollowBackMessage(
  profile: any
): Promise<string> {
  const ollama = getOllamaClient();
  
  const prompt = `Generate a short, friendly welcome message for a new follower.
Keep it under 280 characters and mention something from their profile if available.

Profile description: "${profile.description || 'No description'}"
Display name: ${profile.displayName || profile.handle}

Welcome message:`;

  try {
    const response: OllamaResponse = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch (error) {
    return `Thanks for following!`;
  }
}