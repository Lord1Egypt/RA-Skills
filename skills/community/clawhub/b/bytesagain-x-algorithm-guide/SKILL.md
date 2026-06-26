---
name: bytesagain-x-algorithm-guide
description: "Audit and optimize X (Twitter) posts using bash-based 2026 algorithm rules and growth tactics. Use when drafting tweets, checking content before posting, reviewing hashtag count, or learning posting strategy based on open-source X algorithm weights and real creator case studies."
version: "1.1.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
tags: [social-media, twitter, content-creation, writing, automation]
---

# bytesagain-x-algorithm-guide

Audit and optimize X (Twitter) posts using bash-based 2026 algorithm rules and real growth tactics. Based on open-source X algorithm code and verified creator case studies (4,500 followers / 5M views in 30 days).

## Commands

### summary
Print the 10 core algorithm rules with engagement weights from open-source code.

```bash
bash scripts/script.sh summary
```

### audit
Audit a tweet and score it against 2026 algorithm rules. Flags links in body, excess hashtags, character count.

```bash
bash scripts/script.sh audit "Your tweet text here"
```

### checklist
Print the 8-point pre-post checklist.

```bash
bash scripts/script.sh checklist
```

### draft
Generate two tweet draft templates following 2026 algorithm rules.

```bash
bash scripts/script.sh draft "AI agents for developers"
```

### growth
Print the 30-day growth playbook: daily actions, content mix strategy, and engagement tactics from verified creator case studies.

```bash
bash scripts/script.sh growth
```

## Key 2026 Algorithm Rules

Based on open-source X algorithm code (github.com/twitter/the-algorithm):

1. No links in main tweet — 30-50% reach penalty; put links in first reply
2. Max 1-2 hashtags — more than 2 causes 40% penalty
3. Pure text beats video by 30% — X is the only platform where this is true
4. Reply every genuine comment in first hour — weight +75 (150x a like)
5. Bookmarks signal value — weight +10 (20x a like)
6. Premium accounts get 10x reach vs free accounts
7. Post 3-5 times per day, 30-60 min apart
8. TweepCred threshold is 65 — below 65, only 3 tweets get distributed
9. Grok reads tone — positive content gets more reach
10. Long posts outperform threads — 2+ min read time gets +10 weight

## Growth Playbook (Verified: 4,500 followers / 5M views in 30 days)

- Daily: 30-50 high-quality replies under top creator posts (not "lol" — real opinions)
- Daily: 3-5 original tweets (not more — new accounts get penalized for volume)
- Daily: Follow 5-10 accounts in your niche
- Content mix: 80% broad/relatable + 20% niche expertise
- Week 1-2: Focus entirely on engagement, not posting
- Open Premium early — comments get priority ranking, platform treats you as legitimate

## Requirements

- bash 4+

## Feedback

https://bytesagain.com/feedback/
Powered by BytesAgain | bytesagain.com
