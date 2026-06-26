# Chinese Punctuation Rules for Sentence Correction

## Sources

- GB/T 15834-2011 《标点符号用法》
- 国家语委标点符号查询系统: https://gf.ywky.edu.cn/punctuation_cn_text
- 北师大出版科学研究院《标点符号若干用法的说明》

Use national standard first when two references conflict.

## Fast Decision Order

1. Confirm sentence boundary: `。？！`
2. Confirm explanation/prompt relation: `：` vs `——` vs `()`
3. Confirm clause hierarchy: `；` vs `，`
4. Confirm phrase-level listing: `、` vs `，`
5. Confirm quote/title/bracket pairing

## Rule Set (Condensed)

### 1) Comma `，`

- Use `；` (not `，`) between parallel clauses inside a complex sentence.
- Use `、` (not `，`) between short parallel words.
- Delete comma where there is no real pause.
- Add comma where an actual pause exists.
- Use `：` after prompt lead-ins (for example, "我想：").

### 2) Enumeration Comma `、`

- Do not use `、` in approximate numbers: `二三天`, `七八百`.
- If conjunction words appear (`和/或/以及/并且/尤其是/还有`), generally use `，` before conjunction, not `、`.
- Distinguish hierarchy: outer parallel groups use `，`; inner words use `、`.
- Do not use `、` between non-parallel components (modifier-head, subject-predicate, etc.).
- In compact fixed forms, do not split with `、` (for example, `父母亲`, `烹炒煎炸`).
- For abbreviated ranges that mean two specific items, use `、` (for example, `三、四年级`).

### 3) Semicolon `；`

- Use `；` between parallel clauses with internal commas.
- Do not use `；` between simple parallel noun phrases in a single clause.
- If both sides are independent full sentences, use `。` instead of `；`.
- Do not use `；` in non-parallel clause relation (cause-effect, sequence, progression).

### 4) Question Mark `？`

- Use `？` only when the full sentence is interrogative.
- Do not use `？` only because interrogative words appear (`谁/哪/什么/怎样`).
- For strong rhetorical questions, `？！` is valid; order is question then exclamation.

### 5) Colon `：`

- Use after a true lead-in that introduces following content.
- Do not use after pure insertion tags like "某某说" in the middle of a quote.
- Do not overuse inside one sentence (avoid double-colon structure).
- Add colon where prompt relation is explicit but missing.
- Distinguish ratio sign and time notation properly in domain-specific text.

### 6) Quotation Marks `“”` / `‘’`

- For full quoted sentences, terminal punctuation stays inside quotes.
- For partial quotes embedded in a sentence, sentence punctuation stays outside.
- Add quotes to metalinguistic mention and marked special meaning.
- Do not use quotes for indirect speech.
- Keep terminal `？`/`！` if the quoted part carries that tone.
- Multi-level quote order: outer double, inner single, third-level double.

### 7) Book Title Marks `《》`

- Use for works/titles of cultural products (book/article/newspaper/film/music/show).
- Do not use for ordinary product names, certificates, courses, events, awards.
- Keep title text aligned with official name.

### 8) Parentheses `()`

- Place parenthetical note close to the exact referenced content.
- Inline note that explains local phrase should stay inside sentence.
- Note for whole sentence should be placed at sentence level.

### 9) Ellipsis `……`

- Avoid redundant ellipsis when omission is obvious and not stylistically required.
- Do not combine with `等/等等/之类` unless one side is removed.
- Normally do not add another terminal mark after ellipsis.
- Use standard six-dot full-form ellipsis `……`.

### 10) Dash `——`

- Use for strong insertion/explanation/shift/interruption.
- Do not replace needed punctuation arbitrarily with dash.
- Keep dash as one continuous mark in normalized output.

### 11) Exclamation Mark `！`

- Use only for true exclamatory tone.
- Do not replace `。` or `？` with `！` in plain statements/questions.
- If both question and exclamation are needed, use `？！`.

## Correction Policy

- Preserve meaning first, punctuation second.
- Prefer minimal edit; fix local punctuation before rewriting words.
- If punctuation change still leaves grammar broken, do smallest lexical adjustment.
- In uncertain cases, keep original and avoid over-correction.
