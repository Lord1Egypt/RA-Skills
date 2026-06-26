---
name: Automate Content Repurposing with AI-driven Automation & Google Drive Storage
description: "Transform blog posts, articles, and long-form content into multiple formats—videos, podcasts, social media posts, and summaries. Use when the user needs content automation, multi-channel distribution, or quick content recycling."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"],
        "bins": []
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "♻️"
    }
  }
---

# AI-Powered Content Repurposing

## Overview

The **AI-Powered Content Repurposing** skill automatically transforms your existing content into multiple formats—turning a single blog post into video scripts, podcast episodes, social media threads, email sequences, and executive summaries. Perfect for content teams, marketers, and creators who want to maximize content ROI without manual rewriting.

### Why This Matters

Content creation is expensive. Repurposing is profitable. This skill uses advanced AI models (GPT-4o, Claude 3.5 Sonnet) to intelligently extract key takeaways, adapt tone for different platforms, and generate platform-optimized content in seconds—not hours.

**Integrations & Compatibility:**
- WordPress (auto-fetch posts via REST API)
- Google Drive & Docs (import source content)
- Slack (publish snippets to channels)
- LinkedIn, Twitter, Instagram (format-optimized outputs)
- HubSpot (sync repurposed content to CRM)
- Medium, Substack, Ghost (distribute multi-format posts)

---

## Quick Start

Copy and paste any of these prompts into your OpenClaw interface:

### Example 1: Blog Post → Social Media Bundle
```
Repurpose my blog post into:
- 3x LinkedIn posts (professional, 150 chars max each)
- 1x Twitter thread (10 tweets, conversational tone)
- 5x Instagram captions (casual, hashtag-rich)
- 1x TikTok script (30-60 seconds, energetic)

Blog URL: https://example.com/blog/ai-marketing-trends-2025
Include key statistics and actionable takeaways.
```

### Example 2: Long-Form Article → Video + Podcast Script
```
Transform this article into:
1. YouTube video script (8-minute talking points, B-roll cues)
2. Podcast episode transcript (conversational, 45 minutes)
3. Executive summary (200 words)
4. Quiz/interactive elements (3 questions testing listener comprehension)

Source: [Paste article text or provide URL]
Target audience: Marketing managers, ages 28-45
Tone: Authoritative but approachable
```

### Example 3: Batch Content Transformation
```
I have 5 blog posts in my WordPress site. Repurpose all of them into:
- Email newsletter sequences (3 emails per post)
- LinkedIn article versions (adapted for professional audience)
- Slack company updates (condensed to 2-3 messages)
- PDF one-pagers (visual summary format)

WordPress site: https://myblog.com
Category: "Product Launches"
Maintain brand voice: [Describe your brand tone]
```

---

## Capabilities

### 1. **Multi-Format Content Generation**
Transform a single source into unlimited formats:
- **Blog Posts** → LinkedIn articles, Medium posts, Substack newsletters
- **Long-Form Articles** → Video scripts, podcast transcripts, TED talk outlines
- **Whitepapers** → Infographic scripts, animated explainer concepts, LinkedIn carousels
- **Case Studies** → Email sequences, testimonial videos, success stories
- **Interviews** → Twitter threads, LinkedIn posts, podcast clips, quote graphics

**Example Usage:**
```
Transform "How to Optimize Landing Pages" blog post into:
- 15x social media posts (pre-scheduled content calendar)
- 2x video scripts (YouTube + TikTok versions)
- 3x email sequences (nurture, launch, retention)
- 1x podcast episode transcript
```

### 2. **Intelligent Key Takeaway Extraction**
Automatically identifies and summarizes the most important points:
- Extracts actionable insights for executive summaries
- Highlights statistics, frameworks, and data points
- Creates bullet-point versions for quick consumption
- Generates quiz questions testing core concepts

**Output Examples:**
- 30-second TL;DR versions
- One-page visual summaries
- Twitter-thread key points
- LinkedIn carousel slides

### 3. **Platform-Specific Tone & Format Optimization**
Adapts content for each platform's unique requirements:
- **LinkedIn**: Professional, data-driven, thought leadership
- **Twitter/X**: Punchy, conversation-starting, thread-friendly
- **TikTok/Instagram**: Casual, trendy, emoji-rich, hashtag-optimized
- **Email**: Scannable, CTA-focused, personalization tokens
- **YouTube**: Story-driven, retention cues, chapter markers
- **Podcasts**: Conversational, intro/outro hooks, natural pacing

### 4. **Batch Processing & Automation**
Process multiple pieces of content simultaneously:
- Import 5-50 blog posts from WordPress, Medium, or Google Drive
- Generate all formats for the entire batch in one workflow
- Create pre-scheduled content calendars for social media
- Sync outputs to HubSpot, Buffer, or Hootsuite

