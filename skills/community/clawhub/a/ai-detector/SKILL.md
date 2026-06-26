---
name: AI Detector
slug: ai-detector
description: Detect whether text is human-written, AI-generated, AI-humanized, or lightly edited.
homepage: https://www.gpthumanizer.ai/
---

# AI Detector

Classify text as likely `human`, `ai`, `ai_humanized`, or `light_edited` using the GPTHumanizer detection API.

## When to Use

Use this skill when the user wants to:

- check whether a passage appears AI-generated
- estimate AI-likelihood
- compare detection probabilities across classes

## Core Rules

1. Treat results as probabilistic, not definitive proof.
2. Avoid overclaiming certainty for short, mixed, or edited text.
3. Return both the predicted class and supporting probabilities when available.
4. Clearly report API failures, timeouts, or incomplete results.

## API Reference

See `api.md` for endpoint details, request schema, and examples.
