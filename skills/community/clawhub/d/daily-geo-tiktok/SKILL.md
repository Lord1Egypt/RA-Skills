---
name: daily-geo-tiktok
description: Generate daily geopolitical TikTok scripts using free news sources. Use when user wants to create TikTok content about world events, conflicts, diplomacy, or geopolitical developments that happened in the last 24 hours.
---

# Daily Geopolitical TikTok Reporter

## Quick Start

This skill generates 60-90 second TikTok scripts about major geopolitical events from the past 24 hours using free news sources.

## When to Use This Skill

Use this skill when you need to:
- Generate TikTok scripts about today's geopolitical news
- Create daily world events content for social media
- Analyze and summarize geopolitical developments
- Produce short-form video content about international affairs

## Features

### News Gathering
- **Free RSS feeds** from major news sources
- **Regional filtering** (Middle East, Europe, Asia, Americas, Africa)
- **Topic categorization** (conflicts, diplomacy, elections, sanctions)
- **Daily aggregation** of significant events

### Geopolitical Analysis
- **Event importance scoring** (1-10 scale)
- **Geopolitical impact categorizing**
- **Regional relevance filtering**
- **Fact verification** and source attribution

### TikTok Script Generation
- **60-90 second optimized** scripts
- **Engaging hooks** and cliffhangers
- **Viral hashtags** and trending topics
- **Platform-optimized** formatting

## Usage

### Basic Usage
```
Generate today's geopolitical TikTok scripts
```

### Advanced Usage
```
Generate 3 TikTok scripts about Middle East events from the last 24 hours
Focus on conflicts and sanctions
Include hashtags: #geopolitics #worldnews #middleeast
```

### Scheduled Reports
```
Create daily geopolitical TikTok report schedule for 8 AM UTC
```

## Supported News Sources (Free)

- BBC World News RSS
- Reuters World RSS
- AP World News RSS
- Al Jazeera RSS
- Foreign Policy RSS
- Reuters Conflict News

## Output Formats

### TikTok Script Structure
```
🎵 Hook: (3-5 seconds) Attention-grabbing opening
🌍 Context: (10-15 seconds) Background and significance
📰 News: (30-45 seconds) Main story and developments
💡 Impact: (10-15 seconds) Why it matters
📈 Next: (5 seconds) What to watch for

#hashtags: #geopolitics #worldnews #[region] #[topic]
```

## Configuration

### Regional Focus
Edit `config/regions.yaml` to prioritize specific geographic areas.

### Topic Preferences
Edit `config/topics.yaml` to customize content categories.

### Scheduling
Use `config/schedule.yaml` for automated daily reports.

## Templates

- `templates/tiktok-script.yaml` - Script structure template
- `templates/hashtags.yaml` - Trending hashtag database

## Getting Help

For detailed setup and customization:
- [News Sources Guide](references/news-sources.md)
- [TikTok Best Practices](references/tiktok-best-practices.md)
- [Geopolitical Taxonomy](references/geo-taxonomy.md)