### 5. **Brand Voice Preservation**
Maintains consistent messaging across all formats:
- Analyze your existing content to learn brand voice
- Apply tone guidelines to all repurposed versions
- Ensure technical accuracy and message consistency
- Custom vocabulary and terminology handling

### 6. **SEO & Distribution Intelligence**
Optimizes repurposed content for discovery:
- Generates SEO-friendly titles, meta descriptions, and alt text
- Creates internal linking suggestions
- Suggests optimal posting times by platform
- Recommends hashtag and keyword placement

---

## Configuration

### Required Environment Variables
```bash
# OpenAI API key (GPT-4o for advanced repurposing)
OPENAI_API_KEY=sk-...

# Anthropic API key (Claude 3.5 Sonnet as backup/comparison)
ANTHROPIC_API_KEY=sk-ant-...

# Optional: For WordPress integration
WORDPRESS_API_URL=https://yourblog.com/wp-json
WORDPRESS_API_TOKEN=xxxxxxxxxxxx

# Optional: For Google Drive integration
GOOGLE_API_KEY=AIzaSy...

# Optional: For Slack notifications
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...
```

### Setup Instructions

1. **API Authentication**
   - Get your OpenAI API key from [platform.openai.com](https://platform.openai.com/api-keys)
   - Get your Anthropic key from [console.anthropic.com](https://console.anthropic.com)
   - Store securely in your environment or OpenClaw vault

2. **WordPress Integration** (Optional)
   - Enable REST API on your WordPress site
   - Generate API token: Settings → REST API → Create Token
   - Test connection: `curl https://yourblog.com/wp-json/wp/v2/posts`

3. **Default Configuration Options**
   ```yaml
   DEFAULT_MODEL: "gpt-4o"           # gpt-4-turbo or claude-3.5-sonnet
   BATCH_SIZE: 10                    # Max posts per batch
   OUTPUT_FORMATS: "all"             # Or specify: social,email,video,podcast
   PRESERVE_LINKS: true              # Keep source links in repurposed content
   INCLUDE_TIMESTAMPS: true          # Add publish dates to outputs
   TONE_ANALYSIS_DEPTH: "detailed"   # or "quick"
   ```

---

## Example Outputs

### Input: Blog Post
**Title:** "5 AI Tools That Will Replace Your Copywriter in 2025"
**Source:** 2,500-word article with 8 sections

### Generated Outputs

#### 1. LinkedIn Posts
```
🤖 Just researched the top 5 AI tools disrupting copywriting in 2025.

The surprising part? They're not replacements—they're force multipliers.

A human + GPT-4o + Claude = 3x faster, better copy.

Here's what I found... (thread) 🧵

→ Tool #1: Syntax optimization improved our email CTR by 23%
→ Tool #2: Tone consistency across 50+ brand channels
→ Tool #3: A/B copy variants in milliseconds
→ Tool #4: SEO keyword integration (zero awkwardness)
→ Tool #5: Multilingual expansion at scale

The real insight? The copywriter who uses AI 2x faster > copywriter without AI.

Thoughts?
```

#### 2. TikTok Script (60 seconds)
```
[HOOK - 0-3 sec]
"I tested 5 AI tools that are supposedly replacing copywriters.
Here's what ACTUALLY happened..." (text overlay)

[BODY - 3-45 sec]
- Quick clips of each tool interface
- Before/after copy examples
- Animated stat: "23% CTR improvement"
- Speed montage of generation

[OUTRO - 45-60 sec]
"The winner isn't AI or humans. It's both.
What's your experience? Comment below 👇"

[CTA - Text overlay]
"Link in bio for the full breakdown"
```

#### 3. Email Sequence (3-email series)
```
EMAIL 1: OPENER
Subject: The copywriter profession just changed forever
Preview: And it's not what you think...

---

EMAIL 2: VALUE
Subject: I tested 5 AI tools so you don't have to
[Detailed breakdown of each tool]
[Social proof: CTR improvements, time saved]
[CTA: Download the comparison chart]

---

EMAIL 3: ACTION
Subject: Which AI tool will YOU try this week?
[Recommendation engine: "Based on your role"]
[Testimonial: Client case study]
[CTA: Start free trial]
```

#### 4. Podcast Episode Script (Excerpt - 5 minutes)
```
HOST INTRO:
"Today we're diving into something that's been making copywriters 
anxious for the past 18 months: AI. Specifically, five AI tools 
that are genuinely changing how we write marketing copy.

Now, before you panic—and I get it, you should be thinking about 
this—the answer isn't robots taking your job. It's more nuanced 
than that. So let's break down exactly what each tool does, how 
it performs in the real world, and whether you should be worried..."

[CONVERSATION WITH EXAMPLES]
"The first tool we tested is GPT-4o. It's arguably the most 
well-known, but here's what surprised us when we put it to work 
on an actual email campaign..."
```

#### 5. Executive Summary (One-Pager)
```
📌 KEY FINDINGS: AI Tools for Copywriting (2025)

🎯 MAIN TAKEAWAY
AI doesn't replace copywriters. It multiplies their output by 3x.

📊 THE DATA
• 23% average CTR improvement with AI-optimized copy
• 67% faster turnaround on A/B variants
• $12K-$50K annual savings per copywriter

🏆 TOP 3 TOOLS
1. GPT-4o — Speed & versatility (best for teams)
2. Claude 3.5 Sonnet — Nuanced tone (best for brand voice)
3. Copy.ai — Template library (best for beginners)

⚠️ LIMITATIONS
- Requires human editing for factual claims
- Inconsistent voice across batches without guardrails
- May duplicate common marketing clichés

✅ RECOMMENDATION
Use AI for drafts, outlines, and variations. Reserve humans for 
strategy, fact-checking, and final approval.
```

---

## Tips & Best Practices

### 1. **Provide High-Quality Source Content**
- Well-structured source material produces better repurposing
- Include headers, bullet points, and clear CTAs
- Specify target audience for each format
- Provide brand guidelines upfront

### 2. **Batch Processing for Efficiency**
```
Instead of: "Repurpose 1 blog post"
Do this: "Batch process my top 10 performing posts 
         from Q4 2024 into all social formats"
```
Result: 3-4x faster than individual requests, consistency across content.

### 3. **Leverage Platform Specifications**
- Mention platform limitations upfront (character counts, video length)
- Specify posting schedule preferences (best times, frequency)
- Include platform-specific hashtag strategies

### 4. **Maintain Brand Voice Through Reference**
```
"Use this content as reference for tone:
[Paste 3 examples of your best existing content]
Now repurpose my new blog post maintaining this voice..."
```

### 5. **Use Tiered Requests for Complex Projects**
```
Step 1: Generate video script outline
Step 2: Expand outline with B-roll cues
Step 3: Create speaker notes and timing
Step 4: Add captions and visual directions
```
More granular = better quality, easier to iterate.

### 6. **A/B Test Repurposed Variants**
Ask the skill to generate 2-3 versions of each format and test which resonates:
```
"Generate 3 different approaches for this LinkedIn post:
- Data-driven version
- Story-driven version
- Question-based version"
```

### 7. **Plan Content Calendars Ahead**
Repurpose content in batches quarterly:
- Jan-Mar: Batch process Q4 content
- April-June: Batch process Q1 content
- Etc.

This ensures consistent pipeline and scale.

---

## Safety & Guardrails

### What This Skill WILL Do
✅ Transform your existing content into new formats  
✅ Maintain factual accuracy from source material  
✅ Adapt tone for different platforms  
✅ Generate creative variations and angles  
✅ Optimize for SEO and platform algorithms  

### What This Skill WILL NOT Do
❌ **Create false claims or misleading statistics** — Always verify data in source content  
❌ **Generate plagiarized content** — All outputs are original adaptations of your source  
❌ **Bypass fact-checking requirements** — AI can hallucinate; you must verify claims  
❌ **Violate copyright** — Only repurpose content you own or have permission to use  
❌ **Remove proper attribution** — Always credit original sources in repurposed versions  
❌ **Create harmful, hateful, or discriminatory content** — Filters prevent abuse  

### Content Boundaries
- **Medical claims**: Require professional review before publishing
- **Financial advice**: Label as opinion; include necessary disclaimers
- **Legal statements**: Must be reviewed by legal counsel
- **Proprietary data**: Only repurpose public or internally-approved content
- **Sensitive topics**: Maintain journalistic integrity and balanced perspective

### IP & Attribution
- Repurposed content should credit the original source
- Use canonical tags when republishing across domains
- Respect paywall restrictions (e.g., Medium, Substack)
- Don't republish full copyrighted articles; use excerpts + attribution

---

## Troubleshooting

### ❓ Q: "The repurposed content doesn't sound like my brand"
**A:** Provide 3-5 examples of your best-performing content as reference:
```
"Analyze these 5 posts for tone and style:
[Paste examples]
Now repurpose my new article maintaining this exact voice..."
```

### ❓ Q: "Generated content has factual errors"
**A:** This is normal—AI can misinterpret or hallucinate. Solutions:
1. Use the `INCLUDE_FACT_CHECK_MARKERS` option to flag claims
2. Always review outputs before publishing
3. Provide source links so the AI can cross-reference
4. Use Claude 3.5 Sonnet for higher accuracy on complex topics

### ❓ Q: "Social media posts are too long"
**A:** Specify character limits explicitly:
```
"Generate Twitter posts (max 280 characters each, no threads)"
"Generate TikTok hooks (max 10 words, high-energy)"
```

### ❓ Q: "How do I handle multiple product lines with different tones?"
**A:** Create separate repurposing batches by product/brand:
```
Batch 1: ProductA content [Professional tone]
Batch 2: ProductB content [Casual tone]
Batch 3: ProductC content [Technical tone]
```

### ❓ Q: