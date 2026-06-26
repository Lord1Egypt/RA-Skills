---
name: community_quick_scan
description: Scans a Telegram or Discord community and returns a single actionable fix.
version: 0.1.0
license: MIT-0
metadata:
  author: 0xzahra
  keywords: [community, audit, telegram, discord, engagement]
---

# Community Quick Scan

This skill performs a rapid audit of a community and returns one actionable improvement.

## When to use this skill

Use `community_quick_scan` when a user asks for a quick community review, free audit, or fast feedback.

## Instructions

1. Ask the user for their community invite link, current member count, and a one-sentence project description.
2. Analyze the community for:
   - Engagement quality (ratio of active members)
   - Bot and spam risk
   - Onboarding friction (welcome messages, pinned posts)
3. Return the analysis in this format:

**Health Score:** X/10
**Engagement Quality:** Low/Med/High
**Bot Risk:** Low/Med/High
**Top Problems:** (list up to 3)
**Action Step:** (one specific, actionable fix)

4. Offer the full paid audit ($22 on ACP) if the user wants deeper analysis.
