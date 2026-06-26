# AI Engineering Interview

> Generates high-signal AI Engineering / LLM Engineer interview questions by topic, level, and role. Covers LLM fundamentals, prompt engineering, RAG, vector DBs, agents, fine-tuning (LoRA/QLoRA), evals, observability, safety, and production systems. Trigger for requests like "give me interview questions on RAG", "quiz me on agents", "what are senior-level fine-tuning questions", or "interview questions for an AI engineer role".

---

## English

### Why

This skill exists to make ai engineering interview requests repeatable instead of ad-hoc. It gives the agent a clear workflow, expected output shape, and domain boundaries so the result is more consistent and easier to reuse.

### What

This repository contains an OpenClaw skill for this domain.

Core scope: Generates high-signal AI Engineering / LLM Engineer interview questions by topic, level, and role. Covers LLM fundamentals, prompt engineering, RAG, vector DBs, agents, fine-tuning (LoRA/QLoRA), evals, observability, safety, and production systems. Trigger for requests like "give me interview questions on RAG", "quiz me on agents", "what are senior-level fine-tuning questions", or "interview questions for an AI engineer role".

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
give me interview questions on RAG
quiz me on agents
what are senior-level fine-tuning questions
interview questions for an AI engineer role
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
