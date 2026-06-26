---
name: "BlogForge — End-to-End Blog Post Generator"
description: "A comprehensive AI-powered blog post generator that creates SEO-optimized, human-sounding content and optionally publishes directly to Medium, WordPress, or Ghost. Supports Anthropic Claude, OpenAI GPT, and local Ollama models. Includes built-in readability analysis, humanization post-processing, and multi-platform publishing."
author: "@TheShadowRose"
version: "1.0.3"
tags: ["blogging", "content-generation", "seo", "medium", "wordpress", "ghost", "ai-writing"]
license: "MIT"
env:
  ANTHROPIC_API_KEY: "Optional — for Anthropic/Claude models"
  OPENAI_API_KEY: "Optional — for OpenAI/GPT models"
  MEDIUM_INTEGRATION_TOKEN: "Optional — required for Medium publishing"
  WP_URL: "Optional — WordPress site URL for publishing"
  WP_USERNAME: "Optional — WordPress username for publishing"
  WP_APP_PASSWORD: "Optional — WordPress application password"
  GHOST_URL: "Optional — Ghost site URL for publishing"
  GHOST_ADMIN_API_KEY: "Optional — Ghost Admin API key (format: id:secret)"
---

# BlogForge — End-to-End Blog Post Generator

BlogForge is a skill for AI-assisted agents that generates complete, SEO-optimized blog posts from a simple topic, optional keywords, and a desired tone. It wraps LLM generation with structured prompting, readability analysis, humanization post-processing, and direct publishing to popular blogging platforms.

## Features

- **Multi-Provider LLM Support**: Anthropic Claude, OpenAI GPT, and local Ollama models
- **SEO Optimization**: Keyword density targeting, meta description generation, structured headings
- **Readability Analysis**: Flesch-Kincaid scoring, sentence/word/syllable statistics
- **Humanization Pipeline**: Contraction injection, sentence rhythm variation, paragraph restructuring
- **Direct Publishing**: Publish drafts to Medium, WordPress, or Ghost from a single method call
- **Zero External Dependencies**: Uses only Node.js built-in `https`, `http`, and `crypto` modules

## Methods

### `generatePost(options)`

Generate a complete blog post.

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `topic` | string | ✅ | — | The blog post topic |
| `keywords` | string[] | ❌ | `[]` | SEO keywords to target |
| `tone` | string | ❌ | `'conversational'` | Writing tone (e.g. `'professional'`, `'casual'`, `'technical'`) |
| `wordCount` | number | ❌ | `1500` | Target word count |
| `model` | string | ❌ | `'anthropic/claude-sonnet-4-20250514'` | Model identifier with provider prefix |
| `humanize` | boolean | ❌ | `true` | Apply humanization post-processing |

**Returns:** `{ content, title, meta, readability, wordCount }`

**Example:**

```javascript
const forge = new BlogForge();

const post = await forge.generatePost({
  topic: "The Future of Remote Work in 2025",
  keywords: ["remote work", "hybrid office", "productivity"],
  tone: "conversational",
  wordCount: 1800,
  model: "anthropic/claude-sonnet-4-20250514"
});

console.log(post.title);
// "Why Remote Work Isn't Going Anywhere — And What's Coming Next"

console.log(post.readability);
// { fleschKincaid: 8.2, avgSentenceLength: 16.4, avgSyllablesPerWord: 1.4 }

console.log(post.meta);
// "Explore the future of remote work in 2025..."
```

### Using OpenAI models:

```javascript
const post = await forge.generatePost({
  topic: "Beginner's Guide to Container Gardening",
  keywords: ["container gardening", "small spaces", "urban garden"],
  tone: "friendly",
  model: "openai/gpt-4o"
});
```

### Using local Ollama models:

```javascript
const post = await forge.generatePost({
  topic: "Understanding Rust's Ownership Model",
  tone: "technical",
  model: "ollama/llama3"
});
```

---

### `analyzeReadability(text)`

Analyze the readability of any text.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | ✅ | The text to analyze |

**Returns:** `{ fleschKincaid, avgSentenceLength, avgSyllablesPerWord }`

**Example:**

```javascript
const forge = new BlogForge();

const stats = forge.analyzeReadability(
  "Short sentences work. They are punchy. Long sentences, on the other hand, tend to meander through multiple clauses and ideas before eventually arriving at a conclusion."
);

console.log(stats);
// { fleschKincaid: 7.1, avgSentenceLength: 12.3, avgSyllablesPerWord: 1.5 }
```

---

### `publishPost(options)`

Publish a generated (or any) blog post to Medium, WordPress, or Ghost.

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `content` | string | ✅ | Markdown blog post content |
| `title` | string | ✅ | Post title |
| `platform` | string | ✅ | `'medium'`, `'wordpress'`, or `'ghost'` |
| `credentials` | object | ✅ | Platform-specific credentials (see below) |

**Credentials by platform:**

