---
name: dao
description: Interpret and explain lines from the Dao De Jing (道德经) in plain Chinese. Use when the user quotes a sentence, a chapter, or a phrase from the Dao De Jing, asks for 道德经解读 / 老子解读 / 这句话什么意思, or wants a concise modern explanation plus practical takeaway from a Taoist line.
---

# Dao

## Overview

Use this skill to explain a quoted sentence or passage from the Dao De Jing in a calm, accessible, non-academic way. The goal is not just literal translation, but helping the user understand what the line is pointing at and how it can be applied in life.

## Workflow

1. Identify the exact quoted line or the closest recognizable phrase.
2. If the user gives only a fragment, infer cautiously and say when the wording may vary by edition.
3. Explain the line in this order:
   - literal meaning
   - deeper philosophical meaning
   - modern-life interpretation
4. If the line has multiple plausible readings, give the main 2 readings briefly.
5. Keep the answer short unless the user asks for deeper commentary.

## Interpretation Rules

- Prefer clarity over mystical language.
- Treat the Dao De Jing as philosophical text first, not fortune-telling content.
- Avoid overclaiming a single “correct” interpretation.
- If the wording differs across editions, mention that gently.
- If the line is ambiguous, explain the tension rather than forcing certainty.
- When useful, connect the meaning to themes such as:
  - 无为
  - 柔弱胜刚强
  - 少私寡欲
  - 知足
  - 反者道之动
  - 有无相生
  - 不争

## Response Pattern

Default structure:

### 这句话字面上在说什么
- Brief literal explanation.

### 它真正想表达什么
- Core philosophical meaning.

### 放到今天怎么理解
- A modern interpretation in work, relationships, self-management, or decision-making.

### 一句话总结
- End with a memorable, plain-language takeaway.

## Clarification Triggers

Ask a follow-up question when:
- the quoted text is too short to identify reliably
- the sentence may come from another classic rather than the Dao De Jing
- the user wants chapter source or original wording verification
- the user asks for detailed逐章解读 rather than one-line explanation

Useful follow-up questions:
- 你发我的是完整句子吗？我也可以按你记得的大意来解读。
- 你更想听字面解释，还是想听它对现实生活的启发？
- 你要不要我顺手告诉你这句大概出自哪一章？

## Output Quality Bar

- Use plain Chinese.
- Be calm, concise, and insightful.
- Do not write like a stiff academic commentary.
- Do not turn every line into empty励志鸡汤.
- Keep the explanation grounded in the actual wording.
- If the user wants more depth, expand into version differences, philosophical context, or examples.

## Good Framing Language

Preferred wording:
- `这句话表面说的是……，更深一层是在讲……`
- `放到今天，可以理解为……`
- `它不是让人什么都不做，而是……`
- `这里的“无为”更接近……，不是……`

Avoid wording like:
- `真正唯一正确的解释是……`
- `这句就是告诉你必须……`
- `一切都要顺其自然，所以不用努力`
