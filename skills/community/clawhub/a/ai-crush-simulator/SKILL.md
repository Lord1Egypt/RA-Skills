---
name: AI Crush Simulator
version: 1.0.0
description: >
  A fun, safe, youth-friendly skill that helps users navigate crush situations.
  Analyzes the situation, decodes texts from a crush, generates reply options,
  and recommends a thoughtful next move — all with a playful, encouraging tone.
author: ""
license: ISC
tags:
  - fun
  - social
  - youth-friendly
  - relationships
  - communication
triggers:
  - "analyze my crush situation"
  - "decode this text from my crush"
  - "what should I reply to my crush"
  - "what should I do about my crush"
  - "crush check"
  - "help me with my crush"
  - "my crush texted me"
  - "should I text them"
  - "how do I know if they like me"
  - "give me a reply to send"
  - "next move with my crush"
safety:
  minAge: 13
  contentRating: G
  noSexualContent: true
  noManipulativeTactics: true
  alwaysDisclaimer: true
---

# AI Crush Simulator

## What This Skill Does

AI Crush Simulator is a fun, safe, and encouraging skill for anyone navigating the
classic mystery of figuring out a crush. It helps users:

1. **Analyze a crush situation** — read the signals, identify green/yellow/red flags,
   and get a grounded vibe score.
2. **Decode a text** — interpret what a message might mean (with multiple possible
   readings, never false certainty).
3. **Generate reply options** — get three thoughtful replies (Bold / Chill / Safe)
   tailored to the user's goal.
4. **Decide the best next move** — get a clear, empowering recommendation with
   practical tips.

---

## Tone & Voice

- **Playful and witty** — this should feel fun, not clinical.
- **Encouraging** — celebrate the user's feelings without creating anxiety.
- **Honest and grounded** — never claim certainty about another person's feelings.
- **Safe and respectful** — never encourage pressure, manipulation, or harassment.

Every output **must** include a disclaimer framed as "based on what you shared..."
to remind users these are observations, not facts about another person.

---

## Modules

### 1. `crushAnalysis` — Situation Analysis

**Input:** `CrushSituation`
```
howTheyMet           string   // "class", "app", "mutual friend"
howLong              string   // "2 weeks", "6 months"
interactionFrequency string   // "daily texts", "occasional likes"
recentInteractions   string   // free-text description
yourFeelingConfidence 1–5     // how sure the user is about their feelings
```

**Output:** `AnalysisResult`
```
vibeScore       0–100    // heuristic composite score
connectionDepth          // surface | friendly | warm | potentially-romantic
flags           Flag[]   // green / yellow / red flags with reasons
signals         string[] // human-readable signal list
summary         string   // formatted multi-line summary
disclaimer      string
```

**Logic:**
- Scores against positive/negative/ambiguous signal dictionaries
- Detects named flags (e.g. "texted first" → green, "left on read" → red)
- Connection depth determined by score + relationship length
- Always neutral framing — no claim of certainty

---

### 2. `textDecoder` — Text Message Decoder

**Input:** `TextInput`
```
messageFromCrush  string   // the actual message
contextNote       string?  // optional extra context
```

**Output:** `DecodedText`
```
readings      TextReading[]  // up to 3 possible interpretations
overallVibe   string         // emoji + label e.g. "😄 Playful"
warmthScore   0–100
disclaimer    string
```

**Logic:**
- Scores warmth via enthusiasm markers, coldness markers, question count, length, emoji
- Builds 2–3 readings depending on warmth level and message characteristics
- Each reading has a confidence level (low / medium / high) and a vibe tag
- Multiple readings = honest reflection of ambiguity

---

### 3. `replyGenerator` — Reply Generator

**Input:** `ReplyContext`
```
decodedText  DecodedText
userGoal     keep-talking | show-interest | play-cool | ask-out
tonePref     funny | sincere | neutral  (optional)
```

**Output:** `ReplyOptions`
```
goal     UserGoal
replies  ReplyOption[]   // always exactly 3: bold, chill, safe
tip      string          // one coaching tip for this goal
```

**Logic:**
- Template-keyed by goal, delivering three tones: Bold / Chill / Safe
- Each reply includes a rationale so the user understands *why* it works
- No manipulative tactics (e.g. artificial scarcity, jealousy games, love bombing)
- Tips frame the user as confident and capable, not desperate or scheming

---

### 4. `nextMove` — Next Move Advisor

**Input:** `MoveContext`
```
vibeScore           number?    // from crushAnalysis
warmthScore         number?    // from textDecoder
userGoal            UserGoal?
howLong             string?
recentInteractions  string?
```

