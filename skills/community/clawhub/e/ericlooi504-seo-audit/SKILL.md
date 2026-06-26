---
name: GTS_seo-audit-optimizer
description: Analyze and improve website content for search engines. Guides users through checklist-based reviews of title tags, meta descriptions, headers, content quality, and readability. Best for website owners, bloggers, and small businesses who want actionable SEO recommendations without expensive tools.
version: 1.0.2
metadata:
  openclaw:
    requires:
      bins: []
    emoji: "🔍"
---

# GTS SEO Audit & Optimizer

Guide users through content analysis for search engine optimization. Generate checklists, recommendations, and improvement tracking — all through natural conversation.

## Example Prompts

> *"Analyze the SEO of example.com"*
> *"What should I check for my website's SEO?"*
> *"Give me an SEO review checklist"*
> *"List SEO improvements for my blog"*
> *"Compare SEO readiness of my site vs a competitor"*

## How It Works

The agent performs content analysis by visiting URLs with the built-in web browser and examining visible page elements — no automated crawling, no scanning tools needed.

### 1. Content Analysis Checklist

The agent checks these visible elements on the page and provides feedback:

**Page Content**
- Title tag — present, descriptive, appropriate length
- Meta description — present and compelling
- Heading tags — proper structure starting with H1
- Content — appropriate length and readability
- Images — present with descriptive text
- Internal links — relevant and functional

**Technical Setup**
- robots.txt and sitemap.xml file locations
- HTTPS connection
- Viewport meta tag for mobile
- Page loading timeframe

**Content Quality**
- Primary topic identification
- Related terms used naturally
- Content update freshness
- Readability level

### 2. Recommendation Format

The agent provides suggestions in a clear checklist:

```
🔍 SEO Review: example.com

✅ Title tag: Good (55 chars, includes target topic)
✅ H1 heading: Found
⚠️ Meta description: Missing — add 150-160 character summary
⚠️ Word count: 180 — recommended minimum 300
❌ Images missing alt text: 3 images affected

📋 Priority Actions:
  1. Add meta description to each page
  2. Add descriptive text to images
  3. Expand content to 300+ words
```

### 3. Tracking Progress

The agent can compare current and previous reviews:
- "How does my SEO look compared to last month?"
- "Show me my SEO improvement trend"
- "Create a weekly SEO checklist"

## Comparison Feature

When the user asks to compare with a competitor:

1. Visit both URLs with web browser
2. Compare visible page elements side by side
3. Identify gaps and opportunities
4. Present findings as a comparison table

## Best Practices Shared

The agent shares general web publishing best practices:
- Create descriptive, unique page titles
- Write clear meta summaries for each page
- Use headings in logical order (one H1 per page)
- Include relevant terms naturally in content
- Ensure pages work well on mobile devices
- Use HTTPS for secure connections
- Keep content updated and fresh

## Limitations

This skill provides analysis and recommendations based on visible page content. It does not:
- Access Google Analytics or Search Console data
- Run automated crawling tools
- Check server configuration details
- Use external SEO API services
