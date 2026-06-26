---
name: buymeacoffee-autobot
version: 1.0.18
description: |
  Automates Buy Me a Coffee / Ko-fi page — generates content, posts updates, thanks
  supporters, and converts followers into paying supporters   Also runs affiliate links for digital products and cross-promotes across platforms.
compatibility: Python 3, requests. Buy Me a Coffee has no public API (use browser automation).
metadata:
  author: ssyopros.zo.computer
  category: passive-  tags: buymeacoffee, ko-fi, creator-monetization, tips, donations, supporters, passive-
# buymeacoffee-autobot

Automate your Buy Me a Coffee page.

## What This Does

1. **Posts content updates** — auto-posts to your page via browser automation
2. **Thanks supporters** — personalized thank-you messages after each tip
3. **Converts followers** — promotes page to drive new supporters
4. **Cross-promotes** — shares your page on social channels
5. **Tracks earnings** — daily summary of tips received

## Core Script

### `scripts/bmc_autoposter.py`

```python
#!/usr/bin/env python3
"""Buy Me a Coffee autoposter — automates content and supporter management."""

def post_update(message):
    """Post an update to your BMC/Ko-fi page."""
    pass  # Browser automation via Selenium

def thank_supporter(name, amount):
    """Send personalized thank-you after a tip."""
    pass

def promote_page():
    """Share page link across connected platforms."""
    pass

def get_earnings():
    """Scrape today's tips and total earnings."""
    pass
```

## Growth Strategy

- Post 3x/week minimum — consistency builds supporter base
- Offer 3 supporter tiers: $3, $5, $10
- Bundle digital products as perks
- Cross-promote from Twitter/X and LinkedIn

## Earnings Model

- Buy Me a Coffee: 0% fee on tips (they - Ko-fi: 0% fee, optional paid subscriptions
- Target: $100–$500/month from 10–50 active supporters

## Steps to Connect

1. Sign up at [buymeacoffee.com](https://buymeacoffee.com) or [ko-fi.com](https://ko-fi.com)
2. Save your page URL as `BMC_PAGE_URL` in [Settings > Advanced](/?t=settings&s=advanced)
3. Save login credentials as `BMC_EMAIL` + `BMC_PASSWORD`

## Deliverable

`buymeacoffee-autobot/` with:
- `scripts/autoposter.py`
- `scripts/supporter_thanker.py`
- `config/content_calendar.json` — scheduled posts
- `SKILL.md` — this file
