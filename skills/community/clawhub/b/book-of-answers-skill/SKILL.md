---
name: book-of-answers-skill
description: Route natural-language questions into a three-book answer experience and return one random cited answer with SQLite-backed minimal per-user memory, duplicate-question protection, contextual book switching, and daily fortune. Use when Codex needs to build, run, extend, or debug a pure text conversational skill based on movie, literature, and music quote libraries.
---

# Book of Answers Skill

## Core Workflow

1. Normalize the user input and resolve intents in this order: welcome, fallback, disabled-history notice, daily fortune, contextual switch-book, duplicate check, normal question.
2. Load per-user state from SQLite before generating any answer.
3. Reuse `last_question` only when the input is a switch-book follow-up such as `那用电影版的再测一次`.
4. Block identical questions asked within 300 seconds unless the request is a switch-book follow-up.
5. Persist only `last_question`, `last_answer`, `last_book`, and `last_timestamp` after each successful content response.
6. Default to a random choice between `《电影答案之书》`、`《文学答案之书》` and `《音乐答案之书》` unless the user explicitly specifies a book.
7. Render every answer with both正文 and `出处：...`.

## Project Files

- Use `main.py` as the runtime entry point and local CLI for manual testing.
- Use `service.py` for intent orchestration and response composition.
- Use `router.py` for three-book routing and switch-book detection.
- Use `storage.py` for SQLite persistence and state recovery.
- Use `data/books.json` as the built-in answer corpus for the three themed books.
- Use `skill.json` and `interaction_model.json` as the portable metadata and utterance definitions.
- Use `README.md` as the repository-level setup and usage guide.

## Runtime Rules

- Detect fallback input when the message contains no Chinese or alphabetic characters and is effectively digits or symbols only.
- Prefer explicit book selection when the user names `电影`、`文学` or `音乐` in the same request.
- Keep response formatting stable for normal answers:

```text
我感受到了你的困惑。
正在为你翻开 [book_name]...

它给你的指引是：
「 [答案正文] 」
出处：[出处]
```

## Validation

- Run `python3 main.py --user-id demo-user "明天会好吗"` for a direct single-turn test.
- Run `python3 main.py --user-id demo-user --interactive` for a local REPL.
- Run `python3 -m unittest discover -s tests` to validate key intent and state flows.
- Run `python3 /Users/shaozhaoru/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/shaozhaoru/Documents/book-of-answers-skill` after editing skill metadata.
