---
name: ai-web-check
description: Run an evidence-first, non-mutating AI website usability assessment. Use for requests such as “检查这个网站 AI 好不好用” or “is this site agent ready?”.
---

# AI Website Check v0.1

Use the bundled CLI; do not infer a pass from page copy alone.

```sh
node src/cli.mjs scan https://example.com --format markdown --out report.md
```

For a bounded, read-only browser journey, create a JSON file containing same-origin GET pages and run:

```sh
node src/cli.mjs journey https://example.com --journey journey.json --format markdown
```

The v0.1 runner never fills forms, authenticates, submits, sends, pays, deletes, or follows cross-origin journeys. Treat `NOT_TESTED` as unknown, not as a pass. A `PASS` is only a statement about the named check and its recorded evidence, never vendor certification.

AIRead v0.1 verification needs additional evidence for structured machine actions, a human review flow, cross-entry state consistency, idempotency/version conflicts, and state truthfulness. This scanner can identify candidates; it cannot certify those runtime properties by itself.
