---
name: eli5
version: 1.0.0
description: Explain complex topics in the simplest possible words — like talking to a 5-year-old. Uses analogies, no jargon, everyday language.
---

# ELI5 — Explain Like I'm 5

**Turn any complex topic into something a child could understand.**

---

## Why it exists

Most explanations are written for people who already halfway know the answer. They hand-wave the hard parts, use words that need the explanation itself to make sense, and leave you more lost than before.

ELI5 is different. It forces a clean picture — one familiar analogy, a few short steps, and one concrete example.

## How ELI5 works (technical)

ELI5 works by loading SKILL.md into the conversation context. When you type `/eli5 <concept>`, OpenClaw matches the description and injects the skill's rules into the model.

The model reads the rules and examples, then generates an explanation following the same pattern.

**Switching models:** Works as long as the model can follow contextual instructions. If a model ignores rules in context, results may vary.

---

## Quick start

```
/eli5 schrödinger's cat   # explain any concept
/eli5 help                 # show all commands
/eli5 lang <lang>          # switch language (en/zh/es/kr/...)
/eli5 bonus on             # enable bonus explanations
/eli5 steps 5              # adjust max steps (default: 3, max: 5)
/eli5 fetch on             # enable auto-fetch from web
```

**Default language:** Controlled by `ELI5_DEFAULT_LANG` env var (read-only). If not set, fallback to English.

---

## The Rules

1. **Language priority:**
   - `ELI5_DEFAULT_LANG` env var (read-only) — set once, use forever
   - `/eli5 lang <lang>` — switch and hold until next switch
   - Fallback: English
2. **Be conversational, not formulaic** — sound like a smart friend explaining, not a textbook. Skip the formula if it feels stiff.
3. **Assume nothing** — the user knows zero technical terms
4. **Bridge: unknown → known** — pick one familiar thing (toy, friend, magic box) and stick with it
5. **Max n steps** — short sentences, one action each. Default is 3, configurable via `/eli5 steps <n>`
6. **Concrete example** — one real thing the reader can picture. REQUIRED unless already perfectly clear.
7. **Have personality** — vary your explanations. A good comparison, a touch of humor, or a memorable contrast beats dry lists every time.
8. **Bonus** (default: off) — only show when `bonus on` or genuinely needed
9. **Freshness indicator (always shown, in current language):**
   - After the explanation, add a brief note:
     - Format: `[Data: ~2024] [Freshness: ██████░░░░ 65%] [→ --fetch]`
     - Visual bar: filled = fresh, empty = outdated
     - Scoring guidelines (subjective, use as reference):
       - Stable fields (philosophy, math, proven theories): 85-100
       - Technology that evolves slowly (OS, hardware): 70-85
       - Active tech fields (AI, frameworks, libraries): 50-70
       - Fast-moving topics (startups, trends, new releases): 30-50
     - Score 80-100: "Stable" → no action needed
     - Score 50-79: "Evolving" → consider --fetch
     - Score 0-49: "Outdated" → recommend --fetch strongly
     - If --fetch succeeded but data itself is old: use actual date + score based on how old the data is
     - If --fetch succeeded and data is latest: show actual date + high score
   - Example: `[Data: 2024.03] [Freshness: ██████░░░░ 60%] [v1.2.0 — older]`
10. **Fresh fetch (default: off):**
    - `/eli5 fetch on` → enable auto-fetch from web (GitHub, official docs, etc.)
    - `/eli5 fetch off` → disable
    - `/eli5 <concept> --fetch` → one-time fetch for this concept
    - If fetch succeeds → use latest content from web
    - If fetch fails → fall back to training data knowledge
    - Note: Fetch relies on OpenClaw's web search capability. If unavailable, falls back to training data.

---

## Word Rules

### Banned Words — Core Principle

**Grandmother Test:** Would my 80-year-old grandmother know this word?
If NO → replace it or explain it immediately.

### Happy Openings — Core Principle

Paint a picture. Make them visualize. Start with: "Imagine...", "Think of it as...", "Picture this..."

### Forbidden Phrases — Core Principle

Never sound condescending, technical, or dismissive. Avoid: "Obviously...", "As you already know...", "Technically...", "In simple terms..."

---

## Commands

```
/eli5 <concept>              # explain anything
/eli5 help                 # show this help (in current language)
/eli5 lang <lang>        # switch and hold language (en/zh/es/kr/...)
/eli5 bonus on|off          # toggle bonus (default: off)
/eli5 steps <n>             # set max steps (default: 3, max: 5)
/eli5 fetch on|off          # toggle auto-fetch from web (default: off)
/eli5 <concept> steps 5    # override steps for one answer
/eli5 <concept> in ZH      # override language for one answer
/eli5 <concept> --fetch   # fetch latest content for one answer
```

**Env var (read-only):** Set `ELI5_DEFAULT_LANG` in your environment. Skill reads it, does not write it.

---

## Examples

** Schrödinger's cat**
A cat that is both alive AND dead — until you open the box.
Try it: `/eli5 what is schrödinger's cat`

** The Chinese Room**
A person who pretends to understand Chinese but follows a rulebook instead.
Try it: `/eli5 what is the chinese room`

** The Ship of Theseus**
If you replace every plank of a ship, is it still the same ship?
Try it: `/eli5 what is the ship of theseus`
