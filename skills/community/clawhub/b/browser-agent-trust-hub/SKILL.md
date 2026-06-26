---
name: browser-agent-trust-hub
description: Build and audit trust policies for browser/computer-use agents before they take real-world actions. Use for runtime policy, tool monitoring, domain allowlists, approval gates, and audit evidence for governed OpenClaw browser workflows.
---

# Browser Agent Trust Hub

Use this skill when an OpenClaw agent will browse websites, operate portals, click buttons, submit forms, or call browser/computer-use tools and you need a governed execution policy.

## Workflow

1. Define or collect the browser agent policy: allowed tools, allowed domains, sensitive action keywords, approval rules, and audit requirements.
2. Export planned actions as JSON or use the built-in demo to bootstrap a policy review.
3. Run `scripts/browser_agent_trust_hub.py` to score the workflow and produce a JSON trust report.
4. Treat `BLOCK` and `REVIEW` findings as pre-flight gates before live execution.

## Parameters

- `--policy PATH`: Optional JSON policy file inside this skill directory. Absolute paths and `..` traversal are rejected. If omitted, a safe default policy is used.
- `--actions PATH`: Optional JSON list of proposed tool/browser actions inside this skill directory. Absolute paths and `..` traversal are rejected.
- `--output PATH`: Optional report output path inside this skill directory. Absolute paths and `..` traversal are rejected. Defaults to stdout only.
- `--min-score INT`: Minimum acceptable score before the verdict becomes `REVIEW`.

## Outputs

The script returns JSON with:

- `score`: 0-100 trust score.
- `verdict`: `ALLOW`, `REVIEW`, or `BLOCK`.
- `findings`: Evidence-backed policy gaps.
- `required_controls`: Controls to add before production use.

## Notes

This skill does not browse, click, submit forms, or modify OpenClaw configuration. File inputs/outputs are sandboxed to the skill directory to prevent arbitrary local reads or writes.
