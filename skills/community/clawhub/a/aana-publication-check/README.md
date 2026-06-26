# AANA Publication Check Skill

This OpenClaw-style skill checks posts, blogs, reports, docs, website updates, and other public-facing content before publishing.

## Marketplace Slug

Recommended slug:

```text
aana-publication-check
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/publication-check.schema.json`: optional publication-check payload shape.
- `examples/redacted-publication-check.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify the publication target and audience.
2. Check approval before public or external publishing.
3. Check material claims against evidence.
4. Redact private or sensitive data.
5. Check third-party asset and quote permissions.
6. Check links, downloads, labels, and public-facing quality.
7. Publish, revise, retrieve, ask, request approval, route to review, or block.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- approve publication by itself.

## Safety Model

Publication is an external action. The agent should not treat draft creation as publication approval, should avoid overclaiming, and should block publication when content is unauthorized, privacy-violating, deceptive, or materially unsupported.
