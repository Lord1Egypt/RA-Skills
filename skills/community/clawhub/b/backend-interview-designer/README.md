# Backend Interview Designer

> Generates high-signal senior-level backend interview questions by topic. Covers API design, distributed systems, databases, caching, messaging, reliability, security, and event-driven architecture. Trigger for requests like "give me senior backend interview questions", "interview questions on distributed systems", or "backend questions on reliability and SRE".

---

## English

### Why

This skill exists to make backend interview designer requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: Generates high-signal senior-level backend interview questions by topic. Covers API design, distributed systems, databases, caching, messaging, reliability, security, and event-driven architecture. Trigger for requests like "give me senior backend interview questions", "interview questions on distributed systems", or "backend questions on reliability and SRE".

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
3. No extra support folders are required beyond `SKILL.md`.
4. Start with a prompt like one of these:

```text
give me senior backend interview questions
interview questions on distributed systems
backend questions on reliability and SRE
```

### Repository Structure

```text
.
├── README.md
├── SKILL.md
```

### Main File

- `SKILL.md`

---
