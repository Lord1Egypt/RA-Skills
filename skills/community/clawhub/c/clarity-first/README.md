# Clarity First — Intent Detection Protocol for Claude

> Identify the real goal before taking action. Surfaces hidden assumptions, detects ambiguity, and knows when to ask vs. when to proceed.

[![clawhub](https://img.shields.io/badge/clawhub-clarity--first-blue)](https://clawhub.ai/skills/clarity-first)
[![thinkstack](https://img.shields.io/badge/ThinkStack-1%2F3-purple)](https://clawhub.ai/skills/clarity-first)
[![openclaw](https://img.shields.io/badge/openclaw-skill-orange)](https://openclaw.ai)

## The Problem

Claude executes the wrong thing — perfectly. You said "clean this up" and it rewrote the whole file. You said "fix the bug" and it changed behavior you didn't want changed. The request was clear to you; the interpretation was wrong.

Clarity First fixes the gap between what you say and what you mean.

## What it does

**Intent translation** — restates your request as a real goal before acting  
**Assumption inventory** — lists every assumption being made, explicitly  
**Ambiguity scoring** — counts critical unknowns and decides: ask or proceed?  
**Scope guard** — defines what's in and out of bounds before execution starts  
**Lightweight** — a 3-line Clarity Check, not a 3-paragraph interview

## The Rule

| Unknowns | Action |
|----------|--------|
| 0–1 | Proceed. State assumptions inline. |
| 2–3 | Ask 1 question. State the rest as assumptions. |
| 4+ | Ask up to 3 questions first. |

Never more than 3 questions. Never analysis paralysis.

## Installation

```bash
openclaw install clarity-first
```

## ThinkStack

Clarity First is part of the **ThinkStack** — three skills that make Claude smarter at every stage:

```
clarity-first  →  deep-think  →  task-pilot
 understand        analyze        execute
```

```bash
openclaw install clarity-first
openclaw install deep-think
openclaw install task-pilot
```

## Keywords

intent detection · requirements clarification · ambiguity resolution · clarifying questions · ask vs proceed · scope management · assumption detection · user intent · better understanding · eliminate rework · requirements analysis · AI agent improvement · smarter Claude · prompt engineering · agent behavior · 需求澄清 · 意图识别 · 消除歧义

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai](https://clawhub.ai/skills/clarity-first)
