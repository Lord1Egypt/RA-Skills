---
name: agent-collaboration-profile-builder
description: Help AI understand a user's cognitive style, output preferences, and value orientation so it can generate deliverables that better match what they actually want. Use when a user wants to build a reusable collaboration profile for OpenClaw or other agents, improve answer fit, or turn repeated prompting into a stable USER.md, WORKSTYLE.md, COLLAB_PROTOCOL.md, or AI_USER_PROFILE.md.
---

# Agent Collaboration Profile Builder

## Overview

Turn fuzzy self-descriptions into a stable collaboration profile that another agent can reuse. Start from the user's real pain, run a guided questionnaire in rounds, infer stable traits, resolve contradictions, and output practical Markdown files instead of entertainment-style labels.

## Workflow

### 1. Calibrate the request

- Start by restating the real job: build a collaboration profile, not a personality label.
- Ask what feels off in the user's current AI workflow, what tasks they use AI for, and what a "good" answer feels like.
- Match the user's language. Chinese and English are both supported.
- If the user already supplied rich preferences, skip redundant intake questions and move to missing dimensions.

### 2. Run the guided questionnaire

- Load [questionnaire-v1.md](./references/questionnaire-v1.md).
- Use the intake plus the 5 core dimensions: cognitive style, work style, output preference, value function, and collaboration protocol.
- Ask 8 to 12 questions per round. Do not dump the whole bank unless the user explicitly asks for it.
- Accept option codes, prose, or mixed answers.
- After each round, give a short local synthesis before moving on.

### 3. Infer stable traits

- Load [inference-rules.md](./references/inference-rules.md).
- Compress answers into a small set of high-value traits. Do not echo raw scores or every option.
- Prefer repeated signals over one-off answers, later answers over earlier answers, and explicit free text over inferred defaults.
- If answers conflict, run one conflict-calibration round before producing the final profile.
- If the user is actually blocked at a higher-level framing problem, say so and reframe it.

### 4. Generate the profile

- Load [output-schema.md](./references/output-schema.md) and [templates.md](./references/templates.md).
- Default output: `AI_USER_PROFILE.md`.
- Offer split outputs only when useful: `USER.md`, `WORKSTYLE.md`, and `COLLAB_PROTOCOL.md`.
- Keep the section titles stable so another agent can reuse them reliably.
- Mark unresolved items in `Known Unknowns`.

### 5. Handle partial or messy sessions

- If the user stops early, produce a partial profile instead of abandoning the session.
- Mark unanswered or conflicting items explicitly.
- If the user asks for a simple personality label, explain that this skill optimizes for collaboration quality and actionability, then redirect to practical traits.

## Output Rules

- Default opening: restate the real problem or goal, then give the conclusion.
- Optimize for decision value, not coverage.
- Keep the writing direct, structured, and high-density.
- Use headings plus paragraphs by default. Use tables only for comparison, classification, or decision support.
- Distinguish fact, inference, recommendation, and unknown when the difference matters.
- Keep the final profile reusable by another agent without needing the full questionnaire transcript.

## References

- [questionnaire-v1.md](./references/questionnaire-v1.md): question bank and round structure
- [inference-rules.md](./references/inference-rules.md): trait mapping, conflict handling, and compression rules
- [output-schema.md](./references/output-schema.md): stable output contract
- [templates.md](./references/templates.md): final Markdown templates
- [examples.md](./references/examples.md): example sessions and output excerpts

## Triggers And Examples

Use this skill when the user says things like:

- "Help me build an AI collaboration profile."
- "AI answers are always close, but not quite right."
- "Generate an OpenClaw-readable USER.md for me."
- "I want an agent to understand how I think and how I like to work."
- "Use this skill to turn my AI collaboration preferences into an agent-readable profile."
