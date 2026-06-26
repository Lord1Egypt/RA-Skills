/**
 * AI Content Repurposer - Core Converter
 * Transforms long-form content into multiple formats
 */

const axios = require('axios');
const cheerio = require('cheerio');

class ContentConverter {
  constructor(options = {}) {
    this.apiKey = options.apiKey || process.env.OPENAI_API_KEY;
    this.model = options.model || 'gpt-4';
    this.baseUrl = 'https://api.openai.com/v1';
  }

  /**
   * Convert YouTube video to TikTok/Shorts/Reels script
   * @param {string} transcript - Video transcript
   * @param {string} platform - Target platform (tiktok, shorts, reels)
   * @returns {Promise<object>} - Converted script
   */
  async youtubeToShortForm(transcript, platform = 'tiktok') {
    const limits = {
      tiktok: { maxDuration: 180, maxChars: 2000 },
      shorts: { maxDuration: 60, maxChars: 1000 },
      reels: { maxDuration: 90, maxChars: 1500 }
    };

    const limit = limits[platform];
    
    const prompt = `
Transform this YouTube video transcript into a ${platform} script.

Requirements:
- Maximum ${limit.maxDuration} seconds when spoken
- Hook in first 3 seconds
- Keep only the most engaging parts
- Add visual cues in [brackets]
- Include call-to-action at the end
- Natural, conversational tone

Transcript:
${transcript.substring(0, 8000)}

Output format (JSON):
{
  "title": "Catchy title",
  "hook": "Opening line",
  "body": ["Point 1", "Point 2", "Point 3"],
  "cta": "Call to action",
  "hashtags": ["#tag1", "#tag2"],
  "visualCues": ["[Show X]", "[Cut to Y]"]
}
`;

    return await this._callAI(prompt);
  }

  /**
   * Convert blog post to Twitter thread
   * @param {string} blogContent - Blog post content
   * @param {number} tweetCount - Number of tweets (default: 5-10)
   * @returns {Promise<object>} - Twitter thread
   */
  async blogToTwitterThread(blogContent, tweetCount = 7) {
    const prompt = `
Transform this blog post into a Twitter thread of ${tweetCount} tweets.

Requirements:
- Each tweet max 280 characters
- First tweet must hook readers
- Each tweet should stand alone but flow naturally
- Use thread formatting (1/X, 2/X, etc.)
- Include emojis sparingly
- Last tweet: summary + CTA

Blog content:
${blogContent.substring(0, 8000)}

Output format (JSON):
{
  "threadTitle": "Thread title",
  "tweets": [
    {"number": 1, "text": "Tweet 1"},
    {"number": 2, "text": "Tweet 2"}
  ],
  "hashtags": ["#tag1", "#tag2"]
}
`;

    return await this._callAI(prompt);
  }

  /**
   * Convert blog post to LinkedIn post
   * @param {string} blogContent - Blog post content
   * @param {string} tone - Professional tone (thought-leadership, educational, story)
   * @returns {Promise<object>} - LinkedIn post
   */
  async blogToLinkedIn(blogContent, tone = 'thought-leadership') {
    const prompt = `
Transform this blog post into a LinkedIn post with ${tone} tone.

Requirements:
- Start with strong hook (first 2 lines visible before "see more")
- Use short paragraphs and white space
- Professional but conversational
- Include personal insight or lesson
- End with question to drive engagement
- 3-5 relevant hashtags

Blog content:
${blogContent.substring(0, 8000)}

Output format (JSON):
{
  "hook": "Opening lines",
  "body": "Main content",
  "insight": "Personal takeaway",
  "question": "Engagement question",
  "hashtags": ["#tag1", "#tag2"]
}
`;

    return await this._callAI(prompt);
  }

  /**
   * Convert podcast to transcript with chapters
   * @param {string} audioTranscript - Raw podcast transcript
   * @param {object} options - Options (includeTimestamps, speakerLabels)
   * @returns {Promise<object>} - Formatted transcript
   */
  async podcastToTranscript(audioTranscript, options = {}) {
    const { includeTimestamps = true, speakerLabels = false } = options;

    const prompt = `
Format this podcast transcript with proper structure.

Requirements:
${includeTimestamps ? '- Add timestamps every 2-3 minutes' : ''}
${speakerLabels ? '- Label different speakers (Speaker 1, Speaker 2, etc.)' : ''}
- Break into logical chapters/sections
- Remove filler words (um, uh, like)
- Fix punctuation and capitalization
- Add chapter titles

Transcript:
${audioTranscript.substring(0, 8000)}

Output format (JSON):
{
  "title": "Podcast episode title",
  "chapters": [
    {"timestamp": "00:00", "title": "Chapter 1", "content": "..."}
  ],
  "fullTranscript": "Clean formatted transcript",
  "keyQuotes": ["Quote 1", "Quote 2"]
}
`;

    return await this._callAI(prompt);
  }

  /**
   * Generate summary and quote cards from podcast
   * @param {string} transcript - Podcast transcript
   * @returns {Promise<object>} - Summary and quotes
   */
  async podcastToSummary(transcript) {
    const prompt = `
Create a comprehensive summary and extract quotable moments from this podcast.

Requirements:
- 3-sentence episode summary
- 5-7 key takeaways as bullet points
- 10 shareable quotes (under 200 chars each)
- Suggest 3-5 social media post ideas

Transcript:
${transcript.substring(0, 8000)}

Output format (JSON):
{
  "summary": "Brief episode summary",
  "takeaways": ["Takeaway 1", "Takeaway 2"],
  "quotes": [
    {"text": "Quote", "timestamp": "00:00", "speaker": "Name"}
  ],
  "socialPosts": [
    {"platform": "twitter", "content": "..."},
    {"platform": "linkedin", "content": "..."}
  ]
}
`;

    return await this._callAI(prompt);
  }

