# English Listening Coach

> An interactive English listening and dictation coach that guides learners through structured practice sessions using real content from listenaminute.com, breakingnewsenglish.com, dailydictation.com, and englishclub.com. Use this skill whenever someone asks to practice English listening, do a dictation exercise, improve their English comprehension, practice with a transcript, study English from a text or audio source, or says things like "give me an English lesson", "let's do dictation", "help me practice listening", "I want to study English today", or "quiz me on English". This skill runs a full interactive session: fetch a real passage, guide dictation, check answers, give feedback, teach vocabulary, and offer follow-up exercises. Trigger even for casual requests like "let's do some English practice" or "give me something to listen to in English".

---

## English

### Why

This skill exists to make english listening coach requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: An interactive English listening and dictation coach that guides learners through structured practice sessions using real content from listenaminute.com, breakingnewsenglish.com, dailydictation.com, and englishclub.com. Use this skill whenever someone asks to practice English listening, do a dictation exercise, improve their English comprehension, practice with a transcript, study English from a text or audio source, or says things like "give me an English lesson", "let's do dictation", "help me practice listening", "I want to study English today", or "quiz me on English". This skill runs a full interactive session: fetch a real passage, guide dictation, check answers, give feedback, teach vocabulary, and offer follow-up exercises. Trigger even for casual requests like "let's do some English practice" or "give me something to listen to in English".

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
give me an English lesson
let's do dictation
help me practice listening
I want to study English today
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
