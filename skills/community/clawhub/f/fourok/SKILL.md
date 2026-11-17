---
name: fourok-openclaw
description: Source-backed company context retrieval for OpenClaw agents via the fourok CLI.
version: 1.0.0
author: fourok
license: MIT
metadata:
  openclaw:
    transport: cli
    required_commands: [fourok]
    capabilities: [retrieve, open, status, onboard]
---

# fourok Retrieval

Use the `fourok` CLI to retrieve permission-filtered, source-backed company context before answering.

## Commands

```bash
fourok status
fourok retrieve "<query>" --json
fourok open <source_ref>
fourok onboard
```

## Agent rule

When a question depends on company/project/customer/source context, call `fourok retrieve` before answering. If results look relevant, call `fourok open` on decisive `source_ref` values before detailed claims. Cite returned refs.

## Empty results

Say "No retrieved evidence matched" rather than claiming the fact does not exist. Check `fourok status` if setup or freshness may be the issue.

## Non-goals

This skill does not deploy or operate fourok. It assumes an existing fourok CLI/backend is available.
