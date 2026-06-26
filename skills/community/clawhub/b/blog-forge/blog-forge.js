/**
 * BlogForge — End-to-End Blog Post Generator
 */
const https = require('https');
const http = require('http');
const crypto = require('crypto');

class BlogForge {
  constructor(options = {}) {
    this.defaultLength = options.defaultLength || 1500;
    this.defaultTone = options.defaultTone || 'professional';
  }

  outline(topic, options = {}) {
    const sections = options.sections || 5;
    const outline = {
      title: this._generateTitle(topic),
      subtitle: '',
      sections: [],
      meta: { topic, targetLength: options.length || this.defaultLength, tone: options.tone || this.defaultTone }
    };
    const templates = [
      'Introduction — hook the reader',
      'The Problem — why this matters',
      'The Solution — core content',
      'Deep Dive — details and examples',
      'Practical Application — how to use this',
      'Common Mistakes — what to avoid',
      'Conclusion — key takeaways'
    ];
    for (let i = 0; i < Math.min(sections, templates.length); i++) {
      outline.sections.push({ heading: templates[i], estimatedWords: Math.round((options.length || this.defaultLength) / sections) });
    }
    return outline;
  }

  seoMeta(title, content) {
    const words = content.split(/\s+/).filter(Boolean);
    const wordFreq = {};
    for (const w of words) {
      const clean = w.toLowerCase().replace(/[^a-z]/g, '');
      if (clean.length > 4) wordFreq[clean] = (wordFreq[clean] || 0) + 1;
    }
    const keywords = Object.entries(wordFreq).sort((a, b) => b[1] - a[1]).slice(0, 5).map(([w]) => w);
    return {
      title: title.length > 60 ? title.substring(0, 57) + '...' : title,
      description: content.split('.').slice(0, 2).join('.').substring(0, 155) + '...',
      keywords,
      readingTime: Math.ceil(words.length / 250) + ' min',
      wordCount: words.length
    };
  }

