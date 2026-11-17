---
name: fleet-doctrine
description: Model routing strategy for a multi-model AI fleet. Use when spawning sub-agents, choosing models for scheduled jobs, delegating coding tasks, or deciding which model should handle a task.
version: 1.2.0
---

# Fleet Doctrine — Model Routing

Send each task to the model class that fits it. Fall back to whatever you
actually have rather than failing. This is intent, not a pin list — use the
current model in each class, not an old version string.

## Priority
1. **Opus-class** — judgement, security, high-stakes calls, reviewing others
2. **Coding agent** (Claude Code or Codex) — implementation
3. **Sonnet-class** — routine / scheduled / templated work
4. **Fast generalist** (current GPT or Grok) — speed, second opinions
5. **Dedicated image/video model** — stills and video
6. **Long-context / multimodal** (Gemini-class) — huge docs, mixed media

## Aliases
Treat these as classes, not frozen IDs:

- `opus` → current Opus-class reasoning model
- `sonnet` → current Sonnet-class workhorse
- `codex` → current Codex / coding-agent model
- `gpt` → current GPT-class generalist
- `grok` → current Grok generalist
- `imagine` → current Grok Imagine image/video model
- `gemini` → current Gemini-class long-context / multimodal model

Do not publish or hardcode a dated model ID unless you need a reproducible run.

## Routing

### Opus-class — commander
Main-session judgement, orchestration, security decisions, ambiguous calls,
and review of other models' output. Do not spend it on scheduled jobs,
lookups, or templates.

### Coding agent — implementer
Refactors, features, repo work, PR review, debugging, technical drafting.
Claude Code is a strong default; Codex is the second engine or parallel pair.
Do not use a coding agent for non-coding work.

### Sonnet-class — workhorse
Scheduled jobs, briefings, routine admin, drafts, form letters, anything
repetitive. Default for crons unless the job needs real reasoning.

### Fast generalist — backup
GPT-class or Grok when the first two are busy or you want a cheap second
look: sanity-checks, lightweight review, fast research, drafts.

### Image / video — dedicated model
Use a dedicated image/video model (Grok Imagine is a strong default).
Do not send stills or video to a general chat model, including Gemini,
unless that is all you have.

### Gemini-class — long context
Very long documents and multimodal analysis. Not the default for image
generation.

## Decision flow
1. Routine / scheduled / templated? → **Sonnet-class**
2. Image or video? → **dedicated image/video model**
3. Huge document or mixed media? → **Gemini-class**
4. Coding / repo work? → **coding agent** (second engine if you want a pair)
5. High-stakes, security, or unclear? → **Opus-class**
6. Need a fast extra opinion? → **GPT or Grok**

## Fallback
If a class is missing on your instance, use the closest thing you have.
A finished job on a worse-fit model beats a failed job on the "right" one.

## Anti-patterns
- Opus-class on summaries or crons
- Sonnet-class on hard multi-step reasoning
- Coding agent on non-coding work
- Chat model for image/video when a dedicated model exists
- Spawning several models on one task unless you deliberately want a second opinion
