/**
 * AI Generation Module
 * Smart Compose, Thread Auto-Complete, Sentiment Analysis, Hashtag Suggestions
 */

import { getOllamaClient } from '../llm.js';
import type { OllamaResponse } from '../llm.js';
import { getAgent } from '../bsky.js';

/**
 * Generate AI content from prompt
 */
export async function generate(
  prompt: string,
  tone: string = 'helpful'
): Promise<string> {
  const ollama = getOllamaClient();
  
  const toneInstructions: Record<string, string> = {
    professional: 'Be professional, concise, and industry-focused.',
    casual: 'Be friendly, casual, and conversational.',
    funny: 'Be witty, humorous, and entertaining.',
    helpful: 'Be helpful, informative, and educational.'
  };

  const systemPrompt = `You are Clawbsky, an AI assistant for Bluesky social media.
Generate a short, engaging social media post (under 280 characters).
${toneInstructions[tone] || toneInstructions.helpful}
Add relevant hashtags at the end.`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: prompt }
    ]
  });

  return response.message.content.trim();
}

/**
 * Generate a thread from a topic
 */
export async function generateThread(
  topic: string,
  numPosts: number = 5
): Promise<string[]> {
  const ollama = getOllamaClient();
  
  const prompt = `Create a ${numPosts}-post Bluesky thread about "${topic}".
Each post should be numbered (1/${numPosts}, 2/${numPosts}, etc.) and build on the previous.
Keep each post under 280 characters.
Add relevant hashtags.

Return only the posts, one per line, numbered.`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }]
  });

  const content = response.message.content.trim();
  const posts = content.split('\n').filter(line => line.trim());
  
  // Clean up each post
  return posts.map(post => {
    // Remove numbering prefix if present
    return post.replace(/^\d+\/\d+:\s*/, '').trim();
  });
}

/**
 * Improve existing text
 */
export async function improveText(text: string): Promise<string> {
  const ollama = getOllamaClient();
  
  const prompt = `Improve this Bluesky post. Make it more engaging, add hashtags if appropriate.
Keep it under 280 characters.

Original: "${text}"

Improved:`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }]
  });

  return response.message.content.trim();
}

/**
 * Generate AI reply suggestions for a post
 */
export async function replyAi(
  postUri: string,
  count: number = 3
): Promise<string[]> {
  const agent = await getAgent();
  const ollama = getOllamaClient();
  
  // Get the post content
  try {
    const threadResponse = await agent.getPostThread({ uri: postUri });
    const post = threadResponse.data.thread.post;
    if (!post || !('record' in post)) {
      throw new Error('Post not found');
    }
    const postText = (post.record as any).text;
    const author = post.author.handle;

    const prompt = `Generate ${count} different reply suggestions for this Bluesky post.
Make each reply different in tone/style (helpful, funny, question, agreement).
Keep each under 280 characters.

Post by @${author}: "${postText}"

Return as a numbered list, one reply per line.`;

    const response: OllamaResponse = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    const content = response.message.content.trim();
    const replies = content.split('\n').filter(line => line.trim());
    
    // Clean up each reply
    return replies.map(reply => {
      return reply.replace(/^\d+[.)]\s*/, '').trim();
    }).slice(0, count);
  } catch (error) {
    console.error('Error getting post:', error);
    return [
      'Thanks for sharing!',
      'Great point!',
      'Interesting perspective!'
    ];
  }
}

/**
 * Analyze a profile or post
 */
export async function analyze(target: string, isPost: boolean = false): Promise<string> {
  const agent = await getAgent();
  const ollama = getOllamaClient();
  
  try {
    let content = '';
    let author = '';
    
    if (isPost) {
      // Analyze a post
      const threadResponse = await agent.getPostThread({ uri: target });
      const post = threadResponse.data.thread.post;
      if (!post || !('record' in post)) {
        throw new Error('Post not found');
      }
      content = (post.record as any).text;
      author = post.author.handle;
    } else {
      // Analyze a profile
      const handle = target.replace(/^@/, '');
      const profileResponse = await agent.getProfile({ actor: handle });
      const profile = profileResponse.data;
      content = `${profile.displayName || ''} ${profile.description || ''}`;
      author = handle;
    }

    const prompt = `Analyze this Bluesky ${isPost ? 'post' : 'profile'} and provide insights.
${isPost ? 'Consider the content quality, engagement potential, and topic.' : 'Consider the niche, engagement style, and growth potential.'}

${isPost ? 'Post' : 'Profile'} by @${author}: "${content}"

Provide a brief analysis (2-3 sentences).`;

    const response: OllamaResponse = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch (error) {
    return 'Unable to analyze. Please check the URI/handle and try again.';
  }
}

/**
 * Sentiment analysis
 */
export async function analyzeSentiment(text: string): Promise<{
  sentiment: string;
  score: number;
  summary: string;
}> {
  const ollama = getOllamaClient();
  
  const prompt = `Analyze the sentiment of this text. Return JSON:
{"sentiment": "positive|negative|neutral", "score": 0-10, "summary": "brief summary"}

Text: "${text}"`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }],
    format: 'json'
  });

  try {
    return JSON.parse(response.message.content);
  } catch {
    return { sentiment: 'neutral', score: 5, summary: 'Unable to determine' };
  }
}

/**
 * Hashtag suggestions
 */
export async function suggestHashtags(text: string, count: number = 5): Promise<string[]> {
  const ollama = getOllamaClient();
  
  const prompt = `Generate ${count} relevant hashtags for this post.
Return as JSON array of strings: ["#tag1", "#tag2", ...]

Post: "${text}"`;

  const response: OllamaResponse = await ollama.chat({
    model: 'qwen3.5:4b',
    messages: [{ role: 'user', content: prompt }],
    format: 'json'
  });

  try {
    return JSON.parse(response.message.content);
  } catch {
    return ['#Bluesky', '#Tech', '#SocialMedia'];
  }
}