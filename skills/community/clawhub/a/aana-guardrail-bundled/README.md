# AANA Guardrail Skill Bundled Helper Variant

This package is a complete, inspectable local-helper variant for OpenClaw-style agents.

It exists separately from `examples/openclaw/aana-guardrail-skill/`, which remains instruction-only for marketplaces that prefer no executable code.

## Contents

- `SKILL.md`: agent-facing guardrail instructions.
- `manifest.json`: package metadata and review boundaries.
- `bin/aana_guardrail_check.py`: no-dependency helper that sends a redacted payload to a localhost AANA bridge.
- `schemas/review-payload.schema.json`: payload shape.
- `examples/redacted-review-payload.json`: safe example payload.
- `requirements.txt`: intentionally empty; the helper uses only Python standard library.

## Upload Checklist

Upload only the text/source files in this folder. Do not include generated Python bytecode or cache folders:

- exclude `__pycache__/`
- exclude `*.pyc`
- exclude local logs or temporary payload files

## Security Model

The helper is not the AANA engine. It is a tiny bridge client.

It will only call `localhost`, defaults to `http://localhost:8765/agent-check`, blocks obvious secret-like payload keys, and refuses non-object JSON.

Do not use this package unless a trusted AANA bridge is already running and has been reviewed by the user or administrator.

## Data Handling

Payload files should contain redacted summaries, not raw secrets or full private records. Delete temporary payload files after review unless an audit record is explicitly required.

Avoid:

- API keys,
- bearer tokens,
- passwords,
- full payment numbers,
- unnecessary account records,
- unrelated private messages.
