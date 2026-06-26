# Ad Spy Pipeline

Automated competitor ad monitoring pipeline: scrape ads from ForePlay/Anstrex, generate adaptations with AI, and sync to Facebook Ads — all on autopilot.

Use when: you run e-commerce ads and want to automatically find competitor creatives, adapt them for your brand, and launch new campaigns without manual work.

## What it does

3-stage automated pipeline:

### Stage 1 — Scrape
- Monitors competitor brands on ForePlay or Anstrex
- Detects new ad creatives automatically
- Deduplicates against your existing library
- Downloads source images/videos

### Stage 2 — Generate
- Sends source creatives to Kie.ai for AI adaptation
- Generates brand-specific versions (your colors, your product, your copy)
- Creates multiple aspect ratios (1:1 for feed, 9:16 for stories/reels)
- Auto-classifies creatives by marketing category (urgency, deal, gift, social proof, etc.)

### Stage 3 — Sync to Facebook
- Creates ad campaigns via Facebook Marketing API
- Organizes by category and naming convention
- All ads created in PAUSED mode (you activate manually)
- Full traceability: source → adaptation → Facebook ad ID

## Requirements

- ForePlay API key OR Anstrex account
- Kie.ai API key (image generation)
- Facebook Marketing API access token
- Facebook Ad Account ID

## Cron Schedule

Set up daily runs:
```
0 7 * * * python3 storm_pipeline_agent.py --all
```

## Tags
facebook-ads, advertising, competitor-research, ecommerce, automation, creative, marketing, foreplay, anstrex