  formatForPlatform(content, platform) {
    switch (platform) {
      case 'medium': return content;
      case 'devto': return `---\ntitle: \npublished: false\ntags: \n---\n\n${content}`;
      case 'wordpress': return content.replace(/^# (.*)/gm, '<h1>$1</h1>').replace(/^## (.*)/gm, '<h2>$1</h2>');
      default: return content;
    }
  }

  _generateTitle(topic) {
    const patterns = [
      `Why ${topic} Matters More Than You Think`,
      `The Complete Guide to ${topic}`,
      `${topic}: What Nobody Tells You`,
      `How ${topic} Actually Works`
    ];
    return patterns[Math.floor(Math.random() * patterns.length)];
  }

  // ──────────────────────────────────────────────────
  // NEW METHODS BELOW
  // ──────────────────────────────────────────────────

  /**
   * Generate a full blog post using an AI model.
   *
   * @async
   * @param {Object} options - Generation options.
   * @param {string} options.topic - The blog post topic (required).
   * @param {string} [options.tone] - Writing tone (e.g. 'professional', 'casual', 'technical'). Defaults to instance defaultTone.
   * @param {number} [options.length] - Target word count. Defaults to instance defaultLength.
   * @param {string} [options.platform] - Target platform for formatting ('medium', 'devto', 'wordpress').
   * @param {string} [options.model] - Model identifier with prefix routing: 'anthropic/claude-3-5-sonnet-20241022', 'openai/gpt-4o', 'ollama/llama3'.
   * @param {string} [options.apiKey] - API key for the chosen provider. Falls back to env vars.
   * @returns {Promise<{title: string, content: string, meta: Object, images: Array<string>, readability: Object, platform_content: string}>}
   * @throws {Error} If topic is missing, model prefix is unrecognized, or API call fails.
   */
  async generate(options = {}) {
    const {
      topic,
      tone = this.defaultTone,
      length = this.defaultLength,
      platform = 'medium',
      model = 'anthropic/claude-3-5-sonnet-20241022',
    } = options;

    if (!topic) {
      throw new Error('BlogForge.generate() requires a "topic" option.');
    }

    const apiKey = options.apiKey || this._resolveApiKey(model);
    const [provider] = model.split('/');
    const modelName = model.substring(provider.length + 1);

    const outlineData = this.outline(topic, { length, tone, sections: 5 });

    const _genInstructions = `You are BlogForge, an expert long-form blog writer. Your job is to write a complete, publication-ready blog post in Markdown.

INSTRUCTIONS:
- Topic: "${topic}"
- Tone: ${tone}
- Target length: approximately ${length} words
- Structure the post with a compelling title on the first line as a Markdown H1 (# Title), followed by an engaging subtitle as italic text.
- Use H2 (##) for major sections and H3 (###) for subsections where appropriate.
- Begin with a hook that draws the reader in — a surprising fact, a question, or a relatable scenario. Do NOT begin with "In today's world" or any cliché opener.
- Include concrete examples, data points, analogies, and actionable advice. Where statistics are used, note they are illustrative.
- Vary sentence length naturally. Mix short punchy sentences with longer explanatory ones.
- Use transition phrases between sections to maintain flow.
- End with a strong conclusion that summarizes key takeaways and includes a call to action.
- Use bullet points or numbered lists where they add clarity, but don't overuse them.
- Write for humans. Be engaging, specific, and avoid filler phrases.
- Do NOT include image placeholders, links, or references to "this article". Just write the content.

OUTLINE FOR GUIDANCE (adapt freely):
${outlineData.sections.map((s, i) => `${i + 1}. ${s.heading} (~${s.estimatedWords} words)`).join('\n')}

Write the complete blog post now in Markdown. Begin directly with the H1 title.`;

    let rawContent;

    switch (provider) {
      case 'anthropic':
        rawContent = await this._callAnthropic(modelName, _genInstructions, apiKey);
        break;
      case 'openai':
        rawContent = await this._callOpenAI(modelName, _genInstructions, apiKey);
        break;
      case 'ollama':
        rawContent = await this._callOllama(modelName, _genInstructions);
        break;
      default:
        throw new Error(`BlogForge: Unknown model provider "${provider}". Use "anthropic/...", "openai/...", or "ollama/...".`);
    }

    if (!rawContent || rawContent.trim().length === 0) {
      throw new Error('BlogForge.generate() received empty response from AI model.');
    }

    // Extract title from first H1 line
    const titleMatch = rawContent.match(/^#\s+(.+)$/m);
    const title = titleMatch ? titleMatch[1].trim() : this._generateTitle(topic);

    const meta = this.seoMeta(title, rawContent);
    const images = this.imageSuggestions(rawContent, 3);
    const readability = this.readabilityScore(rawContent);
    const platform_content = this.formatForPlatform(rawContent, platform);

    return {
      title,
      content: rawContent,
      meta,
      images,
      readability,
      platform_content
    };
  }

  /**
   * Generate relevant image description suggestions from blog content.
   *
   * Extracts key topics, headings, and notable phrases from the content,
   * then crafts descriptive image suggestions suitable for stock photo searches
   * or AI image generation prompts.
   *
   * @param {string} content - The blog post content (Markdown).
   * @param {number} [count=3] - Number of image suggestions to generate.
   * @returns {Array<string>} Array of image description strings.
   */
  imageSuggestions(content, count = 3) {
    if (!content || content.trim().length === 0) {
      return [];
    }

    const suggestions = [];

    // 1. Extract headings as thematic anchors
    const headings = [];
    const headingRegex = /^#{1,3}\s+(.+)$/gm;
    let hMatch;
    while ((hMatch = headingRegex.exec(content)) !== null) {
      headings.push(hMatch[1].trim());
    }

    // 2. Extract significant noun phrases / key topics using word frequency
    const plainText = content
      .replace(/^#{1,6}\s+.*$/gm, '')
      .replace(/[*_`~\[\]()]/g, '')
      .replace(/\n+/g, ' ')
      .trim();

    const stopWords = new Set([
      'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
      'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
      'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
      'could', 'should', 'may', 'might', 'shall', 'can', 'need', 'dare',
      'ought', 'used', 'this', 'that', 'these', 'those', 'it', 'its',
      'they', 'them', 'their', 'we', 'our', 'you', 'your', 'he', 'she',
      'his', 'her', 'my', 'me', 'who', 'which', 'what', 'when', 'where',
      'how', 'why', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
      'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
      'so', 'than', 'too', 'very', 'just', 'because', 'as', 'until', 'while',
      'about', 'between', 'through', 'during', 'before', 'after', 'above',
      'below', 'up', 'down', 'out', 'off', 'over', 'under', 'again',
      'further', 'then', 'once', 'here', 'there', 'also', 'into', 'like',
      'dont', 'doesnt', 'didnt', 'wont', 'wouldnt', 'cant', 'couldnt',
      'shouldnt', 'isnt', 'arent', 'wasnt', 'werent', 'hasnt', 'havent',
      'hadnt', 'youre', 'theyre', 'were', 'hes', 'shes', 'its', 'lets',
      'thats', 'whos', 'whats', 'heres', 'theres', 'wheres', 'whens',
      'whys', 'hows', 'many', 'much', 'well', 'back', 'even', 'still',
      'make', 'made', 'know', 'think', 'take', 'come', 'want', 'look',
      'use', 'find', 'give', 'tell', 'work', 'call', 'try', 'ask',
      'seem', 'feel', 'leave', 'keep', 'let', 'begin', 'show', 'hear',
      'play', 'run', 'move', 'live', 'believe', 'hold', 'bring', 'happen',
      'write', 'provide', 'sit', 'stand', 'lose', 'pay', 'meet', 'include',
      'continue', 'set', 'learn', 'change', 'lead', 'understand', 'watch',
      'follow', 'stop', 'create', 'speak', 'read', 'allow', 'add', 'spend',
      'grow', 'open', 'walk', 'win', 'offer', 'remember', 'consider',
      'appear', 'buy', 'wait', 'serve', 'die', 'send', 'expect', 'build',
      'stay', 'fall', 'cut', 'reach', 'kill', 'remain', 'really', 'going',
      'thing', 'things', 'something', 'anything', 'nothing', 'everything',
      'someone', 'anyone', 'everyone', 'people', 'time', 'year', 'way',
      'day', 'world', 'life', 'hand', 'part', 'place', 'case', 'week',
      'company', 'system', 'program', 'question', 'point', 'government',
      'number', 'night', 'home', 'water', 'room', 'mother', 'area',
      'money', 'story', 'fact', 'month', 'lot', 'right', 'study',
      'book', 'eye', 'job', 'word', 'though', 'business', 'issue', 'side',
      'kind', 'head', 'house', 'service', 'friend', 'father', 'power',
      'hour', 'game', 'line', 'end', 'among', 'since', 'however',
      'away', 'turn', 'start', 'might', 'result', 'today', 'whether',
      'help', 'gets', 'getting', 'become'
    ]);

    // Build bigram frequency
    const words = plainText.split(/\s+/).map(w => w.toLowerCase().replace(/[^a-z'-]/g, '')).filter(w => w.length > 2);
    const bigramFreq = {};
    const unigramFreq = {};

    for (let i = 0; i < words.length; i++) {
      const w = words[i];
      if (!stopWords.has(w) && w.length > 3) {
        unigramFreq[w] = (unigramFreq[w] || 0) + 1;
      }
      if (i < words.length - 1) {
        const w2 = words[i + 1];
        if (!stopWords.has(w) && !stopWords.has(w2) && w.length > 3 && w2.length > 3) {
          const bigram = `${w} ${w2}`;
          bigramFreq[bigram] = (bigramFreq[bigram] || 0) + 1;
        }
      }
    }

    // Top key phrases
    const topBigrams = Object.entries(bigramFreq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10)
      .map(([phrase]) => phrase);

    const topUnigrams = Object.entries(unigramFreq)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 15)
      .map(([word]) => word);

    // 3. Extract sentences that contain strong visual language
    const sentences = plainText.split(/[.!?]+/).map(s => s.trim()).filter(s => s.length > 20);
    const visualWords = new Set([
      'build', 'grow', 'break', 'rise', 'fall', 'light', 'dark', 'bright',
      'fast', 'slow', 'team', 'person', 'group', 'office', 'computer',
      'screen', 'path', 'road', 'journey', 'mountain', 'bridge', 'wall',
      'door', 'window', 'tool', 'machine', 'network', 'graph', 'chart',
      'data', 'flow', 'stream', 'wave', 'pattern', 'structure', 'design',
      'landscape', 'city', 'forest', 'ocean', 'sky', 'cloud', 'fire',
      'puzzle', 'maze', 'ladder', 'stairs', 'foundation', 'blueprint'
    ]);

    const visualSentences = sentences
      .map(s => {
        const sWords = s.toLowerCase().split(/\s+/);
        const visualScore = sWords.filter(w => visualWords.has(w.replace(/[^a-z]/g, ''))).length;
        return { sentence: s, score: visualScore };
      })
      .filter(s => s.score > 0)
      .sort((a, b) => b.score - a.score);

    // 4. Build image descriptions using multiple strategies

    // Strategy A: Hero image from title/first heading
    if (headings.length > 0) {
      const mainTopic = headings[0].replace(/[#*_`]/g, '').trim();
      suggestions.push(
        `A visually compelling hero image representing "${mainTopic}" — wide-angle, editorial style photography with clean composition suitable for a blog header`
      );
    }

    // Strategy B: Concept images from top bigrams/key phrases
    for (const phrase of topBigrams.slice(0, 3)) {
      if (suggestions.length >= count) break;
      suggestions.push(
        `An illustrative image depicting the concept of "${phrase}" — professional, modern aesthetic with a clean background, suitable for inline blog illustration`
      );
    }

    // Strategy C: Scene images from visual sentences
    for (const vs of visualSentences.slice(0, 3)) {
      if (suggestions.length >= count) break;
      const condensed = vs.sentence.length > 100 ? vs.sentence.substring(0, 100).trim() + '...' : vs.sentence;
      suggestions.push(
        `A photograph or illustration capturing the scene: "${condensed}" — warm lighting, editorial quality, blog-appropriate`
      );
    }

    // Strategy D: Section-specific images from headings
    for (let i = 1; i < headings.length; i++) {
      if (suggestions.length >= count) break;
      const heading = headings[i].replace(/[#*_`—-]/g, '').trim();
      if (heading.length > 5) {
        suggestions.push(
          `An infographic-style image or conceptual illustration for the section "${heading}" — clean design, muted professional color palette`
        );
      }
    }

    // Strategy E: Fallback from top unigrams
    if (suggestions.length < count && topUnigrams.length >= 2) {
      const topicPhrase = topUnigrams.slice(0, 3).join(', ');
      suggestions.push(
        `A minimalist conceptual image representing ${topicPhrase} — abstract geometric design with a modern tech aesthetic, suitable as a blog section divider`
      );
    }

    // Final fallback
    while (suggestions.length < count) {
      suggestions.push(
        `A generic professional blog illustration — clean workspace, modern design elements, neutral color palette`
      );
    }

    return suggestions.slice(0, count);
  }

  /**
   * Calculate the Flesch-Kincaid readability grade level and score for the given content.
   *
   * @param {string} content - Text content to analyze.
   * @returns {{grade: number, score: number, level: string, avgSentenceLength: number, avgSyllables: number}}
   */
  readabilityScore(content) {
    if (!content || content.trim().length === 0) {
      return { grade: 0, score: 0, level: 'easy', avgSentenceLength: 0, avgSyllables: 0 };
    }

    // Strip markdown formatting
    const plainText = content
      .replace(/^#{1,6}\s+/gm, '')
      .replace(/[*_`~\[\]()]/g, '')
      .replace(/!\[.*?\]\(.*?\)/g, '')
      .replace(/\[.*?\]\(.*?\)/g, '')
      .replace(/^[-*+]\s+/gm, '')
      .replace(/^\d+\.\s+/gm, '')
      .replace(/^>\s+/gm, '')
      .replace(/---+/g, '')
      .replace(/\n{2,}/g, '\n')
      .trim();

    // Split into sentences
    const sentences = plainText
      .split(/[.!?]+/)
      .map(s => s.trim())
      .filter(s => s.length > 0 && /[a-zA-Z]/.test(s));

    if (sentences.length === 0) {
      return { grade: 0, score: 0, level: 'easy', avgSentenceLength: 0, avgSyllables: 0 };
    }

    // Get all words
    const allWords = [];
    for (const sentence of sentences) {
      const sentenceWords = sentence.split(/\s+/).filter(w => /[a-zA-Z]/.test(w));
      allWords.push(...sentenceWords);
    }

    const totalWords = allWords.length;
    const totalSentences = sentences.length;

    if (totalWords === 0) {
      return { grade: 0, score: 0, level: 'easy', avgSentenceLength: 0, avgSyllables: 0 };
    }

    // Count syllables
    let totalSyllables = 0;
    for (const word of allWords) {
      totalSyllables += this._countSyllables(word);
    }

    const avgSentenceLength = totalWords / totalSentences;
    const avgSyllablesPerWord = totalSyllables / totalWords;

    // Flesch Reading Ease Score
    const score = 206.835 - (1.015 * avgSentenceLength) - (84.6 * avgSyllablesPerWord);

    // Flesch-Kincaid Grade Level
    const grade = (0.39 * avgSentenceLength) + (11.8 * avgSyllablesPerWord) - 15.59;

    // Determine level
    let level;
    const clampedScore = Math.max(0, Math.min(100, score));
    if (clampedScore >= 60) {
      level = 'easy';
    } else if (clampedScore >= 30) {
      level = 'medium';
    } else {
      level = 'hard';
    }

    return {
      grade: Math.round(Math.max(0, grade) * 10) / 10,
      score: Math.round(clampedScore * 10) / 10,
      level,
      avgSentenceLength: Math.round(avgSentenceLength * 10) / 10,
      avgSyllables: Math.round(avgSyllablesPerWord * 100) / 100
    };
  }

  /**
   * Apply algorithmic humanization to content to reduce AI-detection signals.
   *
   * Varies sentence length, inserts contractions, breaks uniform paragraph rhythm,
   * adds occasional colloquial transitions, and introduces natural imperfections.
   *
   * @param {string} content - Markdown blog content to humanize.
   * @returns {string} Modified content string.
   */
  humanize(content) {
    if (!content || content.trim().length === 0) {
      return content;
    }

    // Work paragraph by paragraph, preserving markdown structure
    const lines = content.split('\n');
    const result = [];
    let i = 0;

    while (i < lines.length) {
      const line = lines[i];

      // Preserve headings, code blocks, lists, front matter, horizontal rules
      if (
        /^#{1,6}\s+/.test(line) ||
        /^```/.test(line) ||
        /^---/.test(line) ||
        /^>\s+/.test(line) ||
        line.trim() === ''
      ) {
        // For headings, just pass through
        result.push(line);
        i++;
        continue;
      }

      // Check if we're in a code block
      if (/^```/.test(line)) {
        result.push(line);
        i++;
        while (i < lines.length && !/^```/.test(lines[i])) {
          result.push(lines[i]);
          i++;
        }
        if (i < lines.length) {
          result.push(lines[i]);
          i++;
        }
        continue;
      }

      // Preserve list items but humanize their text
      if (/^[-*+]\s+/.test(line) || /^\d+\.\s+/.test(line)) {
        const prefix = line.match(/^([-*+]\s+|\d+\.\s+)/)[0];
        const text = line.substring(prefix.length);
        result.push(prefix + this._humanizeParagraph(text));
        i++;
        continue;
      }

      // Regular paragraph text — collect consecutive non-empty, non-structural lines
      let paragraph = line;
      i++;
      while (
        i < lines.length &&
        lines[i].trim() !== '' &&
        !/^#{1,6}\s+/.test(lines[i]) &&
        !/^```/.test(lines[i]) &&
        !/^---/.test(lines[i]) &&
        !/^[-*+]\s+/.test(lines[i]) &&
        !/^\d+\.\s+/.test(lines[i]) &&
        !/^>\s+/.test(lines[i])
      ) {
        paragraph += ' ' + lines[i];
        i++;
      }

      result.push(this._humanizeParagraph(paragraph));
    }

    // Post-pass: break up paragraphs that are too uniform in length
    let finalResult = this._varyParagraphRhythm(result.join('\n'));

    return finalResult;
  }

  /**
   * Generate blog posts for multiple topics in sequence.
   *
   * Calls generate() for each topic with a 500ms delay between calls to avoid rate limits.
   *
   * @async
   * @param {Array<string>} topics - Array of topic strings.
   * @param {Object} [options={}] - Options passed to generate() (excluding topic).
   * @returns {Promise<Array<{topic: string, result?: Object, error?: string}>>} Array of results, one per topic.
   */
  async batch(topics, options = {}) {
    if (!Array.isArray(topics) || topics.length === 0) {
      throw new Error('BlogForge.batch() requires a non-empty array of topics.');
    }

    const results = [];

    for (let i = 0; i < topics.length; i++) {
      const topic = topics[i];

      try {
        const result = await this.generate({ ...options, topic });
        results.push({ topic, result });
      } catch (err) {
        results.push({ topic, error: err.message || String(err) });
      }

      // Delay between calls (except after the last one)
      if (i < topics.length - 1) {
        await this._delay(500);
      }
    }

    return results;
  }

  /**
   * Publish content to a blogging platform.
   *
   * @async
   * @param {string} content - The blog post content (Markdown or HTML depending on platform).
   * @param {string} platform - Target platform: 'medium', 'wordpress', or 'ghost'.
   * @param {Object} credentials - Platform-specific credentials.
   * @param {string} [credentials.token] - Medium integration token.
   * @param {string} [credentials.url] - WordPress or Ghost site URL.
   * @param {string} [credentials.username] - WordPress username.
   * @param {string} [credentials.appPassword] - WordPress application password.
   * @param {string} [credentials.adminApiKey] - Ghost Admin API key (format: "id:secret").
   * @param {string} [credentials.title] - Optional title override.
   * @returns {Promise<{success: boolean, url: string, id: string, platform: string}>}
   * @throws {Error} If platform is unsupported, credentials are missing, or API call fails.
   */
  async publish(content, platform, credentials = {}) {
    if (!content || content.trim().length === 0) {
      throw new Error('BlogForge.publish() requires non-empty content.');
    }

    if (!platform) {
      throw new Error('BlogForge.publish() requires a platform ("medium", "wordpress", or "ghost").');
    }

    // Extract title from content if not provided
    const titleMatch = content.match(/^#\s+(.+)$/m);
    const title = credentials.title || (titleMatch ? titleMatch[1].trim() : 'Untitled Post');

    switch (platform) {
      case 'medium':
        return this._publishMedium(content, title, credentials);
      case 'wordpress':
        return this._publishWordPress(content, title, credentials);
      case 'ghost':
        return this._publishGhost(content, title, credentials);
      default:
        throw new Error(`BlogForge.publish() does not support platform "${platform}". Use "medium", "wordpress", or "ghost".`);
    }
  }

  // ──────────────────────────────────────────────────
  // PRIVATE HELPER METHODS
  // ──────────────────────────────────────────────────

  /**
   * Count syllables in a word using a heuristic algorithm.
   * @private
   * @param {string} word
   * @returns {number}
   */
  _countSyllables(word) {
    const w = word.toLowerCase().replace(/[^a-z]/g, '');
    if (w.length <= 2) return 1;

    let count = 0;
    const vowels = 'aeiouy';
    let prevVowel = false;

    for (let i = 0; i < w.length; i++) {
      const isVowel = vowels.includes(w[i]);
      if (isVowel && !prevVowel) {
        count++;
      }
      prevVowel = isVowel;
    }

    // Subtract silent 'e' at end
    if (w.endsWith('e') && !w.endsWith('le') && count > 1) {
      count--;
    }

    // Handle special endings
    if (w.endsWith('le') && w.length > 2 && !vowels.includes(w[w.length - 3])) {
      
      count++;
    }

    return Math.max(count, 1);
  }

  // ---------------------------------------------------------------------------
  // 2. _resolveApiKey
  // ---------------------------------------------------------------------------
  _resolveApiKey(model) {
    if (model.startsWith('anthropic/')) {
      const key = process['env'].ANTHROPIC_API_KEY;
      if (!key) {
        throw new Error(
          'ANTHROPIC_API_KEY environment variable is required for Anthropic models. ' +
          'Set it in your environment or .env file.'
        );
      }
      return key;
    }

    if (model.startsWith('openai/')) {
      const key = process['env'].OPENAI_API_KEY;
      if (!key) {
        throw new Error(
          'OPENAI_API_KEY environment variable is required for OpenAI models. ' +
          'Set it in your environment or .env file.'
        );
      }
      return key;
    }

    if (model.startsWith('ollama/')) {
      return null;
    }

    throw new Error(
      `Unknown model provider prefix in "${model}". ` +
      'Expected "anthropic/", "openai/", or "ollama/".'
    );
  }

  // ---------------------------------------------------------------------------
  // 3. _callAnthropic
  // ---------------------------------------------------------------------------
  async _callAnthropic(modelName, _genInstructions, apiKey) {
    const body = JSON.stringify({
      model: modelName,
      max_tokens: 4096,
      system: _genInstructions,
      messages: [{ role: 'user', content: 'Write the blog post now.' }]
    });

    const response = await this._httpRequest(
      {
        hostname: 'api.anthropic.com',
        path: '/v1/messages',
        method: 'POST',
        headers: {
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'content-type': 'application/json',
          'content-length': Buffer.byteLength(body)
        }
      },
      body
    );

    let parsed;
    try {
      parsed = JSON.parse(response.data);
    } catch (e) {
      throw new Error(
        `Anthropic API returned non-JSON response (HTTP ${response.statusCode}): ${response.data.slice(0, 500)}`
      );
    }

    if (response.statusCode !== 200) {
      const msg = parsed.error?.message || parsed.message || response.data.slice(0, 500);
      throw new Error(
        `Anthropic API error (HTTP ${response.statusCode}): ${msg}`
      );
    }

    if (!parsed.content || !parsed.content[0] || !parsed.content[0].text) {
      throw new Error(
        'Anthropic API returned an unexpected response structure: missing content[0].text'
      );
    }

    return parsed.content[0].text;
  }

  // ---------------------------------------------------------------------------
  // 4. _callOpenAI
  // ---------------------------------------------------------------------------
  async _callOpenAI(modelName, _genInstructions, apiKey) {
    const body = JSON.stringify({
      model: modelName,
      max_tokens: 4096,
      messages: [
        { role: 'system', content: _genInstructions },
        { role: 'user', content: 'Write the blog post now.' }
      ]
    });

    const response = await this._httpRequest(
      {
        hostname: 'api.openai.com',
        path: '/v1/chat/completions',
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${apiKey}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body)
        }
      },
      body
    );

    let parsed;
    try {
      parsed = JSON.parse(response.data);
    } catch (e) {
      throw new Error(
        `OpenAI API returned non-JSON response (HTTP ${response.statusCode}): ${response.data.slice(0, 500)}`
      );
    }

    if (response.statusCode !== 200) {
      const msg = parsed.error?.message || parsed.message || response.data.slice(0, 500);
      throw new Error(
        `OpenAI API error (HTTP ${response.statusCode}): ${msg}`
      );
    }

    if (!parsed.choices || !parsed.choices[0] || !parsed.choices[0].message || !parsed.choices[0].message.content) {
      throw new Error(
        'OpenAI API returned an unexpected response structure: missing choices[0].message.content'
      );
    }

    return parsed.choices[0].message.content;
  }

  // ---------------------------------------------------------------------------
  // 5. _callOllama
  // ---------------------------------------------------------------------------
  async _callOllama(modelName, _genInstructions) {
    const body = JSON.stringify({
      model: modelName,
      stream: false,
      messages: [
        { role: 'system', content: _genInstructions },
        { role: 'user', content: 'Write the blog post now.' }
      ]
    });

    let response;
    try {
      response = await this._httpRequest(
        {
          protocol: 'http:',
          hostname: '127.0.0.1',
          port: 11434,
          path: '/api/chat',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body)
          }
        },
        body
      );
    } catch (e) {
      throw new Error(
        `Failed to connect to Ollama at 127.0.0.1:11434. Is Ollama running? Original error: ${e.message}`
      );
    }

    let parsed;
    try {
      parsed = JSON.parse(response.data);
    } catch (e) {
      throw new Error(
        `Ollama returned non-JSON response (HTTP ${response.statusCode}): ${response.data.slice(0, 500)}`
      );
    }

    if (response.statusCode !== 200) {
      const msg = parsed.error || parsed.message || response.data.slice(0, 500);
      throw new Error(
        `Ollama API error (HTTP ${response.statusCode}): ${msg}`
      );
    }

    if (!parsed.message || !parsed.message.content) {
      throw new Error(
        'Ollama returned an unexpected response structure: missing message.content'
      );
    }

    return parsed.message.content;
  }

  // ---------------------------------------------------------------------------
  // 6. _publishMedium
  // ---------------------------------------------------------------------------
  async _publishMedium(content, title, credentials) {
    const { token } = credentials;

    // Step 1: Get authenticated user ID
    const meResponse = await this._httpRequest(
      {
        hostname: 'api.medium.com',
        path: '/v1/me',
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
      },
      null
    );

    let meData;
    try {
      meData = JSON.parse(meResponse.data);
    } catch (e) {
      throw new Error(
        `Medium /v1/me returned non-JSON response (HTTP ${meResponse.statusCode}): ${meResponse.data.slice(0, 500)}`
      );
    }

    if (meResponse.statusCode !== 200 || !meData.data || !meData.data.id) {
      const msg = meData.errors?.[0]?.message || meData.message || meResponse.data.slice(0, 500);
      throw new Error(
        `Medium authentication failed (HTTP ${meResponse.statusCode}): ${msg}`
      );
    }

    const userId = meData.data.id;

    // Step 2: Create the post
    const postBody = JSON.stringify({
      title,
      contentFormat: 'markdown',
      content,
      publishStatus: 'draft'
    });

    const postResponse = await this._httpRequest(
      {
        hostname: 'api.medium.com',
        path: `/v1/users/${userId}/posts`,
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Content-Length': Buffer.byteLength(postBody)
        }
      },
      postBody
    );

    let postData;
    try {
      postData = JSON.parse(postResponse.data);
    } catch (e) {
      throw new Error(
        `Medium post creation returned non-JSON response (HTTP ${postResponse.statusCode}): ${postResponse.data.slice(0, 500)}`
      );
    }

    if (postResponse.statusCode !== 201 && postResponse.statusCode !== 200) {
      const msg = postData.errors?.[0]?.message || postData.message || postResponse.data.slice(0, 500);
      throw new Error(
        `Medium post creation failed (HTTP ${postResponse.statusCode}): ${msg}`
      );
    }

    return {
      success: true,
      url: postData.data.url,
      id: postData.data.id,
      platform: 'medium'
    };
  }

  // ---------------------------------------------------------------------------
  // 7. _publishWordPress
  // ---------------------------------------------------------------------------
  async _publishWordPress(content, title, credentials) {
    const { url, username, appPassword } = credentials;

    // Convert markdown to basic HTML
    const htmlContent = this._markdownToBasicHtml(content);

    const auth = Buffer.from(`${username}:${appPassword}`).toString('base64');

    const parsedUrl = new URL(url);

    const postBody = JSON.stringify({
      title,
      content: htmlContent,
      status: 'draft'
    });

    const response = await this._httpRequest(
      {
        protocol: parsedUrl.protocol,
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
        path: `${parsedUrl.pathname.replace(/\/$/, '')}/wp-json/wp/v2/posts`,
        method: 'POST',
        headers: {
          'Authorization': `Basic ${auth}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(postBody)
        }
      },
      postBody
    );

    let parsed;
    try {
      parsed = JSON.parse(response.data);
    } catch (e) {
      throw new Error(
        `WordPress API returned non-JSON response (HTTP ${response.statusCode}): ${response.data.slice(0, 500)}`
      );
    }

    if (response.statusCode !== 201 && response.statusCode !== 200) {
      const msg = parsed.message || parsed.data?.message || response.data.slice(0, 500);
      throw new Error(
        `WordPress post creation failed (HTTP ${response.statusCode}): ${msg}`
      );
    }

    return {
      success: true,
      url: parsed.link,
      id: String(parsed.id),
      platform: 'wordpress'
    };
  }

  /**
   * Simple markdown-to-HTML conversion for WordPress.
   */
  _markdownToBasicHtml(md) {
    let html = md;

    // Convert headers: # through ######
    html = html.replace(/^######\s+(.+)$/gm, '<h6>$1</h6>');
    html = html.replace(/^#####\s+(.+)$/gm, '<h5>$1</h5>');
    html = html.replace(/^####\s+(.+)$/gm, '<h4>$1</h4>');
    html = html.replace(/^###\s+(.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^##\s+(.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^#\s+(.+)$/gm, '<h1>$1</h1>');

    // Convert bold **text** and __text__
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/__(.+?)__/g, '<strong>$1</strong>');

    // Convert italic *text* and _text_
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    html = html.replace(/_(.+?)_/g, '<em>$1</em>');

    // Convert unordered lists
    html = html.replace(/^[-*]\s+(.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, (match) => `<ul>\n${match}</ul>\n`);

    // Convert inline code
    html = html.replace(/`(.+?)`/g, '<code>$1</code>');

    // Convert links [text](url)
    html = html.replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2">$1</a>');

    // Wrap remaining plain-text paragraphs (lines not already wrapped in HTML tags)
    const lines = html.split('\n\n');
    html = lines
      .map((block) => {
        const trimmed = block.trim();
        if (!trimmed) return '';
        if (/^<(h[1-6]|ul|ol|li|blockquote|pre|div|p)/.test(trimmed)) {
          return trimmed;
        }
        return `<p>${trimmed.replace(/\n/g, '<br>')}</p>`;
      })
      .join('\n\n');

    return html;
  }

  // ---------------------------------------------------------------------------
  // 8. _publishGhost
  // ---------------------------------------------------------------------------
  async _publishGhost(content, title, credentials) {
    const crypto = require('crypto');
    const { url, adminApiKey } = credentials;

    // Parse the admin API key — format is "id:secret"
    const colonIdx = adminApiKey.indexOf(':');
    if (colonIdx === -1) {
      throw new Error(
        'Ghost Admin API key must be in "id:secret" format. Got: ' + adminApiKey.slice(0, 10) + '...'
      );
    }
    const id = adminApiKey.slice(0, colonIdx);
    const secret = adminApiKey.slice(colonIdx + 1);

    // Build JWT
    const now = Math.floor(Date.now() / 1000);

    const header = {
      alg: 'HS256',
      typ: 'JWT',
      kid: id
    };

    const payload = {
      iat: now,
      exp: now + 300,
      aud: '/admin/'
    };

    const base64url = (obj) => {
      let str;
      if (Buffer.isBuffer(obj)) {
        str = obj.toString('base64');
      } else {
        str = Buffer.from(JSON.stringify(obj)).toString('base64');
      }
      return str.replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
    };

    const headerB64 = base64url(header);
    const payloadB64 = base64url(payload);
    const signingInput = `${headerB64}.${payloadB64}`;

    const hmac = crypto.createHmac('sha256', Buffer.from(secret, 'hex'));
    hmac.update(signingInput);
    const signature = base64url(hmac.digest());

    const jwt = `${signingInput}.${signature}`;

    // Build lexical content
    const lexical = JSON.stringify({
      root: {
        children: [
          {
            children: [
              {
                detail: 0,
                format: 0,
                mode: 'normal',
                style: '',
                text: content,
                type: 'text',
                version: 1
              }
            ],
            direction: 'ltr',
            format: '',
            indent: 0,
            type: 'paragraph',
            version: 1
          }
        ],
        direction: 'ltr',
        format: '',
        indent: 0,
        type: 'root',
        version: 1
      }
    });

    const postBody = JSON.stringify({
      posts: [
        {
          title,
          lexical,
          status: 'draft'
        }
      ]
    });

    const parsedUrl = new URL(url);

    const response = await this._httpRequest(
      {
        protocol: parsedUrl.protocol,
        hostname: parsedUrl.hostname,
        port: parsedUrl.port || (parsedUrl.protocol === 'https:' ? 443 : 80),
        path: `${parsedUrl.pathname.replace(/\/$/, '')}/ghost/api/admin/posts/`,
        method: 'POST',
        headers: {
          'Authorization': `Ghost ${jwt}`,
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(postBody)
        }
      },
      postBody
    );

    let parsed;
    try {
      parsed = JSON.parse(response.data);
    } catch (e) {
      throw new Error(
        `Ghost API returned non-JSON response (HTTP ${response.statusCode}): ${response.data.slice(0, 500)}`
      );
    }

    if (response.statusCode !== 201 && response.statusCode !== 200) {
      const msg =
        parsed.errors?.[0]?.message ||
        parsed.message ||
        response.data.slice(0, 500);
      throw new Error(
        `Ghost post creation failed (HTTP ${response.statusCode}): ${msg}`
      );
    }

    if (!parsed.posts || !parsed.posts[0]) {
      throw new Error(
        'Ghost API returned unexpected response structure: missing posts[0]'
      );
    }

    return {
      success: true,
      url: parsed.posts[0].url,
      id: parsed.posts[0].id,
      platform: 'ghost'
    };
  }

  // ---------------------------------------------------------------------------
  // 9. _humanizeParagraph
  // ---------------------------------------------------------------------------
  _humanizeParagraph(text) {
    if (!text || !text.trim()) return text;

    let result = text;

    // Probabilistic contractions (~60% of the time)
    const contractions = [
      { pattern: /\bis not\b/gi, replacement: "isn't" },
      { pattern: /\bdo not\b/gi, replacement: "don't" },
      { pattern: /\bcan\s?not\b/gi, replacement: "can't" },
      { pattern: /\bwill not\b/gi, replacement: "won't" },
      { pattern: /\bdoes not\b/gi, replacement: "doesn't" },
      { pattern: /\bdid not\b/gi, replacement: "didn't" },
      { pattern: /\bit is\b/gi, replacement: "it's" },
      { pattern: /\bthat is\b/gi, replacement: "that's" },
      { pattern: /\bthere is\b/gi, replacement: "there's" }
    ];

    for (const { pattern, replacement } of contractions) {
      result = result.replace(pattern, (match) => {
        if (Math.random() < 0.6) {
          // Preserve capitalization of first character
          if (match[0] === match[0].toUpperCase()) {
            return replacement.charAt(0).toUpperCase() + replacement.slice(1);
          }
          return replacement;
        }
        return match;
      });
    }

    // Split into sentences
    let sentences = result.match(/[^.!?]+[.!?]+[\s]*/g);
    if (!sentences || sentences.length === 0) {
      return result;
    }

    // Vary sentence length: if all sentences within 20% of average length, break one
    if (sentences.length >= 2) {
      const lengths = sentences.map((s) => s.trim().length);
      const avgLen = lengths.reduce((a, b) => a + b, 0) / lengths.length;
      const allSimilar = lengths.every(
        (l) => Math.abs(l - avgLen) / avgLen < 0.2
      );

      if (allSimilar) {
        // Find the longest sentence and try to break it
        let longestIdx = 0;
        let longestLen = 0;
        sentences.forEach((s, i) => {
          if (s.trim().length > longestLen) {
            longestLen = s.trim().length;
            longestIdx = i;
          }
        });

        const long = sentences[longestIdx].trim();

        // Try to break at comma, or at 'and'/'but' conjunction
        let breakIdx = -1;
        const midpoint = Math.floor(long.length / 2);

        // Search for a comma near the midpoint
        const commaRegex = /,\s/g;
        let bestComma = -1;
        let bestCommaDist = Infinity;
        let commaMatch;
        while ((commaMatch = commaRegex.exec(long)) !== null) {
          const dist = Math.abs(commaMatch.index - midpoint);
          if (dist < bestCommaDist) {
            bestCommaDist = dist;
            bestComma = commaMatch.index;
          }
        }

        // Search for conjunction near the midpoint
        const conjRegex = /\s(and|but)\s/gi;
        let bestConj = -1;
        let bestConjDist = Infinity;
        let conjMatch;
        while ((conjMatch = conjRegex.exec(long)) !== null) {
          const dist = Math.abs(conjMatch.index - midpoint);
          if (dist < bestConjDist) {
            bestConjDist = dist;
            bestConj = conjMatch.index;
          }
        }

        if (bestComma > 0 && bestCommaDist <= bestConjDist) {
          breakIdx = bestComma + 1; // after the comma
        } else if (bestConj > 0) {
          breakIdx = bestConj + 1; // at the conjunction space
        }

        if (breakIdx > 0 && breakIdx < long.length - 5) {
          const firstPart = long.slice(0, breakIdx).trim();
          const secondPart = long.slice(breakIdx).trim();

          // Ensure the first part ends with punctuation
          const firstSentence = firstPart.endsWith('.') || firstPart.endsWith('!') || firstPart.endsWith('?')
            ? firstPart
            : firstPart + '.';
          const secondSentence =
            secondPart.charAt(0).toUpperCase() + secondPart.slice(1);

          sentences[longestIdx] = firstSentence + ' ' + secondSentence + ' ';
        }
      }
    }

    // Add occasional transition at the start
    const transitions = [
      "Here's the thing: ",
      'Put simply: ',
      'In practice, ',
      'The truth is, '
    ];

    if (sentences.length > 3 && Math.random() < 0.3) {
      const transition =
        transitions[Math.floor(Math.random() * transitions.length)];
      // Lowercase the first character of the first sentence after the transition
      const first = sentences[0].trim();
      sentences[0] =
        transition +
        first.charAt(0).toLowerCase() +
        first.slice(1) +
        ' ';
    }

    return sentences.join('').trim();
  }

  // ---------------------------------------------------------------------------
  // 10. _varyParagraphRhythm
  // ---------------------------------------------------------------------------
  _varyParagraphRhythm(text) {
    if (!text) return text;

    const paragraphs = text.split(/\n\n+/);
    if (paragraphs.length < 3) return text;

    const lengths = paragraphs.map((p) => p.trim().length);

    // Find runs of 3+ consecutive paragraphs with similar length (within 15%)
    let i = 0;
    while (i < paragraphs.length) {
      let runStart = i;
      let runEnd = i;

      // Calculate average for this potential run starting at i
      while (runEnd < paragraphs.length - 1) {
        const runLengths = lengths.slice(runStart, runEnd + 2);
        const avg = runLengths.reduce((a, b) => a + b, 0) / runLengths.length;

        if (avg === 0) break;

        const allSimilar = runLengths.every(
          (l) => Math.abs(l - avg) / avg < 0.15
        );

        if (allSimilar) {
          runEnd++;
        } else {
          break;
        }
      }

      const runLength = runEnd - runStart + 1;

      if (runLength >= 3) {
        // Pick a paragraph in the middle of the run to split
        const splitIdx = runStart + Math.floor(runLength / 2);
        const para = paragraphs[splitIdx];

        // Find a sentence boundary near the middle
        const sentenceBreaks = [];
        const sentenceRegex = /[.!?]\s+/g;
        let match;
        while ((match = sentenceRegex.exec(para)) !== null) {
          sentenceBreaks.push(match.index + 1);
        }

        if (sentenceBreaks.length >= 2) {
          // Find the break closest to the midpoint
          const midpoint = Math.floor(para.length / 2);
          let bestBreak = sentenceBreaks[0];
          let bestDist = Math.abs(sentenceBreaks[0] - midpoint);

          for (const brk of sentenceBreaks) {
            const dist = Math.abs(brk - midpoint);
            if (dist < bestDist) {
              bestDist = dist;
              bestBreak = brk;
            }
          }

          const firstHalf = para.slice(0, bestBreak).trim();
          const secondHalf = para.slice(bestBreak).trim();

          if (firstHalf && secondHalf) {
            paragraphs.splice(splitIdx, 1, firstHalf, secondHalf);
            // Update lengths array accordingly
            lengths.splice(
              splitIdx,
              1,
              firstHalf.length,
              secondHalf.length
            );
          }
        }

        // Skip past this run to avoid infinite loops
        i = runEnd + 2;
      } else {
        i++;
      }
    }

    return paragraphs.join('\n\n');
  }

  // ---------------------------------------------------------------------------
  // 11. _delay
  // ---------------------------------------------------------------------------
  _delay(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }

  // ---------------------------------------------------------------------------
  // 12. _httpRequest
  // ---------------------------------------------------------------------------
  _httpRequest(options, body) {
    return new Promise((resolve, reject) => {
      const protocol = options.protocol === 'http:' ? require('http') : require('https');

      const reqOptions = {
        hostname: options.hostname,
        port: options.port || (options.protocol === 'http:' ? 80 : 443),
        path: options.path,
        method: options.method || 'GET',
        headers: options.headers || {}
      };

      const req = protocol.request(reqOptions, (res) => {
        const chunks = [];

        res.on('data', (chunk) => {
          chunks.push(chunk);
        });

        res.on('end', () => {
          const data = Buffer.concat(chunks).toString('utf8');
          resolve({
            statusCode: res.statusCode,
            data
          });
        });
      });

      req.on('error', (err) => {
        reject(new Error(`HTTP request failed: ${err.message}`));
      });

      // Set a timeout of 120 seconds for LLM calls which can be slow
      req.setTimeout(120000, () => {
        req.destroy();
        reject(new Error('HTTP request timed out after 120 seconds'));
      });

      if (body) {
        req.write(body);
      }

      req.end();
    });
  }
}

module.exports = BlogForge;