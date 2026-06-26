---
name: content-scorer
description: Score marketing copy for resonance, hook strength, NLP technique usage, and conversion readiness. Returns a 0-100 Content Resonance Score with per-dimension breakdown and actionable rewrite suggestions. Calibrated against fMRI brain-response data (TRIBE v2).
version: 1.0.2
author: drivenautoplex1
price: 0
tags:
  - marketing
  - copywriting
  - content
  - social-media
  - email-marketing
  - direct-response
  - real-estate
  - sales
  - nlp
  - analytics
metadata:
  openclaw:
    requires:
      env:
        - ANTHROPIC_API_KEY
      anyBins:
        - python3
    primaryEnv: ANTHROPIC_API_KEY
    emoji: "🎯"
    homepage: https://github.com/drivenautoplex1/openclaw-skills
    install:
      - kind: uv
        package: anthropic
        bins: []
---

# Content Scorer Skill

Score any piece of marketing copy in seconds. Get a 0-100 resonance score, dimension-by-dimension breakdown, and specific rewrite suggestions — before you post, send, or publish.

## Free vs Premium

**Free tier (no API key needed):**
- `--demo` — run a full score on built-in demo copy, zero external calls, see exactly what the output looks like
- `--compliance-only` — fast forbidden word scan, runs locally, no API
- Score up to 3 pieces of copy/day using local MLX (if you have it running)

**Premium tier (ANTHROPIC_API_KEY):**
- Unlimited scoring via Claude Haiku (~$0.001 per score)
- `--rewrite` — get improved copy alongside your score
- `--compare` — A/B test multiple hooks side-by-side
- `--format=json` — pipe scores into your agent workflows
- Batch scoring for content calendars

The free compliance check alone is worth installing — catch forbidden words before they go live.

## What this skill does

Analyzes marketing copy across 6 weighted dimensions and returns:

- **Content Resonance Score (0-100)** — composite score calibrated against fMRI brain-response patterns (TRIBE v2 weight calibration)
- **Per-dimension scores** — hook strength, specificity, emotional resonance, NLP technique usage, CTA strength, compliance
- **Rewrite suggestions** — specific line-level changes to improve the weakest dimensions
- **Platform fit check** — flag copy that's too long/short for the target platform
- **Compliance gate** — detect forbidden words before they go live

## Scoring dimensions

| Dimension | Weight | What it measures |
|---|---|---|
| Hook Strength | 25% | First line/sentence — does it grab attention in <3 seconds? |
| Emotional Resonance | 25% | Does it connect to the reader's real situation, fear, or desire? |
| NLP Technique Usage | 20% | Presuppositions, embedded commands, pacing/leading, reframes, future pacing |
| Specificity | 15% | Concrete numbers, outcomes, timeframes — no vague platitudes |
| CTA Strength | 10% | Clear, urgent next step with no exit ramp |
| Compliance | 5% | No forbidden words, MLO-safe language |

**Why these weights:** TRIBE v2 fMRI analysis found hook + emotional resonance drive 50% of cortical engagement in language and reward circuits. NLP technique presence activates anterior insula (urgency) and mPFC (social motivation). Specificity activates hippocampal encoding — specific claims are better remembered.

## Input contract

Tell me:
1. **The copy to score** — paste it directly
2. **Platform** (optional): email / linkedin / x / facebook / instagram / sms / ad / script / any
3. **Audience** (optional): first-time buyers / investors / realtors / general
4. **Rewrite mode** (optional): `--rewrite` to get revised copy alongside the score

Example prompts:
- "Score this LinkedIn post: [paste copy]"
- "Score for email, real estate investors: [paste copy]"
- "Score and rewrite: [paste copy] --rewrite"
- "Compliance check only: [paste copy]"
- "Score these 3 hooks and tell me which is strongest: [hook A] / [hook B] / [hook C]"

## Output contract

**Standard score output:**
```
Content Resonance Score: 74/100

Dimension Breakdown:
  Hook Strength:        8/10  ✓  Strong pattern interrupt
  Emotional Resonance:  7/10  ✓  Connects to ownership aspiration
  NLP Technique:        6/10  →  Pacing present, no embedded command
  Specificity:          8/10  ✓  Concrete price + timeline
  CTA Strength:         5/10  ⚠  Exit ramp: "if you're interested"
  Compliance:          10/10  ✓  Clean

Weakest point: CTA exit ramp — "if you're interested" gives reader a way out.
Top suggestion: Replace "if you're interested, DM me" with "Drop your zip below — I'll pull your numbers."

NLP detected: pacing_leading ("Most buyers in your area right now..."), future_pacing ("Picture yourself...")
Missing: embedded_command — add one imperative buried in declarative: "...which is why serious buyers are locking in now."
```

**Rewrite output** (with `--rewrite`):
```
[Score block above]

--- REWRITE ---
[Revised copy with changes highlighted]
--- END REWRITE ---

Changes made:
1. Hook → stronger pattern interrupt (removed "I'm going to share...")
2. CTA → assume-the-close ("Drop your zip below" instead of "if you're interested")
3. Added embedded command in body ("...smart buyers are locking in this week")
```

**Multi-hook comparison:**
```
Hook A: 6/10 — Generic opener, no pattern interrupt
Hook B: 9/10 — Strong curiosity gap + specificity ("Most buyers don't know this costs them $340/month")
Hook C: 7/10 — Emotional but vague, lacks specificity

Winner: Hook B. Combines curiosity gap with concrete loss framing.
```

## How the skill works

Uses `score_content.py` (in this directory). Local MLX first (`LLM_BACKEND=local`), Haiku fallback.

