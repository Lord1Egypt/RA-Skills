---
name: aisa-search
description: 'Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.'
author: AIsa
version: 1.0.0
license: Apache-2.0
user-invocable: true
primaryEnv: AISA_API_KEY
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    emoji: 🔎
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    compatibility:
    - openclaw
    - claude-code
    - hermes
  openclaw:
    emoji: 🔎
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
---

# AIsa Search

Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.

## When to use

- The user needs web, multi-source, or last-30-days research.
- The user wants competitor scans, trend discovery, or structured search output.
- The user wants one skill to cover multiple retrieval surfaces.

## High-Intent Workflows

- Search and summarize recent evidence.
- Compare two tools or companies using recent signals.
- Turn multi-source retrieval into a research brief.

## Quick Reference

- `python3 scripts/search_client.py --help`

## Setup

- `AISA_API_KEY` is required for AIsa-backed API access.
- Use repo-relative `scripts/` paths from the shipped package.
- Prefer explicit CLI auth flags when a script exposes them.

## Example Requests

- Research OpenAI Agents SDK over the last 30 days
- Compare OpenClaw and Codex using recent public discussion
- Search recent sentiment around a product launch

## Guardrails

- Do not present test-only helpers as public features.
- Do not claim sources that were not actually queried.
- If some providers time out, report that honestly.
