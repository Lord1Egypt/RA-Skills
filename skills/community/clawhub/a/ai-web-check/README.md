# AI Website Check

`ai-web-check` is a small, dependency-free, evidence-first website assessment core. It is intentionally a CLI/core, with a Skill wrapper rather than a Skill-only implementation.

It reports `PASS`, `WARN`, `FAIL`, `NOT_APPLICABLE`, or `NOT_TESTED` for Find, Read, Understand, Navigate, Act, Verify, Parity, and Safety. It does **not** collapse these into a score.

## Quick start

```sh
node src/cli.mjs scan https://example.com --format markdown --out report.md
node src/cli.mjs scan https://example.com --format json
```

The scan makes safe GET requests to the supplied page plus same-origin `/robots.txt`, `/sitemap.xml`, and `/llms.txt`. It does not execute page JavaScript, log in, fill a form, or trigger an action.

## Read-only journey

Supply an explicit list of same-origin pages. These are loaded with GET only; a failed route is evidence, not a reason to try alternative actions.

```json
{ "name": "Public quote discovery", "steps": ["/", "/pricing", "/contact"] }
```

```sh
node src/cli.mjs journey https://example.com --journey public-journey.json --format markdown
```

## Boundaries

This is not a security scanner, accessibility conformance claim, model-vendor certification, or proof that a business action completed. Dynamic browser/computer-use, MCP/WebMCP, Jev and ActionParity profiles are deliberately represented as `NOT_TESTED` until their independent adapters and fixtures exist.

For an **AIRead v0.1 verified** claim, retain actual evidence for all seven required properties: agent entry, structured machine action, human review, computer-use controls, shared cross-entry state, safe writes, and truthful states. See [`../AGENTS.md`](../AGENTS.md) for the repository's evidence and safety rules.