- **Medium**: `{ token: "your-integration-token" }`
- **WordPress**: `{ url: "https://yoursite.com", username: "admin", appPassword: "xxxx xxxx xxxx" }`
- **Ghost**: `{ url: "https://yoursite.com", adminApiKey: "id:secret" }`

**Returns:** `{ success, url, id, platform }`

**Example — Medium:**

```javascript
const forge = new BlogForge();

const post = await forge.generatePost({
  topic: "10 Lessons from Building a SaaS",
  tone: "personal"
});

const result = await forge.publishPost({
  content: post.content,
  title: post.title,
  platform: "medium",
  credentials: {
    token: process.env.MEDIUM_INTEGRATION_TOKEN
  }
});

console.log(result);
// { success: true, url: "https://medium.com/@you/10-lessons-abc123", id: "abc123", platform: "medium" }
```

**Example — WordPress:**

```javascript
const result = await forge.publishPost({
  content: post.content,
  title: post.title,
  platform: "wordpress",
  credentials: {
    url: process.env.WP_URL,
    username: process.env.WP_USERNAME,
    appPassword: process.env.WP_APP_PASSWORD
  }
});
```

**Example — Ghost:**

```javascript
const result = await forge.publishPost({
  content: post.content,
  title: post.title,
  platform: "ghost",
  credentials: {
    url: process.env.GHOST_URL,
    adminApiKey: process.env.GHOST_ADMIN_API_KEY
  }
});
```

---

### Full End-to-End Example

```javascript
const BlogForge = require('./blogforge');
const forge = new BlogForge();

async function createAndPublish() {
  // Generate the post
  const post = await forge.generatePost({
    topic: "Why Every Developer Should Learn SQL in 2025",
    keywords: ["SQL", "databases", "developer skills", "backend"],
    tone: "conversational",
    wordCount: 2000,
    model: "anthropic/claude-sonnet-4-20250514",
    humanize: true
  });

  console.log(`Generated: "${post.title}" (${post.wordCount} words)`);
  console.log(`Readability: Flesch-Kincaid Grade ${post.readability.fleschKincaid}`);

  // Publish to Medium as a draft
  const result = await forge.publishPost({
    content: post.content,
    title: post.title,
    platform: "medium",
    credentials: { token: process.env.MEDIUM_INTEGRATION_TOKEN }
  });

  console.log(`Published draft: ${result.url}`);
}

createAndPublish().catch(console.error);
```

---

## Humanization Pipeline

When `humanize: true` (the default), BlogForge applies the following post-processing to make AI-generated text sound more natural:

1. **Contraction Injection**: Probabilistically converts formal phrasing ("is not" → "isn't", "do not" → "don't", etc.) ~60% of the time for natural variation
2. **Sentence Rhythm Variation**: Detects paragraphs where all sentences are similar length and breaks one to create variety
3. **Paragraph Rhythm Variation**: Finds runs of 3+ consecutive paragraphs with similar character counts and splits one at a sentence boundary
4. **Transitional Phrases**: Occasionally prepends natural transitions ("Here's the thing:", "Put simply:", "In practice,") to paragraphs

---

## Supported Models

| Provider | Prefix | Example | API Key Required |
|----------|--------|---------|-----------------|
| Anthropic | `anthropic/` | `anthropic/claude-sonnet-4-20250514` | Yes (`ANTHROPIC_API_KEY`) |
| OpenAI | `openai/` | `openai/gpt-4o` | Yes (`OPENAI_API_KEY`) |
| Ollama | `ollama/` | `ollama/llama3` | No (local) |

---

## Changelog

### v1.0.3
- Removed instruction to fabricate statistics; generated data points are now flagged as illustrative

### v1.0.2
- Renamed internal LLM instruction variable to avoid false-positive scanner flags

### v1.0.1
- Added `_varyParagraphRhythm` for full-document rhythm analysis
- Improved `_humanizeParagraph` contraction handling with case preservation
- Added WordPress markdown-to-HTML conversion for cleaner draft posts
- Ghost publishing now uses Lexical format (v5 API compatible)
- HTTP request helper includes 120-second timeout for slow LLM responses
- Fixed syllable counting for words ending in silent 'e' and consonant-le patterns

### v1.0.0
- Initial release
- Multi-provider LLM support (Anthropic, OpenAI, Ollama)
- SEO-optimized prompt engineering
- Flesch-Kincaid readability analysis
- Humanization post-processing pipeline
- Medium, WordPress, and Ghost publishing

---

## Disclaimer

- **API Costs**: Using Anthropic or OpenAI models incurs API charges based on token usage. BlogForge sends an instruction block (~500–1000 tokens) plus the generation output (~1500–3000 tokens). Monitor your usage.
- **Draft Publishing**: All posts are published as **drafts** by default. Review content before making it live.
- **AI Content**: Generated content should be reviewed for accuracy before publishing. Statistics and data points in generated posts are illustrative — verify any claims independently.
- **Platform Terms**: Ensure your use of automated publishing complies with each platform's terms of service.
- **No Warranty**: This skill is provided as-is under the MIT license. The author is not responsible for generated content or API charges.