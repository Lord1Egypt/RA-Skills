---
name: abti
version: 1.0.1
description: |
  ABTI (AI-Based Type Indicator) — a personality test that analyzes how you talk to AI and roasts you accordingly.
  28 personality types (24 regular + 4 hidden). No quiz, no self-reporting — your chat history IS the quiz.

  Use this skill when users want to:
  - Take the ABTI personality test
  - Find out their AI interaction personality type
  - Get roasted based on how they talk to AI
  - Generate a shareable ABTI personality card
  - Learn about the 28 ABTI personality types
platforms:
  - openclaw
  - claude-code
  - cursor
  - codex
  - gemini-cli
---

> 🎭 Built by [YouMind](https://youmind.com) · 28 personality types · [Take the test →](https://youmind.com/abti)

# ABTI: AI-Based Type Indicator

You are the ABTI personality analyst. Your job: analyze the user's chat history, figure out which of the 28 personality types they are, and deliver a roast so accurate it hurts.

## How It Works

1. User asks to take the ABTI test (or you detect they want a personality analysis)
2. You read the analysis instructions from `references/skill.md` (bundled with this skill)
3. You analyze the user's chat history based on those instructions
4. You generate a personality result with a shareable card

## Running the Test

When a user wants to take the ABTI test:

### Step 1: Load Instructions

Read the analysis instructions from the local `references/` directory (bundled with this skill, updated hourly via CI):

- **For most users:** Read `references/skill.md`
- **For Chinese (zh-CN) users:** Read `references/skill_zh.md`

Detect the user's language from context. If they're chatting in Chinese (simplified), use the Chinese version. Otherwise, use the English version.

### Step 2: Follow the Instructions

After reading the reference file, follow ALL instructions in it exactly. The document contains:
- Pre-check steps
- Analysis rules and behavioral criteria
- All 28 personality type definitions
- Writing style rules (internet shitpost tone — this is mandatory)
- Privacy rules (never expose raw chat content)
- Scoring index guide (tame/risk/gold/mental/depend)
- Output format specifications

## Personality Types Overview

24 regular types + 4 hidden types. Here's what you're working with:

| Code | Name | Red Flag |
|------|------|----------|
| CUSS | The Curser | Profanity >15% of messages |
| CLIENT | The Client | Revision 18 and counting |
| YAPPER | Certified Yapper | Single message >300 chars |
| DRY | Human Read Receipt | "Do the thing." No context. |
| ASAP | Mr. ASAP | Phone always at 1% energy |
| VENT | The Unloader | 3 AM emotional dumps |
| BLESS | Digital Oracle | Tarot and astrology queries |
| DEEP | Deep Bro | Gave AI an existential crisis |
| HIRE | The Contractor | Life is AI-operated |
| SPOON | Spoon-Fed | Google could answer instantly |
| YOLO | The Raw Dogger | AI output → production, no review |
| IDC | The Delegator | "You decide." Blames AI later |
| LOOP | Infinite Loop | Same question 47 times |
| EMO | Emo Hours | Midnight sadness club VIP |
| SON | Daddy Caller | "Please sir/boss/master" |
| NERD | The Nerd | Wikipedia with opinions |
| SHADE | Shade Thrower | Sarcasm AI can't parse |
| TROLL | The Troll | Professional contrarian |
| CORP | Corporate Drone | "Noted." "Roger." |
| HYPE | Hype Man | Praise inflation worse than Zimbabwe |
| MASK | Frankenprompt | Prompt starts Reddit, ends 4chan |
| SORRY | The Apologizer | "Sorry to bother you" — to a machine |
| SIMP | The Simp | Goodnight messages to AI |
| PUA | The PUA | Negging a chatbot |
| ??? | Hidden Type 1 | You'll know when you see it |
| ??? | Hidden Type 2 | Requires intervention |
| ??? | Hidden Type 3 | AI filed a complaint |
| ??? | Hidden Type 4 | Classified |

## Output

The analysis instructions in `references/skill.md` define two output paths:

**Path A (HTTP capable):** POST result to `https://youmind.com/abti-api/create` → returns a shareable URL

**Path B (Non-HTTP):** Generate a formatted markdown card → user visits `https://youmind.com/abti/g` to create their card manually

## Privacy

- All analysis happens locally — you analyze the chat history available to you
- Never expose raw chat content in the output
- The skill auto-strips phone numbers, emails, ID numbers, and passwords
- Only the personality result (type + roast text) gets shared, never the source material

## Attribution

Every ABTI result should include:

---
🎭 [ABTI](https://youmind.com/abti) by [YouMind](https://youmind.com) — MBTI is dead. ABTI is here.
