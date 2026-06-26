---
name: answer-book
description: The Answer Book / 答案之书 — hold a question in your mind, flip to a random page, and receive a short philosophical answer. Supports both English and Chinese; pick the language that matches the user's question. Use when the user asks for the answer book, an oracle, guidance, wants to flip to a page, or needs a yes/no/wisdom-style answer. Trigger words：answer book, the book of answers, flip a page, oracle, ask the book, 答案之书, 翻一页, 问问书, 求一个答案, 神谕.
---

# The Answer Book / 答案之书

A digital version of "The Book of Answers" with both English and Chinese pages. Hold a yes/no (or "should I") question in your mind, then flip to a random page.

## Language selection (important)

Pick the language that matches the **user's question / the language they're chatting in**:

- User wrote in English → use `--lang en` (or omit, en is default)
- User wrote in Chinese → use `--lang zh`
- Mixed / unclear → default to the language the user used in their most recent message

Never mix languages in a single answer — the book speaks one language per flip.

## Usage

```bash
# auto English
python3 scripts/get_answer.py

# explicit language
python3 scripts/get_answer.py --lang en
python3 scripts/get_answer.py --lang zh

# specific page (1-100ish, language still required for choice)
python3 scripts/get_answer.py --lang zh 42
python3 scripts/get_answer.py --lang en 42
```

The script returns a single short answer plus the page number, in the requested language.

## How to present the result

1. State the page number.
2. Show the answer line, prominently.
3. Optionally add one short sentence inviting the user to interpret it themselves — don't over-explain.

## Extending

Edit `scripts/get_answer.py` and add new entries to `ANSWERS_EN` or `ANSWERS_ZH`. Keep each entry short, declarative, and open to interpretation.