```bash
# Score a piece of copy
python3 score_content.py "Your LinkedIn post text here" --platform=linkedin

# Score + rewrite
python3 score_content.py "Your copy here" --platform=email --rewrite

# Compare hooks
python3 score_content.py --compare "Hook A text" "Hook B text" "Hook C text"

# Compliance check only (fast, no API call needed)
python3 score_content.py "Your copy" --compliance-only

# JSON output (for agent pipelines)
python3 score_content.py "Your copy" --format=json | jq '.score'

# Force backend
LLM_BACKEND=local python3 score_content.py "copy"     # Qwen3.5-9B (free)
LLM_BACKEND=haiku python3 score_content.py "copy"     # Claude Haiku (~$0.001/score)
```

**Core scoring implementation:**
```python
SCORING_PROMPT = """You are a direct-response copywriting analyst trained in:
- Hormozi (value stacking, urgency, no-brainer offers)
- Belfort straight-line persuasion (tonality, certainty, trust)
- Cardone 10X (boldness, assumptive language, commitment)
- NLP persuasion (presuppositions, embedded commands, pacing/leading, reframes, future pacing)

Score the following {platform} copy on a 0-10 scale for each dimension.
Be strict — a 10 means the best direct-response copy you've ever seen.

COPY TO SCORE:
{copy}

AUDIENCE: {audience}

Respond ONLY in this JSON format:
{{
  "hook_strength": {{ "score": N, "reason": "...", "improvement": "..." }},
  "emotional_resonance": {{ "score": N, "reason": "...", "improvement": "..." }},
  "nlp_technique": {{ "score": N, "detected": ["technique1", ...], "missing": "...", "improvement": "..." }},
  "specificity": {{ "score": N, "reason": "...", "improvement": "..." }},
  "cta_strength": {{ "score": N, "reason": "...", "improvement": "..." }},
  "compliance": {{ "score": N, "violations": [] }},
  "overall_comment": "..."
}}"""

WEIGHTS = {
    "hook_strength": 0.25,
    "emotional_resonance": 0.25,
    "nlp_technique": 0.20,
    "specificity": 0.15,
    "cta_strength": 0.10,
    "compliance": 0.05,
}

FORBIDDEN_WORDS = [
    "pre-approval", "pre-approved", "pre-qualify", "specialist",
    "mortgage", "lending", "rates", "loan", "showings", "tours",
    "transfer", "connect", "team", "agent", "department",
    "qualify for", "AWESOME"
]

def compliance_check(copy: str) -> list[str]:
    """Fast local check — no API call needed."""
    violations = []
    copy_lower = copy.lower()
    for word in FORBIDDEN_WORDS:
        if word.lower() in copy_lower:
            violations.append(word)
    return violations

def composite_score(dimensions: dict) -> int:
    total = sum(dimensions[k]["score"] * WEIGHTS[k] for k in WEIGHTS)
    return round(total * 10)  # 0-100

async def score(copy, platform="any", audience="general", rewrite=False):
    violations = compliance_check(copy)
    prompt = SCORING_PROMPT.format(copy=copy, platform=platform, audience=audience)
    response = await client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    result = json.loads(response.content[0].text)
    result["compliance"]["violations"] = violations
    result["compliance"]["score"] = 10 if not violations else max(0, 10 - len(violations) * 3)
    result["composite"] = composite_score(result)
    if rewrite and result["composite"] < 85:
        result["rewrite"] = await generate_rewrite(copy, result, platform, audience)
    return result
```

## Calibration note — TRIBE v2

Dimension weights are calibrated against TRIBE v2 (Meta's fMRI brain-response prediction model, `facebook/tribev2`). Emma sales call transcripts were run through TRIBE to measure predicted neural activation in language (STG/IFG), reward (mPFC/precuneus), and urgency (ACC/anterior insula) circuits.

Calibration findings:
- **Hook + emotional resonance → 50% of language/reward activation** (hence 25% + 25% weights)
- **NLP techniques → anterior insula / urgency circuit activation** (20% weight)
- **Specificity → hippocampal encoding** — concrete claims stick (15% weight)
- **CTA framing → frontal-pole decisional activation** (10% weight)

To recalibrate weights with fresh TRIBE data: see `vault/learnings/2026-03-27-tribe-v2-colab-spec-task47.md`.

## Use cases by role

**Sales copy (pre-send):**
"Score this email sequence — I'm targeting homebuyers who browsed last week"

**Social content (pre-post):**
"Score this LinkedIn post and tell me if the hook is strong enough"

**Hook A/B testing:**
"Which of these 3 hooks will perform better and why?"

**Compliance pre-check:**
"Check this for forbidden words before I post it"

**Training data QA:**
"Score Turn 3 of this Emma call transcript for NLP technique usage"

## Integration with agent infrastructure

```bash
# Via Telegram
@openclaw content-scorer "Score this email: [paste]"
@openclaw content-scorer "Compare hooks: [hook A] / [hook B]"

# Via Claude Code
openclaw run content-scorer "Score for LinkedIn: [paste copy]"

# In agent pipelines (JSON mode)
python3 score_content.py "[copy]" --format=json | jq '.composite'
```

## Benchmark scores (reference)

| Copy type | Typical range | Notes |
|---|---|---|
| Generic real estate post | 40-55 | Vague, no hook, weak CTA |
| Good LinkedIn post | 60-75 | Decent hook, some specificity |
| Emma Turn 3 (post-R15) | 72-85 | Strong NLP, assume-the-close CTAs |
| Direct response ad (top 5%) | 85-92 | Hormozi-style, concrete, urgent |
| Perfect score territory | 93-100 | Rarely seen — Claude Sonnet 4.6 + expert copy review |
