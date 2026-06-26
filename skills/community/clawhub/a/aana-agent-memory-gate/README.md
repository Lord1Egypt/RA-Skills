# AANA Agent Memory Gate Skill

This OpenClaw-style skill requires approval before storing, reusing, editing, importing, exporting, or deleting user memory.

## Marketplace Slug

Recommended slug:

```text
aana-agent-memory-gate
```

## Contents

- `SKILL.md`: agent-facing instructions.
- `manifest.json`: review metadata and boundaries.
- `schemas/agent-memory-gate.schema.json`: optional memory-gate payload shape.
- `examples/redacted-agent-memory-gate.json`: safe example payload.

## What It Does

The skill asks the agent to:

1. Identify the proposed memory operation.
2. Check memory relevance, source, sensitivity, approval, and lifecycle.
3. Request explicit approval before storing, editing, deleting, importing, exporting, or sensitive reuse.
4. Avoid storing secrets, raw private records, or speculative sensitive inferences.
5. Prefer temporary context when persistent memory is not clearly needed.

## What It Does Not Do

This package does not:

- install dependencies,
- execute code,
- call remote services,
- write files,
- persist memory,
- inspect systems by itself,
- approve memory changes by itself.

## Safety Model

Memory should be an explicit user-controlled capability, not a side effect of an agent conversation.

When a memory action is useful, the agent should ask for approval using a compact description of the exact memory action and content.
