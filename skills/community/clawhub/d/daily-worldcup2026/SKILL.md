---
name: daily-worldcup2026
description: Generate daily FIFA World Cup 2026 content and TikTok scripts using free news sources. Use when user wants to create content about World Cup 2026 preparations, qualifiers, team news, host cities, or tournament developments from the last 24 hours.
---

# Daily World Cup 2026 Reporter

## Quick Start

This skill generates 60-90 second TikTok scripts and social media content about FIFA World Cup 2026 events from the past 24 hours using free news sources.

## When to Use This Skill

Use this skill when you need to:
- Generate TikTok scripts about World Cup 2026 news
- Create daily World Cup content for social media
- Cover qualifying matches and standings
- Report on team preparations and player selections
- Produce content about host cities, venues, and infrastructure

## Features

### News Gathering
- **Free RSS feeds** from FIFA and major sports sources
- **Regional qualifier tracking** (UEFA, CONMEBOL, CAF, AFC, CONCACAF, OFC)
- **Topic categorization** (qualifiers, host preparations, squads, venues)
- **Daily aggregation** of World Cup 2026 developments

### Tournament Analysis
- **Match qualification probability** tracking
- **Host city readiness** updates
- **Team squad announcements**
- **Venue construction** and stadium progress

### TikTok Script Generation
- **60-90 second optimized** scripts
- **Exciting qualifier highlights**
- **Host city reveals** and venue features
- **Viral hashtags** and trending topics
- **Platform-optimized** formatting

## Usage

### Basic Usage
```
Generate today's World Cup 2026 TikTok scripts
```

### Advanced Usage
```
Generate 3 TikTok scripts about European qualifiers from the last 24 hours
Focus on host city preparations
Include hashtags: #WorldCup2026 #FIFA #football
```

### Regional-Specific
```
Create daily CONCACAF qualifier report
```

## Supported News Sources (Free)

- FIFA.com World Cup 2026 RSS
- Reuters World Cup News
- ESPN World Cup Coverage
- BBC Sport World Cup RSS
- The Athletic World Cup 2026
- Goal.com World Cup Coverage

## Output Formats

### TikTok Script Structure
```
🏆 Hook: (3-5 seconds) World Cup excitement or qualifier drama
🌍 Context: (10-15 seconds) Confederation, teams, stakes
📰 News: (30-45 seconds) Qualifier updates, prep news, or venue reveals
💡 Impact: (10-15 seconds) What this means for WC 2026
📈 Next: (5 seconds) Upcoming qualifiers or countdown

#hashtags: #WorldCup2026 #FIFA #[confederation] #[team] #[topic]
```

## Configuration

### Confederation Focus
Edit `config/confederations.yaml` to prioritize specific qualifier regions (UEFA, CONMEBOL, etc.).

### Topic Preferences
Edit `config/topics.yaml` to customize content categories (qualifiers, venues, squads, prep).

### Scheduling
Use `config/schedule.yaml` for automated daily reports.

## Templates

- `templates/tiktok-script.yaml` - Script structure template
- `templates/hashtags.yaml` - Trending hashtag database
- `templates/qualifier-summary.yaml` - Match result template

## Getting Help

For detailed setup and customization:
- [News Sources Guide](references/news-sources.md)
- [TikTok Best Practices](references/tiktok-best-practices.md)
- [World Cup 2026 Timeline](references/wc2026-timeline.md)
