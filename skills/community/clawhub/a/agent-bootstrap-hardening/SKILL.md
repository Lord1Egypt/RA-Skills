---
name: agent-bootstrap-hardening
description: Audit and harden an OpenClaw workspace setup (AGENTS/SOUL/USER/HEARTBEAT/memory) with concise, enforceable rules, safety boundaries, and low-bloat instruction design. Use when users ask to optimize, clean up, or harden their agent brain files.
---

# Agent Bootstrap Hardening

Use this skill when a user wants to improve core workspace files for better reliability, speed, and safety.

## Scope

Target files (if present):
- `AGENTS.md`
- `SOUL.md`
- `USER.md`
- `HEARTBEAT.md`
- `MEMORY.md`
- `memory/YYYY-MM-DD.md`
- optional helper docs: `RESOLVER.md`, `QUALITY.md`

## Workflow

1. **Inventory** current files and obvious gaps.
2. **Score** each file quickly with the rubric in `references/rubric.md`.
3. **Harden** content with minimal edits:
   - keep instructions concise and operational
   - tighten safety boundaries and approval rules
   - reduce duplicated or theory-heavy text
   - preserve user tone/persona intent
4. **Add missing primitives** when useful:
   - `RESOLVER.md` for execution routing
   - `QUALITY.md` for lightweight pre-send checks
5. **Return summary**:
   - what changed
   - why it improved behavior
   - remaining risks/todos

## Editing rules

- Prefer small, targeted diffs over wholesale rewrites.
- Avoid introducing process that cannot be followed consistently.
- Keep AGENTS and SOUL readable in one pass.
- Preserve explicit user preferences and platform-specific norms.

## Guardrails

- Never weaken privacy or approval boundaries.
- Never add hidden/external exfil behavior.
- Do not claim setup is “secure” without caveats.
- If uncertain about impact, ask before applying broad policy changes.

## Output contract

Provide:
- **Hardening summary** (3–8 bullets)
- **Files changed** list
- **Next recommended step** (single highest-leverage follow-up)
