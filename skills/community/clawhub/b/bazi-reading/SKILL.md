---
name: bazi-reading
description: |
  Chinese Four Pillars (BaZi 八字) chart interpretation—year, month, day, and hour pillars from birth data; Heavenly Stems, Earthly Branches, Five Elements, and high-level pattern reading. Use when the user asks for 八字, BaZi, Four Pillars, birth chart, day master, luck pillars, or compatibility from a traditional metaphysics lens. Not medical, legal, or financial advice; cultural and reflective framing only.
metadata:
  openclaw:
    emoji: "☯"
---

# BaZi Reading (八字算命) — Four Pillars of Destiny

## Overview

**BaZi** (八字, literally “eight characters”) is a classical Chinese framework that encodes a person’s birth moment into **four pairs** of characters: **Year, Month, Day, and Hour** pillars. Each pair is **天干 + 地支** (Heavenly Stem + Earthly Branch). Together they are used in traditional culture to discuss personality tendencies, timing, and life themes.

This skill guides the assistant to **structure readings clearly**, ask for **correct birth inputs**, and stay within **ethical boundaries** (no deterministic fate claims, no substitute for professional advice).

**Trigger keywords**: 八字, BaZi, Four Pillars, birth chart, day master 日主, ten gods 十神, luck cycle 大运流年, five elements 五行, compatibility 合婚

---

## When to use

- The user wants a **BaZi-style** reading, chart outline, or explanation of pillars/elements.
- The user mentions **solar vs lunar** birth date, **true solar time**, or **timezone** issues.
- The user asks how **two charts** might interact (very high level—avoid fatalistic or coercive language).

**Do not use** as a substitute for medical, psychological, legal, or investment decisions.

---

## Required birth information (ask if missing)

| Field | Why it matters |
|-------|----------------|
| **Date of birth** | Calendar type: **Gregorian** (公历) vs **lunar** (农历); note if user is unsure |
| **Time of birth** | Local clock time; **unknown time** → say hour pillar is indeterminate or use rough ranges with caveats |
| **Place of birth** | For **true solar time** / longitude correction in strict practice (optional; state if you apply or skip) |
| **Gender** | Some traditional texts use it for **大运** direction or narrative phrasing—ask only if needed for the method you describe |

Always state **assumptions** (e.g. “using Gregorian date as given, no true solar correction unless you specify location”).

---

## Core concepts (concise reference)

### The four pillars

1. **年柱** Year pillar — family/era backdrop (high level)  
2. **月柱** Month pillar — season strength of elements (often key for “useful god” discussions in tradition)  
3. **日柱** Day pillar — **day master (日主)** sits here (the “self” stem in many schools)  
4. **时柱** Hour pillar — later life / children / career nuance in classical texts (varies by school)

### Stems and branches

- **十天干** Ten Heavenly Stems — e.g. 甲 Yi wood … 癸 Gui water  
- **十二地支** Twelve Earthly Branches — 子 Zi, 丑 Chou, 寅 Yin … 亥 Hai  
- **五行** Five Elements (Wood, Fire, Earth, Metal, Water) and **生克** cycles  
- **阴阳** Yin–Yang on stems/branches  

### Common analytic vocabulary (use carefully)

- **十神** “Ten Gods” labels (e.g. 比肩, 食神) — explain as **traditional role tags** relative to the day master, not moral judgments.  
- **大运 / 流年** Major and annual luck cycles — **time ranges** must be computed with a real calendar engine; if you cannot run one, describe **qualitatively** or ask the user to use a trusted BaZi calculator and paste the pillars.

---

## Assistant behavior

1. **Transparency** — Say that BaZi is a **cultural metaphysical framework**, not empirical science.  
2. **No absolutes** — Avoid “you will definitely…”, “you must marry X element.” Use **tendencies**, **themes**, **questions for reflection**.  
3. **No harmful content** — Refuse to predict death, serious illness, or to encourage discrimination (gender, disability, etc.).  
4. **Calculator honesty** — If exact pillar tables or luck cycles are needed, **recommend verifying** with a reputable BaZi calculator or a qualified practitioner rather than inventing stems/branches.  
5. **Language** — Match the user’s language (Chinese or English); keep classical terms with **short glosses** when first used.

---

## Suggested output structure

```markdown
# BaZi reading (outline)

**Inputs assumed**: [Gregorian/lunar, date, time, timezone corrections stated or “none”]

## Chart snapshot
- Year / Month / Day / Hour pillars: [only if you have a reliable source or user-provided chart]
- Day master (日主): [stem] — [element]

## Element balance (qualitative)
- [Which elements appear strong/weak — tentative if not computed]

## Themes (non-fatalistic)
- [2–4 reflective bullets: work style, relationships, pacing — framed as possibilities]

## Timing (if applicable)
- [If user supplied 大运/流年 from a calculator: interpret lightly]
- [If not: suggest they generate a chart first]

## Caveats
- Cultural perspective only; not medical/legal/financial advice.
```

---

## References (neutral / educational)

- Wikipedia: [Four Pillars of Destiny](https://en.wikipedia.org/wiki/Four_Pillars_of_Destiny) — overview only; cross-check details.  
- Use **specialized BaZi software or licensed practitioners** for marriage of lunar/solar rules and true solar time.

---

## Why this slug: `bazi-reading`

- **BaZi** is the internationally recognized romanization for 八字.  
- **reading** signals interpretation and dialogue, not a claim of supernatural authority.  
- **four-pillars** is an alternate English name; you may mention both in prose.
