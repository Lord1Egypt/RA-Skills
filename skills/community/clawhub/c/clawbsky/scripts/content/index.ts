/**
 * Content Enhancement Module
 * Image/Video Processing, ALT Text Generator, Quote Card Creator, Meme Maker
 */

import { getOllamaClient } from '../llm.js';

/**
 * Generate ALT text for images using AI
 */
export async function generateAltText(imagePath: string): Promise<string> {
  const ollama = getOllamaClient();
  
  // Note: This would ideally use vision capabilities
  // For now, we'll generate descriptive ALT text based on context
  
  const prompt = `Generate a descriptive ALT text for an image that would make it accessible to visually impaired users.
Keep it under 125 characters.
Describe the main subject, action, setting, and any text visible.

Return just the ALT text, nothing else.`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch (error) {
    return 'Image description unavailable';
  }
}

/**
 * Generate ALT text from image description
 */
export async function generateAltTextFromDescription(description: string): Promise<string> {
  const ollama = getOllamaClient();
  
  const prompt = `Create a concise, accessible ALT text for an image based on this description.
Keep it under 125 characters.
Focus on the essential visual information.

Description: "${description}"

ALT text:`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch (error) {
    return description.substring(0, 125);
  }
}

/**
 * Suggest image improvements
 */
export async function suggestImageImprovements(
  currentAlt: string,
  imageContext?: string
): Promise<string> {
  const ollama = getOllamaClient();
  
  const prompt = `Analyze this image ALT text and suggest improvements for accessibility and engagement.
Current ALT: "${currentAlt}"
${imageContext ? `Image context: "${imageContext}"` : ''}

Provide suggestions in a brief, helpful tone.`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch (error) {
    return 'Consider adding more descriptive details about the image content.';
  }
}

/**
 * Generate a quote card from text
 */
export async function generateQuoteCard(
  quote: string,
  author?: string,
  style?: 'minimal' | 'creative' | 'bold'
): Promise<{
  text: string;
  suggestedStyle: string;
  hashtags: string[];
}> {
  const ollama = getOllamaClient();
  
  const prompt = `Create a quote card post from this quote.
${author ? `Author: ${author}` : ''}

Style preference: ${style || 'creative'}

Return as JSON:
{
  "text": "The formatted quote post",
  "suggestedStyle": "recommended style",
  "hashtags": ["#hashtag1", "#hashtag2"]
}

Quote: "${quote}"`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }],
      format: 'json'
    });

    return JSON.parse(response.message.content);
  } catch {
    return {
      text: `"${quote}"${author ? ` — ${author}` : ''}`,
      suggestedStyle: style || 'minimal',
      hashtags: ['#Quote', '#Inspiration']
    };
  }
}

/**
 * Generate a meme caption
 */
export async function generateMemeCaption(
  template: string,
  topic?: string
): Promise<string> {
  const ollama = getOllamaClient();
  
  const prompt = `Generate a funny meme caption.
Template style: "${template}"
${topic ? `Topic: ${topic}` : ''}

Keep it short (1-2 lines), punchy, and internet-ready.
Just return the caption, no explanation.`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch {
    return 'When you realize...';
  }
}

/**
 * Suggest meme templates
 */
export async function suggestMemeTemplates(
  topic: string
): Promise<{ template: string; caption: string }[]> {
  const ollama = getOllamaClient();
  
  const prompt = `Suggest 3 popular meme formats suitable for this topic.
Return as JSON array:
[
  {"template": "Distracted Boyfriend", "caption": "caption here"},
  {"template": "Change My Mind", "caption": "caption here"},
  {"template": "This Is Fine", "caption": "caption here"}
]

Topic: "${topic}"`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }],
      format: 'json'
    });

    return JSON.parse(response.message.content);
  } catch {
    return [
      { template: 'Distracted Boyfriend', caption: 'Me vs my productivity' },
      { template: 'Drake Hotline Bling', caption: 'Working vs debugging' },
      { template: 'This Is Fine', caption: 'When the production database is on fire' }
    ];
  }
}

/**
 * Transform content for different formats
 */
export async function repurposeContent(
  original: string,
  targetFormat: 'thread' | 'blog' | 'tweet' | 'linkedin'
): Promise<string> {
  const ollama = getOllamaClient();
  
  const formatInstructions = {
    thread: 'Expand into a 5-post Twitter/Bluesky thread with numbered points.',
    blog: 'Expand into a short blog post with introduction, body, and conclusion.',
    tweet: 'Condense into a single engaging tweet under 280 characters.',
    linkedin: 'Transform into a professional LinkedIn post with professional tone.'
  };

  const prompt = `${formatInstructions[targetFormat]}

Original content: "${original}"

Converted:`;

  try {
    const response = await ollama.chat({
      model: 'qwen3.5:4b',
      messages: [{ role: 'user', content: prompt }]
    });

    return response.message.content.trim();
  } catch {
    return original;
  }
}