  /**
   * Fetch YouTube transcript (using placeholder - integrate with real API)
   * @param {string} videoUrl - YouTube video URL
   * @returns {Promise<string>} - Transcript text
   */
  async fetchYouTubeTranscript(videoUrl) {
    // Placeholder: integrate with YouTube Transcript API or similar
    const videoId = this._extractVideoId(videoUrl);
    
    // TODO: Implement actual transcript fetching
    // Options: youtube-transcript npm package, or API service
    throw new Error('YouTube transcript fetching not yet implemented. Use manual transcript input.');
  }

  /**
   * Fetch blog post content from URL
   * @param {string} url - Blog post URL
   * @returns {Promise<string>} - Article content
   */
  async fetchBlogContent(url) {
    try {
      const response = await axios.get(url, {
        headers: { 'User-Agent': 'Mozilla/5.0' },
        timeout: 10000
      });

      const $ = cheerio.load(response.data);
      
      // Remove scripts, styles, nav, footer
      $('script, style, nav, footer, header, aside').remove();
      
      // Try to find main content
      let content = $('article').text() || 
                    $('main').text() || 
                    $('.post-content').text() || 
                    $('.entry-content').text() ||
                    $('body').text();

      // Clean up whitespace
      return content.replace(/\s+/g, ' ').trim();
    } catch (error) {
      throw new Error(`Failed to fetch blog content: ${error.message}`);
    }
  }

  /**
   * Call AI API for content transformation
   * @private
   */
  async _callAI(prompt) {
    if (!this.apiKey) {
      // Fallback: return template structure without AI processing
      return this._fallbackResponse(prompt);
    }

    try {
      const response = await axios.post(
        `${this.baseUrl}/chat/completions`,
        {
          model: this.model,
          messages: [
            { role: 'system', content: 'You are a content transformation expert.' },
            { role: 'user', content: prompt }
          ],
          temperature: 0.7,
          max_tokens: 2000
        },
        {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`,
            'Content-Type': 'application/json'
          }
        }
      );

      const content = response.data.choices[0].message.content;
      return JSON.parse(content);
    } catch (error) {
      console.error('AI API error:', error.message);
      return this._fallbackResponse(prompt);
    }
  }

  /**
   * Fallback response when AI not available
   * @private
   */
  _fallbackResponse(prompt) {
    // Return demo/template structure based on transformation type
    if (prompt.includes('tiktok') || prompt.includes('shorts') || prompt.includes('reels')) {
      return {
        warning: '⚠️  AI not configured. Showing demo output. Set OPENAI_API_KEY for real transformations.',
        title: 'Your Catchy Title Here',
        hook: 'Hook viewers in 3 seconds with this opening line...',
        body: [
          'Key point 1 from your content',
          'Key point 2 that builds interest',
          'Key point 3 with the payoff'
        ],
        cta: 'Follow for more! | Comment your thoughts below',
        hashtags: ['#viral', '#trending', '#fyp'],
        visualCues: ['[Show engaging visual]', '[Text overlay appears]', '[Quick cut]']
      };
    } else if (prompt.includes('twitter')) {
      return {
        warning: '⚠️  AI not configured. Showing demo output. Set OPENAI_API_KEY for real transformations.',
        threadTitle: 'Your Thread Title Here',
        tweets: Array(7).fill(null).map((_, i) => ({
          number: i + 1,
          text: `Tweet ${i + 1}: Key insight from your content. Keep it under 280 characters. 🧵 ${i + 1}/7`
        })),
        hashtags: ['#thread', '#content']
      };
    } else if (prompt.includes('linkedin')) {
      return {
        warning: '⚠️  AI not configured. Showing demo output. Set OPENAI_API_KEY for real transformations.',
        hook: 'Hook that makes people click "see more"...',
        body: 'Main content goes here. Use short paragraphs. White space is your friend.\n\nMake it professional but conversational.',
        insight: '💡 Personal insight or lesson learned',
        question: '❓ What\'s your experience with this?',
        hashtags: ['#leadership', '#insights', '#growth']
      };
    } else if (prompt.includes('podcast') && prompt.includes('summary')) {
      return {
        warning: '⚠️  AI not configured. Showing demo output. Set OPENAI_API_KEY for real transformations.',
        summary: 'Brief 3-sentence summary of the episode.',
        takeaways: ['Takeaway 1', 'Takeaway 2', 'Takeaway 3'],
        quotes: [
          { text: 'Memorable quote from the episode', timestamp: '00:00', speaker: 'Speaker' }
        ],
        socialPosts: [
          { platform: 'twitter', content: 'Social post content...' }
        ]
      };
    } else if (prompt.includes('podcast') && prompt.includes('transcript')) {
      return {
        warning: '⚠️  AI not configured. Showing demo output. Set OPENAI_API_KEY for real transformations.',
        title: 'Podcast Episode Title',
        chapters: [
          { timestamp: '00:00', title: 'Introduction', content: 'Chapter content...' },
          { timestamp: '02:30', title: 'Main Discussion', content: 'Chapter content...' }
        ],
        fullTranscript: 'Clean formatted transcript would appear here.',
        keyQuotes: ['Quote 1', 'Quote 2']
      };
    }
    
    return {
      warning: 'AI not configured. Showing template structure.',
      prompt: prompt.substring(0, 500) + '...'
    };
  }

  /**
   * Extract YouTube video ID from URL
   * @private
   */
  _extractVideoId(url) {
    const match = url.match(/(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/);
    return match ? match[1] : null;
  }
}

module.exports = ContentConverter;
