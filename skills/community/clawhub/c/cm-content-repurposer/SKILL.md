---
name: content-repurposer
description: Repurpose long-form content (blog posts, articles, newsletters, YouTube transcripts) into platform-optimized social media posts, Twitter/X threads, LinkedIn posts, email newsletter snippets, and short-form summaries. Use when asked to repurpose content, turn an article into social posts, create a thread from a blog post, adapt content for different platforms, generate social media versions of existing content, or create multi-platform content from a single source. Triggers on "repurpose", "turn this into tweets", "make social posts from", "create a thread", "adapt for LinkedIn", "newsletter snippet", "content remix".
---

# Content Repurposer

Transform any long-form content into platform-optimized outputs. Feed it a URL, text, or document — get back ready-to-post content for multiple platforms.

## Workflow

### 1. Extract Source Content

Determine the source type and extract content:

- **URL** → Use `web_fetch` to extract readable text
- **YouTube URL** → Use youtube-transcript skill if available, otherwise `web_fetch`
- **Pasted text** → Use directly
- **File path** → Read the file (supports .md, .txt, .html, .pdf)

If extraction fails, inform the user and suggest alternatives.

### 2. Analyze Content

Before generating outputs, analyze the source:

1. **Core message** — What is the single main takeaway?
2. **Key points** — List 3-5 supporting points or insights
3. **Quotable lines** — Extract 2-3 memorable phrases or statistics
4. **Target audience** — Infer from tone, vocabulary, and subject matter
5. **Content type** — Tutorial, opinion, news, case study, announcement, story

### 3. Generate Platform Outputs

Generate requested formats (default: all). Each format follows platform-specific rules from `references/platform-guides.md`.

**Available formats:**
- **Twitter/X thread** — 3-10 tweets, hook-first, one idea per tweet
- **Twitter/X single post** — Standalone tweet, max 280 chars
- **LinkedIn post** — Professional tone, 1300 chars max, uses line breaks for readability
- **Instagram caption** — Casual tone, hashtags, emoji-friendly, CTA at end
- **Email newsletter snippet** — 2-3 paragraphs, subject line included
- **Short summary** — 2-3 sentences, platform-agnostic
- **Reddit post** — Title + body, informative tone, no self-promotion feel
- **Hacker News** — Title only (concise, factual), optional top-level comment

### 4. Apply Tone & Style

If user specifies a tone or brand voice, apply it. Otherwise, match the source's tone but optimize for each platform's conventions.

Tone options: professional, casual, witty, authoritative, friendly, provocative, educational.

### 5. Output Format

Present outputs in clear sections:

```
## Source Analysis
- Core message: ...
- Key points: ...

## Twitter/X Thread (N tweets)
🧵 1/ [hook tweet]
2/ [supporting point]
...

## LinkedIn Post
[post content]

## Email Newsletter
Subject: ...
[body]
```

## Customization Options

Users can specify:
- **Platforms** — "just Twitter and LinkedIn"
- **Tone** — "make it casual" / "keep it professional"
- **Audience** — "targeting developers" / "for marketing managers"
- **Length** — "keep the thread short, 3-4 tweets max"
- **CTA** — "include a link to [URL]" / "ask them to subscribe"
- **Hashtags** — "include hashtags" / "no hashtags"
- **Emoji** — "use emojis" / "no emojis"
- **Language** — generate in specified language

## Platform Guides

For detailed platform-specific formatting rules, character limits, and best practices, see `references/platform-guides.md`.

## Tips

- When repurposing tutorials: focus on the "aha moment" or key insight, not the step-by-step
- When repurposing news: lead with impact/consequence, not the event itself
- When repurposing case studies: lead with the result, then the method
- For threads: each tweet should work standalone — readers may see any single tweet
- Always adapt vocabulary and jargon level to the target platform's audience
