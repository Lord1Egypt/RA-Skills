---
name: cocreator-content-research
description: "Pure intelligence gathering for social media platforms (TikTok & Instagram). Use when an agent needs to discover trending hooks, analyze a competitor's strategy, or look up a specific creator's profile data. This skill does not generate content or post; it relies entirely on ScrapeCreators to return data for analysis."
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "requires": {
        "bins": ["uv"],
        "env": ["SCRAPE_CREATORS_API_KEY"]
      },
      "primaryEnv": "SCRAPE_CREATORS_API_KEY",
      "install": [
        {
          "id": "uv-install",
          "kind": "bash",
          "script": "curl -LsSf https://astral.sh/uv/install.sh | sh",
          "bins": ["uv"],
          "label": "Install uv (cross-platform via bash)"
        }
      ]
    }
  }
---

# Content Research Skill

This skill provides agents with the ability to gather raw intelligence on social media performance (TikTok and Instagram) using the ScrapeCreators API. It does not generate content or interact with posting APIs.

## Prerequisites
- `uv` installed
- `SCRAPE_CREATORS_API_KEY` set in the environment

## Capabilities

### 1. Broad Content Discovery (Keywords & Hashtags)
Use this to find top-performing content. 
**Agent Instructions for Keyword Search:**
- **DO NOT** use the same hardcoded keyword (like "affirmations") every time.  
- **ALWAYS** brainstorm 3-5 diverse keywords based on the user's app (e.g., if it's an affirmation app, try searching "mindset shift", "daily routine", "self healing", "morning motivation").
- Use time frames (`--date-posted`) to find recent trends, and test different sorting methods. 
- Use the `--format` filter (`video`, `slideshow`, or `both`) if the user specifically requests only one type of content.
- **CRITICAL:** The script returns an `is_slideshow` boolean and a `video_url`. Use this to distinguish between video trends and slideshow trends.

```bash
uv run {baseDir}/scripts/keyword-search.py --platform tiktok --type keyword --query "morning routine" --date-posted this-month --sort-by most-liked --format slideshow
uv run {baseDir}/scripts/keyword-search.py --platform instagram --type keyword --query "morning routine" --format video
```

### 2. Competitor Hook Research
Use this to analyze specific competitor handles. 
**Agent Instructions for Competitor Research:**
- **ALWAYS** ask the user if they have specific competitors or creator profiles they want you to check before you assume.
- If they don't know, brainstorm potential top creators in their niche using the keyword search first, extract their handles, and then run competitor research on them.

```bash
uv run {baseDir}/scripts/competitor-research.py --platform tiktok --handles user1 user2 user3
uv run {baseDir}/scripts/competitor-research.py --platform instagram --handles user1 user2
```

### 3. Profile Lookup
Use this to get raw metric data (followers, following, bio) for a specific creator.

```bash
uv run {baseDir}/scripts/profile-lookup.py --platform tiktok --handle <handle>
uv run {baseDir}/scripts/profile-lookup.py --platform instagram --handle <handle>
```
