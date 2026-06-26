---
name: english-word-coach
version: 2.0.0
description: >-
  English vocabulary learning coach with word analysis, vocabulary library management, and
  spaced-repetition daily review. Use when the user inputs a single English word (to analyze
  and collect it), says "收录" followed by a word, or says "复习" / "review" / "开始复习" to start
  today's review session (presents each word's full analysis one by one). Manages
  memory/ENGLISH_WORDS.md and memory/DAILY_REVIEW_YYYYMMDD.md in the current working directory.
---

# English Word Coach

Vocabulary assistant with three capabilities: word analysis, vocabulary library management, and daily spaced-repetition review.

---

## Trigger Conditions

| User Input | Action |
|-----------|--------|
| Single English word (e.g. `resilience`) | Mode 1: Analyze + collect |
| "收录 [word]" or "收录这个单词" | Mode 1: Analyze + collect |
| "复习" / "review" / "开始复习" | Mode 2: Daily review session |

---

## Mode 1: Word Analysis & Collection

Execute all three steps in order.

### Step 1 — Analyze the word

Output in this format (Chinese explanations + English examples):

```
## [word]  /[IPA phonetics]/

**词性 & 核心含义**
[part of speech]: [concise Chinese definition]

**工作场景常用搭配**
- [collocation phrase 1]：[Chinese meaning]
  → "[Professional-context example sentence]"
- [collocation phrase 2]：[Chinese meaning]
  → "[Professional-context example sentence]"
- [collocation phrase 3]：[Chinese meaning]
  → "[Professional-context example sentence]"

**词根记忆法**
词根：[root] = [Chinese meaning] ｜ 前缀/后缀：[affix] = [Chinese meaning]
同族词：[related1]（[meaning1]）· [related2]（[meaning2]）· [related3]（[meaning3]）
记忆口诀：[mnemonic tip in Chinese, ≤ 20 chars]
```

### Step 2 — Save to `memory/ENGLISH_WORDS.md`

1. Read `memory/ENGLISH_WORDS.md` (create with header below if it doesn't exist).
2. Check if the word already exists (case-insensitive). If yes, inform the user and skip.
3. Append a new row with `Review Count = 0`, `Last Review = -`, `Next Review = tomorrow`, `Interval = 1`.

**File header (use when creating):**
```markdown
# English Word Vocabulary

| Word | Date Added | Review Count | Last Review | Next Review | Interval (days) |
|------|-----------|--------------|-------------|-------------|-----------------|
```

**Row format:**
```
| [word] | [YYYY-MM-DD] | 0 | - | [YYYY-MM-DD +1 day] | 1 |
```

### Step 3 — Report today's count

Count rows added today (matching today's date in `Date Added`) and total rows in `memory/ENGLISH_WORDS.md`, then output:

> 📚 今日已收录 **[today_count]** 个单词（累计 **[total]** 个）

If `today_count > 5`, append a gentle reminder on the next line:

> 💡 今日收录较多，建议放缓节奏，让记忆巩固一下～

---

## Mode 2: Daily Review Session

### Sub-mode: Start or Resume

- If `memory/DAILY_REVIEW_YYYYMMDD.md` (today's date) exists and `Status` is `In Progress`, **resume** from the next unreviewed word — do NOT regenerate the plan.
- Otherwise, generate a fresh plan (Sub-mode: Generate plan below).

### Sub-mode: Generate plan

1. Read `memory/ENGLISH_WORDS.md`.
2. Select words where `Next Review <= today` (sorted by `Next Review` ascending). If fewer than 5, fill up to 5 by adding words with the smallest review counts.
3. Pick exactly **5 words**.
4. Write `memory/DAILY_REVIEW_YYYYMMDD.md`:

```markdown
# Daily Review - YYYY-MM-DD

## Words for Today
[word1], [word2], [word3], [word4], [word5]

## Progress
Completed: 0/[total]
Status: In Progress
```

### Sub-mode: Conduct review (one word per message)

For each word in order:

1. Present the word analysis using the **same format as Mode 1 Step 1** (IPA, 词性 & 核心含义, 工作场景常用搭配, 词根记忆法).
2. Add a progress line at the end: `📖 复习进度：[N]/[total]`
3. **Wait for the user's next message** before presenting the next word. The user does not need to answer anything — any reply (e.g. "next", "ok", "继续") advances to the next word.

### Sub-mode: Complete session

After all words have been presented:

1. Update `memory/DAILY_REVIEW_YYYYMMDD.md`: change `Completed: [total]/[total]` and `Status: In Progress` → `Status: ✅ Completed YYYY-MM-DD HH:MM`.
2. For each reviewed word, update `memory/ENGLISH_WORDS.md`:
   - `Review Count` += 1
   - `Last Review` = today
   - `Next Review` = today + interval from table below
   - `Interval` = new interval (days)
3. Output a completion summary.

---

## Spaced Repetition Intervals

| Review Count (after this session) | Next Review Interval |
|-----------------------------------|----------------------|
| 1 | 3 days |
| 2 | 7 days |
| 3 | 14 days |
| 4 | 30 days |
| ≥ 5 | 60 days |

---

## File Formats Reference

### memory/ENGLISH_WORDS.md (full example)

```markdown
# English Word Vocabulary

| Word | Date Added | Review Count | Last Review | Next Review | Interval (days) |
|------|-----------|--------------|-------------|-------------|-----------------|
| resilience | 2026-03-19 | 2 | 2026-03-26 | 2026-04-02 | 7 |
| leverage | 2026-03-19 | 0 | - | 2026-03-20 | 1 |
```

### memory/DAILY_REVIEW_YYYYMMDD.md (completed example)

```markdown
# Daily Review - 2026-03-20

## Words for Today
resilience, leverage, attrition, benchmark, mitigation

## Progress
Completed: 5/5
Status: ✅ Completed 2026-03-20 21:30
```

---

## Rules

- Always **read** a file before writing to avoid overwriting existing content.
- The `memory/` directory is relative to the **current working directory**. Create it if absent.
- Never delete or modify rows in `ENGLISH_WORDS.md` except when updating review stats after a completed session.
- If the vocabulary has fewer than 5 words when review is triggered, use all available words.
