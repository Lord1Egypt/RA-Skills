---
name: dropspace-content-engine
description: "Self-improving autonomous content pipeline. Analyzes post performance across 6 platforms, generates new content with AI (slideshows, tweets, linkedin posts, reddit threads), schedules via Dropspace API. Gets smarter every night — each cycle learns from real engagement data. Use when asked to set up autonomous content posting, run the content engine, or manage multi-platform social media automation."
homepage: https://www.dropspace.dev/community/dropspace-content-engine
source: https://github.com/joshchoi4881/dropspace-agents
metadata:
  {
    "openclaw":
      {
        "emoji": "🔄",
        "requires": {
          "env": ["DROPSPACE_API_KEY", "ANTHROPIC_API_KEY", "FAL_KEY"],
          "install": "git clone https://github.com/joshchoi4881/dropspace-agents && cd dropspace-agents && npm install"
        }
      }
  }
---

# Dropspace Content Engine

Fully autonomous content pipeline. Every night: pull analytics → identify winning hooks → generate new posts → schedule across 6 platforms. The feedback loop compounds — each cycle produces better content because it learns from real engagement data.

## Setup

### 1. Clone and install

```bash
git clone https://github.com/joshchoi4881/dropspace-agents && cd dropspace-agents && npm install
```

If `canvas` fails to install, that's fine — text-only formats still work. For visual formats (TikTok/Instagram slideshows): macOS `brew install pkg-config cairo pango`, Linux `apt install libcairo2-dev libpango1.0-dev`, then `npm install` again.

### 2. Run the setup wizard

```bash
node setup.js --template dropspace-content-engine
```

Walks you through API keys, platform selection, and app configuration.

### 3. Set your API keys

```bash
export DROPSPACE_API_KEY="ds_live_..."     # from dropspace.dev/settings/api
export ANTHROPIC_API_KEY="sk-ant-..."       # from console.anthropic.com
export FAL_KEY="fal_..."                    # from fal.ai (for visual/video formats)
```

Save in a `.env` file (copy from `templates/.env.example`). Add `.env` to `.gitignore` to avoid committing secrets.

### 4. Validate

```bash
node scripts/test-pipeline.js --app myapp
```

## Run the Pipeline

```bash
source .env

# Analyze performance + generate new posts
node scripts/run-self-improve-all.js --app myapp

# Schedule generated posts for today
node scripts/schedule-day.js --app myapp
```

## Automate Nightly

| Time (ET) | Script | What |
|-----------|--------|------|
| 12:00 AM | `scripts/refresh-tracking.js --all` + `scripts/cleanup-posts.js --all` | Refresh analytics, clean old media |
| 12:30 AM | `scripts/run-x-research.js --app myapp` | Scan X for trending hooks (optional, needs Bird CLI) |
| 1:00 AM | `scripts/run-self-improve-all.js --app myapp` | Analyze + generate (up to 60 min) |
| 2:00 AM | `scripts/schedule-day.js --app myapp` | Schedule for today |

## What Happens Each Run

1. Pulls 14 days of analytics from Dropspace API
2. Identifies winning hooks (posts with >2x average engagement)
3. Cross-references with X/Twitter research signals
4. Generates 7-14 new posts with AI (text, visual, video formats)
5. Fact-checks any claims about people, products, or events
6. Writes strategy notes that persist between runs (the loop compounds)
7. Schedules posts across the day via Dropspace API

## Content Formats

| Format | Type | Platforms |
|--------|------|-----------|
| story-slideshow | visual | TikTok, Instagram, Facebook |
| ugc-reaction | video | TikTok, Instagram |
| text-single | text | Twitter/X |
| text-post | text | LinkedIn, Reddit, Facebook |

## Links

- Community page: https://www.dropspace.dev/community/dropspace-content-engine
- Case study: https://www.dropspace.dev/case-studies/march-2026
- Repo: https://github.com/joshchoi4881/dropspace-agents
- Dropspace API docs: https://www.dropspace.dev/docs
