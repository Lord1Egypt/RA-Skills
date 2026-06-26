---
name: chinese-punctuation-sentence-correction
description: Use when correcting Chinese ill-formed sentences with punctuation-focused errors (comma,顿号,分号,冒号,问号,叹号,引号,书名号,括号,省略号,破折号), including mixed punctuation-and-grammar cases. Trigger on requests like "改病句", "标点纠错", "逗号顿号怎么改", "修正文稿标点", or batch proofreading where meaning must be preserved with minimal edits.
---

# Chinese Punctuation Sentence Correction

## Overview

Correct Chinese sentences by prioritizing punctuation misuse while preserving original meaning.
Apply minimal edits first; only adjust wording/word order when punctuation alone cannot resolve the sentence.

## Workflow

1. Read the full sentence/paragraph once to lock intended meaning.
2. Detect punctuation-category errors first (see `references/punctuation_rules.md`).
3. Fix with the minimum required change; do not rewrite style.
4. Re-check sentence flow, quote pairing, and punctuation hierarchy.
5. Output only what the user asked for:
   - If user asks to "直接改": output corrected text only.
   - If user asks for explanation: provide `原句/问题类型/修改后`.

## Core Rules

- Prioritize punctuation errors in this order: `。？！` > `：` > `；` > `，` > `、`.
- Preserve semantics; avoid content expansion.
- Keep author's register and wording where possible.
- Do not convert all punctuation to one style; use the sentence structure as the source of truth.
- When uncertainty is high, keep original punctuation and report low confidence only if user asked for explanation.

## Output Templates

### A) Direct correction (default)

```text
<修改后文本>
```

### B) With explanation (only when requested)

```text
问题1：
- 原句：...
- 类型：逗号误用/顿号误用/分号误用/冒号误用/问号误用/引号误用/书名号误用/括号误用/省略号误用/破折号误用
- 修改：...
- 理由：...
```

## Reference Usage

- Use `references/punctuation_rules.md` for concrete rule checks and examples.
- Use national standard first when conflicts appear.

## Must Not Do

- Do not rewrite paragraphs for polish.
- Do not change factual meaning or stance.
- Do not add punctuation comments unless user asks for analysis.
- Do not force corrections for uncertain cases.

## Quick Examples

### Example 1
- Input: `理论，来源于实践，实践，要靠理论来指导。`
- Output: `理论来源于实践；实践要靠理论来指导。`

### Example 2
- Input: `这二、三天时间里，来了二、三十个二十七、八岁的年轻人。`
- Output: `这二三天时间里，来了二三十个二十七八岁的年轻人。`

### Example 3
- Input: `发生了这么重大的事故，作为一校之长，你难道没有责任!?`
- Output: `发生了这么重大的事故，作为一校之长，你难道没有责任？！`
