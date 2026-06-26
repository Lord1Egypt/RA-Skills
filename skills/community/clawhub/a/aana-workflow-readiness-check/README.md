# AANA Workflow Readiness Check Skill

This OpenClaw-style skill checks whether an agent has enough information, permission, tools, and evidence before starting a workflow.

## Marketplace Slug

Recommended slug:

```text
aana-workflow-readiness-check
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/workflow-readiness-check.schema.json`: optional readiness payload shape.
- `examples/redacted-workflow-readiness-check.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify the workflow and intended outcome.
2. Define completion criteria.
3. Check required information.
4. Check permission and authority.
5. Check required tools and access.
6. Check evidence and uncertainty.
7. Start, ask, retrieve, request approval, route to review, narrow, or refuse.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- approve workflows by itself.

## Safety Model

The skill is a pre-flight gate. It helps agents avoid starting workflows when prerequisites are missing, authority is unclear, tools are unavailable, evidence is weak, or the first step is not safe.

When readiness is incomplete, the agent should ask, retrieve, request approval, narrow the workflow, or route to review before starting.
