# English Writing Coach

> An interactive English writing coach that teaches, drills, and gives detailed feedback across all major writing types — professional emails, academic essays, reports, creative writing, IELTS/TOEFL writing tasks, and everyday communication. Uses a process-genre approach: teach the genre conventions first, model a strong example, guide the learner through planning and drafting, then give structured feedback on content, coherence, vocabulary, and grammar. Use this skill whenever someone wants to improve their English writing, get feedback on a draft, practice a specific writing type, prepare for IELTS or TOEFL writing, learn how to write professional emails, fix grammar and vocabulary mistakes, or says things like "help me write better in English", "check my essay", "teach me how to write emails professionally", "I want to practice IELTS writing", "how do I structure a report", or "give me a writing exercise". Trigger even for casual requests like "can you fix my writing" or "I want to write better".

---

## English

### Why

This skill exists to make english writing coach requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: An interactive English writing coach that teaches, drills, and gives detailed feedback across all major writing types — professional emails, academic essays, reports, creative writing, IELTS/TOEFL writing tasks, and everyday communication. Uses a process-genre approach: teach the genre conventions first, model a strong example, guide the learner through planning and drafting, then give structured feedback on content, coherence, vocabulary, and grammar. Use this skill whenever someone wants to improve their English writing, get feedback on a draft, practice a specific writing type, prepare for IELTS or TOEFL writing, learn how to write professional emails, fix grammar and vocabulary mistakes, or says things like "help me write better in English", "check my essay", "teach me how to write emails professionally", "I want to practice IELTS writing", "how do I structure a report", or "give me a writing exercise". Trigger even for casual requests like "can you fix my writing" or "I want to write better".

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
help me write better in English
check my essay
teach me how to write emails professionally
I want to practice IELTS writing
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
