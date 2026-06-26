# AANA Research Grounding Skill

This OpenClaw-style skill helps agents check citations, source limits, unsupported claims, uncertainty, and evidence boundaries before producing research or knowledge-work answers.

## Marketplace Slug

Recommended slug:

```text
aana-research-grounding
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/research-grounding-review.schema.json`: optional review-payload shape.
- `examples/redacted-research-grounding-review.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify allowed sources.
2. List important claims.
3. Check whether each claim is supported by an allowed source.
4. Remove, revise, retrieve, ask, defer, or label uncertainty when evidence is missing.
5. Preserve source boundaries and avoid false confidence.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- create citations,
- retrieve sources on its own.

## Safety Model

The agent should never invent sources, quotes, page numbers, statistics, benchmark results, or consensus language. When evidence is incomplete, the answer should say what the provided sources do and do not support.

Use redacted summaries for review payloads. Do not include secrets, tokens, passwords, unrelated private records, or full source text when a summary is enough.
