# Outreach & Copy Optimization

## Overview

Copy optimization (cold email, ad copy, landing pages, LinkedIn messages) is the highest-ROI application of binary evals. The feedback loop is clear: did the person reply? Did they click? These are your metrics.

## Cold Outreach Optimization

### Scalar metric (if you have reply rate data):
```bash
./auto-optimizer.sh \
  --eval-mode scalar \
  --metric "bash ./measure-reply-rate.sh" \
  --file ./outreach-template.md \
  --budget 30 \
  --session "outreach-opt"
```

### Binary eval metric (before you have data, or for quality pre-screening):
```bash
./auto-optimizer.sh \
  --eval-mode binary \
  --evals ./evals-templates/outreach-evals.md \
  --file ./outreach-template.md \
  --batch-size 10 \
  --budget 20 \
  --session "outreach-quality"
```

## What Makes Outreach Convert

Based on our optimization runs, the highest-impact variables:
1. **Subject line specificity** — generic = ignored, specific = opened
2. **First line relevance** — reference something real about the prospect
3. **Problem statement** — articulate their pain better than they can
4. **Single CTA** — one ask, not three
5. **Social proof** — specific results, not vague claims
6. **Length** — under 100 words is almost always better

## Template Structure (Battle-Tested)

```
Subject: [Specific hook about them/their company]

[1-2 sentence observation about a specific thing they're doing or experiencing]

[1 sentence connecting their situation to a result you've achieved]

[Social proof — specific: "helped X similar company achieve Y"]

[One clear ask — 15-min call? Quick reply? Not "let me know if interested"]

[Name]
```

## Learnings from Our Outreach Loop

From running the autoresearch loop on outreach templates:

- **Personalization beats polish**: A slightly awkward email that references the prospect's specific situation outperforms a polished generic one
- **Curiosity gaps work**: "Here's what I noticed about [their company]..." → higher open rate than feature-led openers
- **Remove "I" from first sentence**: Starting with "You" or a specific observation removes the self-promotional feel
- **One specific number beats three vague claims**: "14% reply rate" > "strong results for similar companies"
- **Question CTAs outperform action CTAs**: "Would it be worth 15 min to explore?" > "Book a call here"

## Ad Copy Optimization

For ad copy, binary evals work well pre-launch. Scalar evals (CTR, ROAS) work better post-launch.

Pre-launch binary evals:
1. Does the headline communicate a specific benefit (not a feature)? → yes/no
2. Is the offer clear within the first 5 seconds of reading? → yes/no
3. Does the copy address a real pain point the target audience experiences? → yes/no
4. Is there a specific call to action (not "learn more")? → yes/no
5. Does the copy avoid insider jargon the audience wouldn't use? → yes/no

## Landing Page Optimization

Landing pages work best with scalar metrics (conversion rate via analytics API) but binary evals can catch obvious quality issues before launch.

```bash
# Scalar: measure conversion rate via analytics API
./auto-optimizer.sh \
  --eval-mode scalar \
  --metric "python measure-conversions.py --page landing-v2" \
  --file ./landing-page-copy.md \
  --budget 20 \
  --goal maximize

# Binary: quality check before launch
./auto-optimizer.sh \
  --eval-mode binary \
  --evals ./landing-evals.md \
  --file ./landing-page-copy.md \
  --batch-size 5 \
  --budget 15
```
