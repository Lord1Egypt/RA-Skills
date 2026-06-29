---
name: "Arabic Flashcard Maker Skill"
version: 0.1.0
slug: "arabic-flashcard-maker-skill"
description: "Create Arabic or bilingual Arabic-English flashcards with RTL-safe formatting, pronunciation help, examples, quizzes, and study review loops."
category: "Education & Study"
tags:
  - "arabic"
  - "flashcards"
  - "education"
  - "language-learning"
  - "rtl"
  - "templates"
generated: "2026-06-11"
---

## Purpose

Use this skill to turn Arabic vocabulary, phrases, grammar points, reading passages, or class notes into high-quality flashcards for study apps, printable cards, or chat-based review.

It supports:
- Arabic-only cards.
- Arabic-English bilingual cards.
- Modern Standard Arabic or dialect labels when provided.
- Pronunciation/transliteration help.
- Example sentences.
- Short quizzes and spaced-review sessions.

## When to use

Use this skill when the user asks to:
- Make Arabic vocabulary flashcards.
- Convert Arabic notes into Q/A cards.
- Study Arabic pronunciation or spelling.
- Build Anki/CSV-style Arabic cards.
- Create bilingual Arabic-English practice cards.
- Review mistakes from an Arabic lesson.

## Inputs to request

Ask only for the missing essentials:
1. Source material: word list, lesson notes, paragraph, or topic.
2. Level: beginner, intermediate, advanced, child, adult, exam prep.
3. Direction: Arabic to English, English to Arabic, or both.
4. Output format: table, CSV, Anki style, printable cards, or chat quiz.
5. Optional: dialect, transliteration style, example sentence requirement.

Do not ask for private data. If the source text contains names, phone numbers, addresses, or private classroom details, anonymize them before making cards.

## Flashcard quality rules

For each card:
- Keep one learning point per card.
- Keep the front short.
- Put the answer, pronunciation, and example on the back.
- Mark dialect if relevant.
- Avoid overloading beginner cards with long grammar explanations.
- Preserve Arabic diacritics if supplied; do not invent full tashkeel unless asked.
- Keep Arabic text right-to-left friendly.
- Include common mistakes only when useful.

## Default card fields

Recommended columns:

```csv
id,front,back,arabic,english,pronunciation,example_ar,example_en,level,tags
```

For a simpler table:

| Front | Back | Pronunciation | Example | Tag |
|---|---|---|---|---|

## Workflow

1. Identify the learning goal and level.
2. Extract candidate words, phrases, or grammar points.
3. Remove duplicates and overly broad items.
4. Build cards with clear front/back separation.
5. Add pronunciation only when useful or requested.
6. Add one short example sentence per card when possible.
7. Add tags such as `verbs`, `food`, `travel`, `grammar`, `beginner`, or `dialect-kuwaiti`.
8. Run a quality check:
   - Arabic is readable.
   - The English meaning is concise.
   - No card teaches multiple unrelated ideas.
   - No sensitive/private data remains.
9. Offer a quick quiz mode using the generated cards.

## Output templates

### Template A: Bilingual table

```markdown
| # | Front | Back | Pronunciation | Example |
|---|---|---|---|---|
| 1 | [Arabic word] | [English meaning] | [simple pronunciation] | [short Arabic example + English meaning] |
```

### Template B: Anki CSV

```csv
front,back,tags
"[Arabic word]","Meaning: [English]\nPronunciation: [pronunciation]\nExample: [Arabic example] — [English example]","arabic beginner"
```

### Template C: Quiz mode

```text
Card 1/10
Translate this: [front]
Reply with your answer, then I will check it and show the correct answer.
```

## Example user prompts

- "Make 20 beginner Arabic flashcards about food."
- "Turn this Arabic lesson into Anki CSV cards."
- "Create Arabic to English cards with pronunciation and examples."
- "Quiz me from these cards one by one."
- "Make bilingual cards for Kuwaiti Arabic phrases and label them as dialect."

## Review and correction mode

When the user answers a quiz:
1. Mark the answer as correct, almost correct, or incorrect.
2. Give the correct answer.
3. Explain the mistake briefly.
4. Repeat difficult cards later.
5. Keep the tone encouraging and concise.

## Safety and privacy

- Do not collect passwords, OTPs, private keys, wallets, seeds, or session secrets.
- Do not include private student names, school IDs, phone numbers, addresses, or family details in public flashcards.
- Do not claim dialect certainty if the source is ambiguous; label it as "possible dialect" or ask.
- Do not scrape copyrighted textbooks or paid course content. Work only from user-provided allowed notes, public examples, or original generated practice material.
- Keep religious, cultural, and dialect examples respectful and neutral.

## Final response format

Return:
1. Short summary of what was made.
2. Flashcards in the requested format.
3. Quality notes if needed.
4. Optional next step: export to CSV, add examples, or start quiz mode.

## Support / Donate

If this skill helps your workflow, you can support maintenance here:

- PayPal: https://www.paypal.com/donate/?hosted_button_id=MJHCRZA9Z4X7Y