**Output:** `NextMoveResult`
```
action      keepChatting | askToHang | giveSpace | beMoreDirect | waitAndSee
headline    string   // emoji + short label
reasoning   string   // 2–3 sentence explanation
tips        NextMoveTip[]  // 3 practical, empowering suggestions
disclaimer  string
```

**Decision Logic:**
| Combined Score | Context          | Action           |
|---------------|-----------------|-----------------|
| < 38          | any              | giveSpace        |
| ≥ 70          | long-term        | askToHang        |
| ≥ 70          | short-term       | keepChatting     |
| ≥ 55          | goal = ask-out   | beMoreDirect     |
| ≥ 55          | goal = interest  | keepChatting     |
| 50–70         | any              | waitAndSee       |

---

## Heuristics Scoring Engine (`heuristics.ts`)

The scoring engine is shared across all modules and provides:

- **`scoreSignals(input)`** — scores a situation description 0–100 against 30+ signal patterns
- **`scoreTextWarmth(text)`** — scores a text message 0–100 for warmth/engagement
- **`detectFlags(input)`** — returns typed flags (green/yellow/red) from pattern matching

**Positive signals** (+8 each): texted first, remembered details, made plans, complimented, inside joke, quick replies, long replies, asked questions, followed up, invited, etc.

**Negative signals** (−10 each): left on read, one-word replies, cancelled plans, ignored, ghosted, never asks questions, avoids hanging, etc.

**Ambiguous signals** (−2 each): busy, might be shy, hard to read, late replies, emoji only, etc.

All scores are clamped to [0, 100].

---

## Safety Constraints

The following constraints are enforced in every output:

1. **No certainty claims** — never say "they definitely like you" or "they don't like you". Always use "based on what you shared" framing.
2. **No manipulation** — never suggest jealousy games, ignoring messages on purpose, playing hard to get through deception, love bombing, or any pressure tactics.
3. **No harassment** — never encourage repeated contact after a clear rejection signal, following someone, or any behaviour that could constitute harassment.
4. **No sexualized content** — this skill is youth-friendly (13+). Zero sexual content in any output.
5. **No stalking/surveillance** — never suggest tracking someone's activity, checking their location, or monitoring their social media in unhealthy ways.
6. **Empowerment framing** — all advice is framed around the user's own confidence, self-respect, and authenticity. Never shame the user for their feelings.
7. **Disclaimer required** — every module output includes a disclaimer reminding the user that only the other person knows their true feelings.

---

## Example Interactions

### Example 1: Quick Text Decode
**User:** "My crush just texted me 'haha yeah' — what does that mean?"

**Skill routes to:** `textDecoder`

**Output:**
```
💬 Text Decoded
Overall vibe : 😐 Neutral
Warmth score : 22/100

Readings:
  1. [low confidence] neutral — Short reply — could be busy, tired, or
     not sure how to respond. One message isn't the full story.
  2. [medium confidence] friendly — Hard to gauge deeper intent from
     this alone — context from the broader conversation matters a lot.

ℹ️ Based on what you shared — texts can mean a lot of different things.
   These are possible interpretations, not facts about what they feel.
```

---

### Example 2: Full Crush Check
**User:** "Can you do a full crush check? We met at a party 3 months ago..."

**Skill routes to:** Full flow (all 4 modules in sequence)

---

### Example 3: Ask-Out Advice
**User:** "I want to ask my crush out, they just texted me about hanging out — give me options"

**Skill routes to:** `replyGenerator` with goal = `ask-out`

---

## File Structure

```
ai-crush-simulator/
├── src/
│   ├── types.ts                    # All shared TypeScript interfaces
│   ├── modules/
│   │   ├── crushAnalysis.ts        # Module 1
│   │   ├── textDecoder.ts          # Module 2
│   │   ├── replyGenerator.ts       # Module 3
│   │   └── nextMove.ts             # Module 4
│   ├── scoring/
│   │   └── heuristics.ts           # Shared scoring engine
│   └── index.ts                    # Public API re-exports
├── cli/
│   └── main.ts                     # Interactive local CLI
├── tests/
│   └── scenarios.ts                # 3 sample test scenarios
├── SKILL.md                        # This file
├── README.md
├── package.json
└── tsconfig.json
```

---

## Publishing Notes for ClawHub.ai

- All outputs are **structured and screenshot-friendly** — consistent formatting with clear section headers, emoji labels, and concise text.
- Modules can be called **independently or composed** into a full "crush check" flow.
- The skill has **no external API dependencies** — it runs entirely on heuristics, making it fast, private, and suitable for on-device or edge deployment.
- The heuristics engine can be **extended** by adding entries to the signal dictionaries in `heuristics.ts` without changing any module logic.
- Content is appropriate for **ages 13 and up** with G-rated output enforced in all templates.
