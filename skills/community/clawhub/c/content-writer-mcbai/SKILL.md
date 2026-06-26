---
name: content-writer
description: Generate high-quality social media posts from research articles and source data. Supports multiple platforms (LinkedIn, Facebook, Twitter/X, TikTok caption, Threads), 6 content formats (Toplist, POV, Case Study, How-to, Story, Hook-List-CTA), multiple tones (default, bold, educational, storytelling, analytical, viral, empathetic, custom), 3 lengths (short/medium/long), and 2 languages (English/Vietnamese). Use this skill whenever the user wants to write a post, create social media content, draft content from research data, generate content in any format, or asks to "write a post", "viết bài", "tạo nội dung", "draft a post", "generate a post from this article", or any content writing from source material.
---

# Content Writer Skill

## Installation

```bash
npx clawhub@latest install content-writer-mcbai
```

Generate professional social media posts from research articles. Supports LinkedIn, Facebook, Twitter/X, TikTok caption, Threads — taking source material and producing polished, platform-optimized posts.

## When to Use

- User has articles/data and wants to create social media posts
- User wants to write a post in a specific format
- User needs content for any platform: LinkedIn, Facebook, Twitter/X, TikTok, Threads
- User asks to "write a post", "viết bài", "tạo content" from any source material
- Works best after using the `content-research` skill to gather sources

## Core Workflow

### Step 1: Gather Inputs

Collect from the user (ask if not provided):

1. **Source material** (required) — article, URL, summary, or raw data
2. **Platform** (default: LinkedIn) — LinkedIn / Facebook / Twitter/X / TikTok / Threads
3. **Content format** (default: toplist) — see 6 formats below
4. **Tone** (default: default) — see Tone Presets
5. **Length** (default: medium) — short/medium/long
6. **Language** (default: Vietnamese) — English or Vietnamese
7. **Number of posts** (default: 1)

### Step 2: Select Format

Read the appropriate format reference file:

| Format | File | Best For |
|--------|------|----------|
| 📋 Toplist | `references/format-toplist.md` | Numbered lists with data |
| 💡 POV | `references/format-pov.md` | Bold opinions backed by data |
| 🏢 Case Study | `references/format-case-study.md` | Deep-dive one story |
| 🛠️ How-to | `references/format-how-to.md` | Step-by-step guides |
| 📖 Story | `references/format-story.md` | Narrative, emotional journey |
| 🎯 Hook-List-CTA | `references/format-hook-list-cta.md` | Facebook viral format |

### Step 3: Apply Platform Rules

Read `references/platform-rules.md` for platform-specific constraints. Quick reference:

| Platform | Max length | Style | Hashtag |
|----------|-----------|-------|---------|
| LinkedIn | 3,000 chars | Professional, data-driven | 3-5 tags |
| Facebook | 63,206 chars | Conversational, emotional, story | 0-3 tags |
| Twitter/X | 280 chars | Punchy, hook-heavy | 1-2 tags |
| TikTok | 2,200 chars (caption) | Casual, trendy, FOMO | 5-10 tags |
| Threads | 500 chars | Conversational, casual | 0-2 tags |

### Step 4: Build the Prompt

Combine:
1. **Brand context** — read `references/brand-context.md`
2. **Format instructions** — from selected format file
3. **Platform rules** — from `references/platform-rules.md`
4. **Source material** — articles/data provided
5. **Tone + Language + Length** instructions

### Step 5: Generate Content

Output rules (non-negotiable):
- **Plain text only** — no markdown rendering on social platforms
- **ZERO asterisks** — no `*`, no `**`
- **No em dashes** (—) — use `-` or comma
- **No source URLs** in post body
- **No markdown** (`#`, `[]`, `()`)
- **Short paragraphs** — 1-2 sentences max
- **Data-driven** — every claim backed by numbers
- For emphasis: use CAPS on 1-2 key words
- Lists: use numbers (`1. 2. 3.`) or arrows (`→`)
- Emoji: use naturally per platform style (Facebook/TikTok: more; LinkedIn: 2-3 max)

### Step 6: Present and Refine

Offer after generating:
- Regenerate with different format/tone/length/platform
- Create variants for A/B testing
- Generate versions for multiple platforms simultaneously

## Format Structures

### Toplist
```
HOOK: Bold claim + specific number
CONTEXT: Why this matters now
LIST: Numbered items with data points
TAKEAWAY: Pattern that emerges
CTA: Engagement question
```

### POV
```
HOOK: Contrarian bold opening
DATA: Evidence with numbers
ANALYSIS: What this means
PREDICTION: Clear position
CTA: Provocative question
```

### Case Study
```
HOOK: Most impressive metric
CONTEXT: Problem that existed
WHAT THEY DID: Strategy + numbers
RESULTS: Concrete outcomes
LESSON: Non-obvious takeaway
CTA: Engagement or MCB AI mention
```

### How-to
```
HOOK: Promise clear outcome
WHY: What people get wrong
STEPS: 3-7 numbered, action verbs
PRO TIP: Non-obvious shortcut
RESULT: What they'll achieve
CTA: "Try step 1 today"
```

### Story (Facebook-optimized)
```
OPENING SCENE: Specific moment, pulls reader in
TENSION: Problem/conflict builds
TURNING POINT: Insight or decision
RESOLUTION: Outcome + lesson
CTA: Relatable question or tag prompt
```

### Hook-List-CTA (Facebook viral)
```
HOOK (1 line): Stop-the-scroll — question, shock, or bold claim
BLANK LINE
LIST: 5-10 short punchy items (emoji optional)
BLANK LINE
CTA: "Tag ai cũng cần biết điều này" hoặc câu hỏi
```

## Tone Presets

Read `references/tone-presets.md` for full details:

| Tone | Style |
|------|-------|
| Default | Data-driven, confident, accessible |
| Bold | Provocative, contrarian, strong positions |
| Educational | Teacher mode, analogies, "here's why" |
| Storytelling | Narrative arc, scenes, emotional |
| Analytical | Research analyst, patterns, comparisons |
| Viral | FOMO-driven, emotional trigger, share-bait |
| Empathetic | Warm, understanding, community-focused |
| Custom | User provides own tone description |

## Length Guidelines

| Length | Words | Chars | Best for |
|--------|-------|-------|---------|
| Short | 50-100 | ~300-600 | Twitter/X, Threads, TikTok caption |
| Medium | 150-300 | ~800-1800 | LinkedIn, Facebook standard |
| Long | 400-700 | ~2500-4500 | LinkedIn deep dive, Facebook story |

## Reference Files

- `references/brand-context.md` — MCB AI brand identity + writing rules
- `references/format-toplist.md` — Toplist format instructions
- `references/format-pov.md` — POV format instructions
- `references/format-case-study.md` — Case Study instructions
- `references/format-how-to.md` — How-to format instructions
- `references/format-story.md` — Story format instructions (Facebook-optimized)
- `references/format-hook-list-cta.md` — Hook-List-CTA viral format
- `references/tone-presets.md` — All tone details + Viral + Empathetic presets
- `references/platform-rules.md` — Platform-specific constraints
- `references/formatting-rules.md` — Critical formatting rules (MUST read)

## Critical Rules (Non-Negotiable)

1. ABSOLUTELY NO asterisks (*) anywhere
2. ABSOLUTELY NO markdown formatting
3. ABSOLUTELY NO em dashes (—)
4. ABSOLUTELY NO source URLs in post
5. Output MUST be plain text only
6. Emphasis = CAPS on 1-2 words max
7. Lists = numbers or → arrows only
8. Emoji = natural, platform-appropriate (not excessive on LinkedIn)


