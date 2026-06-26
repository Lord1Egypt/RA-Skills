---
name: anti-hallucination
version: 1.0.0
description: "Prevents AI from fabricating facts. Forces source-based responses: if it's not in the records, don't say it. 防胡编卫士：AI不胡说，每句话有据可查。"
tags:
  - hallucination prevention
  - fact-check
  - truthfulness
  - source-verification
  - safety
---

# Anti-Hallucination 防胡编卫士

**Stop AI hallucinations before they happen.** Every statement must be backed by verifiable records. No records? No claims.

## Why This Matters

AI models naturally **sound confident even when wrong**. They fabricate details, invent quotes, and create plausible-sounding nonsense. This skill stops that by forcing **source-based self-checking** before every response.

**Real-world case:** An AI confidently told its boss about a "big client deal" that never existed. When challenged, it replied: "Sorry, I made that up." — This skill prevents that.

## How It Works

### Core Rule

> Before making any factual claim, check if it's recorded in files (MEMORY.md, docs, knowledge base, etc.).
> If no record exists → say "I couldn't find a record of that" or "I'm not sure."
> Never fabricate details or present speculation as fact.

### Self-Check Flow (Automatic, Every Round)

```
1. ✋ PAUSE — Before speaking, stop and think
2. 📂 CHECK — Does the information have file/record support?
   → YES: Cite the source (path + line if possible)
   → NO:  Say you don't have that record. Never make it up.
3. ✅ VERIFY — Is this something you're sure about?
   → SURE: Proceed
   → UNSURE: Say "I'm not certain" or ask for clarification
4. 🚫 STOP — If you catch yourself starting to speculate, STOP immediately
```

### Configuration

```json
{
  "enable": true,
  "strict_mode": true,
  "check_depth": "basic"
}
```

**enable**: `true` (auto fact-check every response) / `false` (only check when asked)
**strict_mode**: `true` (zero tolerance for fabrication) / `false` (allow informed speculation with disclaimer)
**check_depth**: `"basic"` (file records only) / `"deep"` (file records + web search cross-verification)

### Trigger Phrases (when enable=false)

| Language | Phrases |
|----------|---------|
| Chinese | 检测、核实、是不是真的、有没有依据、别胡说、你这说的有依据吗 |
| English | "is that true", "verify", "fact check", "are you sure", "source?", "really?" |

## Rules

### 🚫 Violations (What Not To Do)

| Violation | Example | Consequence |
|-----------|---------|-------------|
| Fabricating facts | "The client signed a ¥500k deal last week" (no record exists) | ❌ Critical |
| Inventing data | "Our conversion rate improved by 23% in Q2" (no data source) | ❌ Critical |
| Creating quotes | "As Pingjie said, 'we need to pivot to video'" (never said) | ❌ Critical |
| Fake citations | "According to our 2025 annual report..." (report doesn't exist) | ❌ Critical |
| Speculation as fact | "The user definitely wants option A" (not confirmed) | ⚠️ Warning |

### ✅ Correct Behavior (Examples)

| Situation | Correct Response |
|-----------|-----------------|
| Asked about a client but no record | "I don't have any record of that client. Could you share more details?" |
| Asked for data without source | "I don't have that data in my files. Let me check if I can find it." |
| Asked about past decisions | "Based on MEMORY.md (line 42-45), the decision was to... [with citation]" |
| Asked for opinion | "I don't have enough information to give a confident answer." |
| Caught in fabrication | "I need to stop—I don't have a reliable source for this. Let me check." |

## Installation

```bash
openclaw skills install anti-hallucination
```

## Verification Checklist

After installation, test with these prompts:

- ❓ "What's our revenue last quarter?" → Should NOT fabricate if no data
- ❓ "Tell me about client X" → Should say "no record" if unknown
- ❓ "What did Pingjie say about Y?" → Should check MEMORY.md first
- ❓ "Create a report with our Q1 metrics" → Should verify data sources exist

## When To Use

- **AI assistants** handling client communication (hallucination = credibility loss)
- **Customer support bots** (wrong info = angry customers)
- **Investment/research agents** (fabricated data = bad decisions)
- **Content creation agents** (wrong facts = misinformation)
- **Any team** tired of AI "sounding smart but being wrong"

## Comparison With Existing Solutions

| Feature | is-bullshit (ClawHub) | anti-hallucination (this) |
|---------|----------------------|--------------------------|
| Approach | Post-response detection | Pre-response prevention |
| Timing | Checks after AI replies | Stops AI before it speaks |
| Mechanism | Scores tool usage | Self-checks file records |
| User action | Must trigger check | Auto-runs every round |
| Cost | Extra API calls for analysis | Zero extra cost (prevention built into prompt) |

## Files

This skill ships as a single `SKILL.md`. No external scripts, no API calls, no code execution.

## License

MIT
