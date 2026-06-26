# Content Machine

Automated content generation system that discovers trending topics and publishes to social media. Uses AI to research, write, and schedule posts.

## What It Does

- Monitors trends across multiple sources
- Generates engaging content using AI
- Schedules and publishes to social platforms
- Tracks performance and optimizes

## Setup

### Prerequisites

1. **OpenAI API Key** or **Anthropic API Key** - For content generation
2. **Postiz API Key** - For posting to social platforms
3. Optional: Platform-specific APIs (Twitter, LinkedIn, etc.)

### Environment Variables

```bash
export OPENAI_API_KEY="your_openai_key"
export POSTIZ_API_KEY="your_postiz_key"
```

### Installation

```bash
pip install requests openai
```

## Usage

### Run content generation

```bash
python content-machine.py --niche tech --platforms twitter,linkedin --count 5
```

### Configure sources

Edit `config/sources.json` to add:
- RSS feeds
- News APIs
- Social trend endpoints

### Set posting schedule

```bash
python content-machine.py --schedule "9am,12pm,6pm"
```

## Configuration

- `config/content.json` - Content templates
- `config/schedule.json` - Posting times
- `config/platforms.json` - Platform settings

## Features

- Multi-platform posting (Twitter, LinkedIn, Instagram, TikTok)
- Content templates and virality scoring
- Auto-hashtag generation
- Image generation for posts
- Performance analytics

## Cost

Depends on AI usage:
- OpenAI: ~$0.001/post
- Images: ~$0.01/post (if generating)
