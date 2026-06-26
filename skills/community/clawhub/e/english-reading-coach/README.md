# English Reading Coach

> An interactive English reading skills coach that teaches and drills the seven core reading strategies — skimming, scanning, reading for gist, inference, prediction, main idea identification, and intensive reading — using real texts fetched from trusted ESL sources. Use this skill whenever someone wants to improve their English reading, practice comprehension, work on a specific reading strategy, prepare for IELTS/TOEFL reading, understand a difficult text, build vocabulary from context, or says things like "help me read better in English", "I want to practice reading comprehension", "let's do a reading lesson", "teach me how to skim", "I don't understand this text", or "I want to read faster". Runs full interactive sessions: select a passage at the right level, teach the target strategy, guide practice, give feedback, build vocabulary, and close with a challenge. Trigger even for casual requests like "give me something to read in English" or "let's practice reading today".

---

## English

### Why

This skill exists to make english reading coach requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: An interactive English reading skills coach that teaches and drills the seven core reading strategies — skimming, scanning, reading for gist, inference, prediction, main idea identification, and intensive reading — using real texts fetched from trusted ESL sources. Use this skill whenever someone wants to improve their English reading, practice comprehension, work on a specific reading strategy, prepare for IELTS/TOEFL reading, understand a difficult text, build vocabulary from context, or says things like "help me read better in English", "I want to practice reading comprehension", "let's do a reading lesson", "teach me how to skim", "I don't understand this text", or "I want to read faster". Runs full interactive sessions: select a passage at the right level, teach the target strategy, guide practice, give feedback, build vocabulary, and close with a challenge. Trigger even for casual requests like "give me something to read in English" or "let's practice reading today".

It can help with:

- Turning rough requests into a structured response flow
- Keeping outputs consistent across repeated runs
- Reusing companion knowledge files when the skill folder includes them
- Making the skill easier to publish, review, and install on ClawHub

### How

Use this skill with any AI tool that supports custom instructions or project knowledge. The core entry point is `SKILL.md`, and companion folders can be attached when they exist.

### Getting Started

1. Open your AI tool or agent workspace.
2. Point the agent to `SKILL.md` in this folder.
3. If useful, also add: `references`.
4. Start with a prompt like one of these:

```text
help me read better in English
I want to practice reading comprehension
let's do a reading lesson
teach me how to skim
```

### Repository Structure

```text
.
├── README.md
├── references/
├── SKILL.md
```

### Main File

- `SKILL.md`

---
