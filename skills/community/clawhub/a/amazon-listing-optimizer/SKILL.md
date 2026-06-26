# Amazon Listing Optimizer — Free Listing Analysis & Keyword Research

**Free alternative to Helium 10 ($97/mo) and Jungle Scout ($49/mo).**

## Description
Analyze any Amazon product listing, score its quality, find keyword opportunities, and spy on competitors. No API keys needed. No subscription. Just results.

## When to Use
- User wants to optimize an Amazon listing
- User needs keyword research for Amazon SEO
- User wants to analyze competitors in a niche
- User asks about Amazon listing quality or conversion optimization
- User mentions Helium 10, Jungle Scout, or any Amazon seller tool

## Tools

### 1. Listing Analyzer
Scores any ASIN on Title (30%), Bullets (25%), Images (25%), Reviews (20%). Returns actionable feedback.
```bash
cd <skill_dir>/scripts && python3 analyzer.py B0XXXXXXXXX
```

### 2. Keyword Extractor
Uses Amazon's own autocomplete to find long-tail keyword opportunities. Alphabet expansion + depth crawling.
```bash
cd <skill_dir>/scripts && python3 keyword_extractor.py "seasoning blend" com 2
```

### 3. Competitor Spy
Search any term, find top ASINs, identify weak competitors to outrank.
```bash
cd <skill_dir>/scripts && python3 competitor_spy.py "garlic seasoning organic"
```

## What It Scores
- **Title** (0-100): Length, keywords, formatting, numbers, separators
- **Bullets** (0-100): Count, length, benefit language, keyword density
- **Images** (0-100): Count vs Amazon's 7+ recommendation
- **Reviews** (0-100): Rating + review count as social proof
- **Overall** (0-100): Weighted composite with letter grade (A+ to F)

## No Dependencies
- Pure Python 3 (stdlib only)
- No pip install needed
- No API keys
- No browser extension
- Works on any machine with Python 3.6+

## Comparison
| Feature | This Skill | Helium 10 | Jungle Scout |
|---------|-----------|-----------|--------------|
| Price | FREE | $97-397/mo | $49-399/mo |
| Listing Score | ✅ | ✅ | ✅ |
| Keyword Research | ✅ | ✅ | ✅ |
| Competitor Analysis | ✅ | ✅ | ✅ |
| API Key Required | ❌ | ✅ | ✅ |
| Works in Agent | ✅ | ❌ | ❌ |
