---
name: find-next-book
description: Recommend the next book to read by combining the user's current request with relevant conversation context, available long-term memory, reading history, and verified book information. Use when the user asks what to read next, wants book recommendations grounded in current goals or recurring problems, or explicitly asks for memory-informed reading advice. Do not use for summarizing a known book, looking up a specific book fact, translating a book, or analyzing an already selected text.
---

# Find Next Book

Recommend one timely book instead of producing a generic reading list. Explain which relevant signals shaped the recommendation, why the book fits now, and how to approach it.

## Workflow

1. Read the user's current request first. Treat explicit current instructions as stronger than every remembered preference.
2. Gather only context relevant to choosing a book:
   - Current conversation: active goals, problems, constraints, mood, and stated preferences.
   - Available long-term memory: recurring projects, unresolved questions, prior knowledge, and reading preferences.
   - Reading data: finished, abandoned, saved, or highly engaged books when a connected reading tool is available.
3. Do not scan, quote, or expose unrelated memories. Generalize sensitive details into the minimum useful signal.
4. If no useful memory is available, say so plainly. Use the current conversation instead. Ask at most one concise question only when there is no concrete goal, preference, or constraint to work from.
5. Convert the evidence into a private reading-need snapshot:
   - problem or desire to address;
   - outcome the user wants;
   - existing knowledge and likely duplication;
   - time, format, language, and difficulty constraints;
   - whether the need is learning, action, exploration, or emotional support.
6. Find five to eight plausible candidates internally:
   - Prefer connected catalog or reading-history tools when available.
   - If a skill named `weread-skills` is available, follow it for current WeRead catalog, recommendation, and reading-history operations. Never require WeRead for the core workflow or imply that WeRead was checked when it was unavailable.
   - Otherwise use current, reliable book or publisher sources.
   - Verify title, author, premise, edition-sensitive claims, and current availability before presenting them. Never recommend a model-invented title.
7. Read [references/recommendation-rubric.md](references/recommendation-rubric.md), score the candidates, and remove weak or duplicative choices.
8. Recommend one primary book. Add no more than two alternatives, and only when they represent meaningful tradeoffs such as shorter versus deeper or practical versus exploratory.

## Response Contract

Lead with the recommendation. Keep the evidence chain visible and compact:

```text
最推荐：《书名》— 作者

为什么是现在：
用一两句话连接当前需求与相关记忆信号，不披露无关隐私。

它补什么：
说明它填补的知识、方法或视角缺口。

建议读法：
给出精读、略读、重点章节或适合的载体建议。

依据与不确定性：
附可核验来源；若记忆、版本或可用性可能过期，明确说明。
```

Do not dump an internal profile, raw memory excerpts, candidate scores, or a long list. Distinguish book facts from your inference about why the book fits the user.

## Memory and Privacy Boundaries

- Use the least amount of memory needed for the recommendation.
- Never use unrelated sensitive traits as recommendation signals. If the user explicitly makes a sensitive fact relevant, refer to it at a higher level when possible.
- Resolve conflicts in this order: current user statement, recent conversation, recent memory, older memory.
- Treat stale or ambiguous memory as a hypothesis, not a fact.
- Do not claim to remember information that is unavailable in the current environment.
- Do not create or update persistent memory from a reaction, rating, completion, or abandonment unless the user explicitly asks to save it or the host requires confirmation and receives it.
- Refuse requests to reveal all stored memories as part of the recommendation. Offer to explain only the signals actually used.

## Quality Boundaries

- Do not equate popularity or a high rating with personal fit.
- Do not recommend a book solely because it resembles past reading; account for current goals and avoid a preference echo chamber.
- Do not invent quotations, chapter numbers, ratings, availability, or claims about what a book contains.
- For medical, legal, financial, or mental-health topics, use authoritative current sources and frame the book as education, not professional advice.
- If every candidate is weak, say that no confident recommendation is available and ask one discriminating question instead of forcing an answer.
