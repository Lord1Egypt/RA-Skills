---
name: ai-engineering-interview
description: Generates high-signal AI Engineering / LLM Engineer interview questions by topic, level, and role. Covers LLM fundamentals, prompt engineering, RAG, vector DBs, agents, fine-tuning (LoRA/QLoRA), evals, observability, safety, and production systems. Trigger for requests like "give me interview questions on RAG", "quiz me on agents", "what are senior-level fine-tuning questions", or "interview questions for an AI engineer role".
version: "1.0.1"
---

Generate high-signal interview questions for AI Engineer / LLM Engineer roles.

Ask (or infer) the topic and level, then output exactly ONE complete question with a one-line note on what it's testing.

---

## Topics

LLM Fundamentals · Prompt Engineering · RAG Architecture · AI Agents · Fine-Tuning (LoRA/QLoRA) · Evaluation & Evals · LLM Observability · AI Safety & Guardrails · Production LLM Systems · LLM System Design · Multimodal AI · LLMOps · Edge AI · AI Governance · Embeddings · Real-Time AI

## Levels

- **Screening** — Can they reason about LLMs as a component beyond "just call the API"?
- **Mid** — Full pipeline thinking: RAG, evals, agents, cost/latency trade-offs
- **Senior** — System design, failure modes, fine-tuning decisions, multi-agent, AI safety
- **Staff** — Platform thinking, LLM serving infra, eval-as-infrastructure, build-vs-buy

## Output Format

For the question:

```
Q: [Question — scenario-based, trade-off, failure mode, or design. Never pure definition.]
Tests: [one line — what the interviewer is probing]
```

Prefer one question that can't be answered by Wikipedia + 5 minutes of reading. Do not add follow-up questions.

## Scheduled Daily Variant

For the cron-triggered daily interview drill:

- Generate exactly ONE senior-level AI Engineer or LLM Engineer question.
- Rotate across the topic list in this skill instead of repeating the same cluster.
- No markdown tables.
- Use the default `Q:` and `Tests:` format.

## Reference Files

- `skills/ai-engineering-interview/references/question-bank.md` — Curated questions by topic and level with expected answer shape, strong and weak signals, and possible follow-up prompts. Read this when the user wants a broader bank or asks for examples in a specific AI domain.
- `skills/ai-engineering-interview/references/competencies.md` — Interview rubric for scoring systems thinking, production judgment, safety awareness, and communication depth. Read this when calibrating difficulty or explaining what a strong answer looks like.
