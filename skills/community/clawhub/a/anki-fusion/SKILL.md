---
name: anki-fusion
description: "Convert any learning material into Anki flashcards — Bloom's taxonomy powered card design"
---

# Anki Fusion (anki-fusion)

Converts textbooks, lecture notes, web articles, and PDF chapters into high-quality Anki flashcards. Applies Bloom's taxonomy to classify knowledge level (remember / understand / apply / analyze) and selects optimal card templates accordingly. Follows Anki best practices: minimum information principle, cloze deletion, avoid ambiguous Q&A.

## Workflow

1. Parse input — accept PDF, web page URL, Markdown notes, textbook chapter text, or raw text. Extract meaningful paragraphs and headings. Handle Chinese, English, and mixed content.
2. Decompose — split into atomic knowledge points. Identify: definitions, lists, processes, formulas, code snippets, key-value pairs, chronological sequences, cause-effect relations.
3. Bloom's classification — assign each knowledge point a Bloom level:
   - **Remember**: facts, dates, terminology → cloze deletion cards
   - **Understand**: concepts, explanations → basic Q&A cards
   - **Apply**: formulas, procedures, code → code / apply cards
   - **Analyze**: compare/contrast, classification → multi-cloze / image cards
4. Apply Anki best practices — one fact per card, concrete cloze hints, avoid "what is X" without context, ensure reversibility where appropriate, add mnemonics for hard items.
5. Multi-template generation — for each classified point, select template:
   - **Basic**: front/back Q&A
   - **Cloze**: `{{c1::term}}` definition with context
   - **Code**: syntax-highlighted snippet + explanation
   - **Image**: diagram labeling with occlusion
6. Add metadata — tags (subject / chapter / difficulty), priority (high-frequency / exam-focused / supplementary), and a learning tip or mnemonics hint per card.
7. Preview + edit — show a 5-card preview for user review. Support edit commands: `drop`, `merge`, `rewrite`, `retag`.
8. Output — generate `.apkg` file (direct Anki import) + card statistics (total cards by type, Bloom level distribution, estimated study time).

## Sample prompts

- `anki-fusion generate --input chapter3.pdf --subject "Computer Networks"`
- `anki-fusion generate --input https://en.wikipedia.org/wiki/Red%E2%80%93black_tree --subject "Data Structures" --difficulty hard`
- `anki-fusion generate --input "The OSI model has 7 layers: Physical, Data Link..." --topic "Networking Basics"`
