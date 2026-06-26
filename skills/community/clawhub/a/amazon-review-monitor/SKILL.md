# Amazon Review Monitor — Track, Analyze, Respond

**Never miss a negative review again. AI-drafted responses included.**

## Description
Monitor reviews for any ASIN. Tracks rating distribution, analyzes sentiment, identifies negative themes, and drafts professional seller responses. Set up alerts for new negative reviews.

## When to Use
- User wants to monitor Amazon product reviews
- User received a negative review and needs a response
- User wants sentiment analysis on their product reviews
- User asks about review trends or customer feedback

## Usage
```bash
# Analyze reviews for an ASIN
cd <skill_dir>/scripts && python3 monitor.py B0XXXXXXXXX

# Analyze 5 pages of reviews on UK marketplace
cd <skill_dir>/scripts && python3 monitor.py B0XXXXXXXXX co.uk 5
```

## What It Does
- Scrapes recent reviews (configurable depth)
- Shows rating distribution (5⭐ to 1⭐ with visual bars)
- Calculates average rating
- Sentiment analysis (positive/negative word detection)
- Identifies top positive and negative themes
- Highlights negative reviews needing responses
- **Drafts professional seller responses** based on complaint type

## Response Templates Cover
- Product freshness/quality issues
- Shipping damage
- Wrong item/expectations mismatch
- General dissatisfaction

## No Dependencies
Pure Python 3. No API keys. No pip install needed.
