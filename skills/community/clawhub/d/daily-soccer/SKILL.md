---
name: daily-soccer
description: Generate daily soccer/football news content and TikTok scripts using free sports news sources. Use when user wants to create content about football matches, transfers, player news, league updates, or FIFA competitions from the last 24 hours.
---

# Daily Soccer Content Generator

## Quick Start

This skill generates 60-90 second TikTok scripts and social media content about major soccer/football events from the past 24 hours using free news sources.

## When to Use This Skill

Use this skill when you need to:
- Generate TikTok scripts about today's soccer/football news
- Create daily sports content for social media
- Summarize match results and upcoming fixtures
- Cover transfer news and player movements
- Produce content about leagues, cups, or international competitions

## Features

### News Gathering
- **Free RSS feeds** from major sports news sources
- **League filtering** (Premier League, La Liga, Serie A, Bundesliga, Ligue 1, MLS, etc.)
- **Topic categorization** (matches, transfers, injuries, management)
- **Daily aggregation** of significant football events

### Soccer Analysis
- **Match significance scoring** (1-10 scale)
- **Transfer impact evaluation**
- **League standing updates**
- **Player performance metrics**

### TikTok Script Generation
- **60-90 second optimized** scripts
- **Exciting match highlights** and key moments
- **Viral hashtags** and trending topics
- **Platform-optimized** formatting

## Usage

### Basic Usage
```
Generate today's soccer TikTok scripts
```

### Advanced Usage
```
Generate 3 TikTok scripts about Premier League matches from the last 24 hours
Focus on transfers and player news
Include hashtags: #football #soccer #premierleague
```

### League-Specific
```
Create daily La Liga soccer report schedule
```

## Supported News Sources (Free)

- ESPN Soccer RSS
- BBC Sport Football RSS
- Reuters Soccer News
- Goal.com RSS
- FIFA.com News
- UEFA.com News
- Sky Sports Football RSS

## Output Formats

### TikTok Script Structure
```
⚽ Hook: (3-5 seconds) Exciting opening about match or player
🏟️ Context: (10-15 seconds) League, teams, and situation
📰 News: (30-45 seconds) Match highlights, transfers, or key updates
💡 Impact: (10-15 seconds) What this means for the team/league
📈 Next: (5 seconds) Upcoming matches or transfer window dates

#hashtags: #football #soccer #[league] #[team] #[topic]
```

## Configuration

### League Focus
Edit `config/leagues.yaml` to prioritize specific leagues.

### Topic Preferences
Edit `config/topics.yaml` to customize content categories (matches, transfers, injuries, management).

### Scheduling
Use `config/schedule.yaml` for automated daily reports.

## Templates

- `templates/tikTok-script.yaml` - Script structure template
- `templates/hashtags.yaml` - Trending hashtag database
- `templates/match-summary.yaml` - Match result template

## Getting Help

For detailed setup and customization:
- [News Sources Guide](references/news-sources.md)
- [TikTok Best Practices](references/tiktok-best-practices.md)
- [Soccer Taxonomy](references/soccer-taxonomy.md)
