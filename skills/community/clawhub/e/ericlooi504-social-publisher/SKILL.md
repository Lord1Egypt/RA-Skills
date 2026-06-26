---
name: GTS_social-media-publisher
description: Generate, schedule, and publish social media content across platforms. Use when the user wants to: (1) Create engaging social media posts for Twitter/X, LinkedIn, Instagram, Facebook, TikTok, (2) Generate content calendars for weeks or months, (3) Repurpose long-form content (blog posts, videos) into social snippets, (4) Schedule posts with optimal timing, (5) Maintain consistent brand voice across platforms. Best for content creators, small businesses, marketers, and anyone who needs consistent social media presence without daily manual effort.
version: 1.0.1
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "📱"
---

# GTS Social Media Publisher

Automate your social media content pipeline — generate posts, plan calendars, repurpose content, and maintain brand voice across platforms.

## Quick Start

> *"Create a LinkedIn post about our new product launch"*
> *"Generate a week of Twitter content about AI trends"*
> *"Turn this blog post into 5 social media posts"*
> *"Create a content calendar for next month"*
> *"Write an Instagram caption for this product photo"*

The agent will:
1. Understand the topic, brand voice, and target platform
2. Generate platform-optimized content (character limits, hashtags, tone)
3. Create a content calendar if requested
4. Track published content for consistency

## Features

### 1. Post Generation

Generate platform-specific posts from any input:

**From scratch**: *"Create 3 Twitter posts about our new eco-friendly packaging"*
**From URL**: *"Turn this article into LinkedIn posts: https://..."*
**From topic**: *"Weekly content for a fitness coach Instagram"*
**From existing**: *"Repurpose this blog post for Twitter, LinkedIn, and Instagram"*

The agent generates content that respects:
- Platform character limits (Twitter: 280, LinkedIn: 3000, Instagram caption: 2200)
- Optimal post structure (hook → body → CTA)
- Hashtag strategy (platform-appropriate count)
- Best posting times per platform
- Brand voice consistency

### 2. Content Calendar

Generate weekly/monthly calendars:

```
📅 Content Calendar — May 2026
──────────────────────────────
Week 1 (May 1-7): Product Focus
  Mon: Product teaser (Twitter)
  Tue: Customer testimonial (LinkedIn)
  Wed: Behind-the-scenes (Instagram)
  Thu: Industry tip (Twitter)
  Fri: Weekly roundup (LinkedIn)

Week 2 (May 8-14): Educational
  ...
```

### 3. Content Repurposing

Take one piece of long-form content and extract multiple social posts:

**Blog post →**
- 1 LinkedIn article summary
- 3 Twitter threads (key takeaways)
- 1 Instagram carousel (5 slides as text)
- 1 Facebook post with link preview

**Video/transcript →**
- 1 Twitter thread with timestamps
- 2 LinkedIn posts (key insights)
- 1 Instagram Reel caption
- Quote cards for all platforms

## Post Format Reference

### Platform Guidelines
| Platform | Max chars | Ideal length | Hashtags | Best times |
|----------|-----------|--------------|----------|------------|
| Twitter/X | 280 | 180-240 | 1-3 | 8-10am, 12-1pm |
| LinkedIn | 3,000 | 150-300 | 3-5 | Tue-Thu 8-10am |
| Instagram | 2,200 | 150-300 | 10-20 | 9-11am, 7-9pm |
| Facebook | 63,206 | 80-150 | 1-2 | 1-4pm |
| TikTok | 2,200 | 100-200 | 3-5 | 7-9am, 10-11am |

### Engagement Hooks (by platform)
- **Twitter/X**: Hot take, surprising stat, question, poll
- **LinkedIn**: Personal story, industry insight, professional tip
- **Instagram**: Visual-first, aesthetic quote, storytelling caption
- **Facebook**: Community question, relatable content, shareable image
- **TikTok**: Trend-hopping, educational hook, raw/unpolished

## Scripts

### `scripts/generate.py` — Content generation engine

```bash
# Generate posts
python3 scripts/generate.py post --topic "new product launch" --platform twitter --count 5

# Generate calendar
python3 scripts/generate.py calendar --theme "educational" --weeks 4 --platforms twitter,linkedin

# Repurpose content
python3 scripts/generate.py repurpose --input post.md --platforms all
```

### `scripts/calendar.py` — Content calendar management

```bash
python3 scripts/calendar.py create --month may --theme product-launch
python3 scripts/calendar.py view --month may
python3 scripts/calendar.py export --format csv
python3 scripts/calendar.py add --date 2026-05-15 --platform twitter --topic "customer story"
```

### `scripts/voice.py` — Brand voice management

```bash
# Define brand voice
python3 scripts/voice.py set --name "my-brand" --tone professional --audience "B2B SaaS founders"

# Apply voice to content
python3 scripts/voice.py apply --voice my-brand --input draft.md

# List saved voices
python3 scripts/voice.py list
```

## References

- **Platform guides**: See [references/PLATFORMS.md](references/PLATFORMS.md) for platform-specific content strategies, hashtag research, and engagement tactics
- **Content templates**: See [references/TEMPLATES.md](references/TEMPLATES.md) for post templates across platforms
- **Brand voice guide**: See [references/BRAND_VOICE.md](references/BRAND_VOICE.md) for tone of voice guidelines and examples

## Tips

- Maintain a content calendar for consistency — aim for 3-5 posts/week per platform
- Repurpose every long-form piece into at least 3 social posts
- Use the brand voice feature to keep messaging consistent
- Track engagement and adjust posting strategy accordingly
- Mix content types: educational, promotional (20%), entertaining, community
