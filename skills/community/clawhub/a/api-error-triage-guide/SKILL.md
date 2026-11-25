---
name: api-error-triage-guide
version: 1.0.0
description: Classify API errors and choose the right response: retry, back off, fix the request, or escalate. Use when an integration starts failing or when designing retry logic.
---

# Api Error Triage Guide

## Overview

Not all errors deserve a retry. This guide sorts failures by class — client error, auth, rate limit, server error, network — and maps each to the correct behavior, so integrations fail loudly when they should and recover quietly when they can.

## When to use

When debugging a failing integration or writing the error-handling layer of a new one.

## Workflow

1. **Read the status and body** — the exact code and message, not a summary of them
2. **Classify** — 4xx request problem (fix, don't retry), 401/403 auth (stop, check credentials), 429 rate limit (hard stop until the window passes), 5xx server (bounded retry with backoff), network/timeout (retry once, then check state before assuming failure)
3. **Check idempotency** — before retrying any write, read back whether the first attempt actually landed
4. **Apply backoff** — exponential with jitter; a 429 means stop, not slow down slightly
5. **Log the class, not just the error** — so patterns (always the same endpoint, always at the same hour) become visible
6. **Escalate with evidence** — the exact request, response, timestamps, and what was already tried

## Guardrails

- Never retry a payment or order submission blindly — verify state first
- A 429 is a hard stop for that provider in that task, not a suggestion
- Do not catch-all exceptions into silent success

## Output format

A triage note per failure: class, evidence, action taken, and whether it recovered.

---

Part of the Manteclaw free skill series. These workflow skills are free forever; Manteclaw's paid automation tools (runnable code, not just prompts) live at payhip.com/Manteclaw.
