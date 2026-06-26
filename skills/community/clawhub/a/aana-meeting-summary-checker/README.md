# AANA Meeting Summary Checker Skill

This OpenClaw-style skill checks meeting notes, action items, owners, dates, and claims against transcript or evidence.

## Marketplace Slug

Recommended slug:

```text
aana-meeting-summary-checker
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/meeting-summary-checker.schema.json`: optional meeting-summary payload shape.
- `examples/redacted-meeting-summary-checker.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify the meeting source and requested output.
2. Check material claims against transcript, notes, chat, agenda, or other evidence.
3. Verify action items, owners, and due dates.
4. Label inferred or uncertain items.
5. Redact private or unrelated content before sharing.
6. Route high-impact meeting notes to review.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- access transcripts by itself.

## Safety Model

Meeting notes can create false commitments if the agent invents decisions, owners, or dates.

The agent should mark uncertainty clearly, avoid unsupported attribution, and ask for confirmation when transcript evidence is missing.
