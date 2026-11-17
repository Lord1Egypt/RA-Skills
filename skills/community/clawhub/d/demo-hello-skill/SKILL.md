---
name: demo-hello-skill
description: Minimal demonstration skill for verifying a ClawHub publish flow. Prints a configurable greeting and the current date so the publish/ingest path can be exercised with a safe, side-effect-free artifact.
metadata: { "openclaw": { "emoji": "👋" } }
---

# Demo Hello Skill

A tiny skill used to validate the TaskFlow + ClawHub publish flow. It has no
external dependencies and performs no network writes, so it is safe to publish
and re-run.

## When to use

- Smoke-testing a ClawHub publish pipeline.
- Verifying that a freshly published skill installs and renders correctly.
- Demonstrating the input/output contract of a skill in documentation.

## Prerequisites

- POSIX shell with `date` available.

## Basic steps

```bash
# Print the default greeting
demo-hello-skill greet

# Print a custom greeting
demo-hello-skill greet --to "OpenClaw"
```

## Input

- `--to <name>` (optional): override the default recipient. Defaults to `world`.

## Output

A single line on stdout: `hello, <name> @ <ISO-8601 date>`.

## Notes

- This skill intentionally avoids any external side effects so it can be
  republished during a flow test without mutating production state.
