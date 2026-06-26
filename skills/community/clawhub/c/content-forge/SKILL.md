---
name: content-forge
description: Generate content ideas, blog outlines, social media posts, and headlines. Use when the user needs help creating content for blogs, Twitter/X threads, LinkedIn posts, or developing a content calendar. Provides templates and AI-assisted content generation patterns.
---

# Content Forge

Generate content ideas and drafts for blogs, social media, and marketing.

## Commands

### Blog Post Ideas
```bash
content-forge blog TOPIC [-s STYLE] [--json]
```

Styles: `how_to` (default), `listicle`, `case_study`

Examples:
```bash
content-forge blog "machine learning"
content-forge blog "productivity tips" -s listicle
content-forge blog "startup growth" --json
```

### Social Media Content
```bash
content-forge social PLATFORM TOPIC [--json]
```

Platforms: `twitter`, `linkedin`

Examples:
```bash
content-forge social twitter "AI tools"
content-forge social linkedin "career growth"
```

### Content Calendar
```bash
content-forge calendar TOPIC1 [TOPIC2 ...] [-d DAYS] [--json]
```

Examples:
```bash
content-forge calendar "AI" "productivity" "startup"
content-forge calendar marketing sales growth -d 14
```

### Headline Generator
```bash
content-forge headlines TOPIC [-n NUM]
```

Examples:
```bash
content-forge headlines "passive income"
content-forge headlines "remote work" -n 20
```

## Output Formats

Default: Human-readable formatted text

`--json`: Machine-readable JSON output for scripting

## Use Cases

- **Content creators**: Beat writer's block with generated ideas
- **Marketers**: Create content calendars and social posts
- **Founders**: Generate blog topics for thought leadership
- **Agencies**: Scale content production with templates

## Notes

- No external API calls required
- Works offline
- Templates are customizable patterns, not AI-generated text
