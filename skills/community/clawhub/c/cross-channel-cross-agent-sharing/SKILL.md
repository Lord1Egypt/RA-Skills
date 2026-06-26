---
name: cross-channel-cross-agent-sharing
description: Ensure new capabilities gained from workspace-installed tools/packages are propagated across channels and agent sessions. Use when any tool/env/package install (e.g., venv, pip, npm, apt, binaries) unlocks new workflows and you need consistent cross-channel + cross-agent awareness via TOOLS.md updates, reusable skill updates, memory logging, and session notifications.
---

# Cross-Channel & Cross-Agent Skill Sharing

## Execute this workflow whenever workspace capability changes

1. Detect capability change source:
   - New package/tool installed in workspace
   - Existing tool upgraded and behavior changed
   - New env/interpreter path required for capability

2. Update `TOOLS.md` with operational facts:
   - Exact runtime/interpreter path
   - Install command
   - Verify command
   - Package versions
   - One-line usage note

3. Create or update a reusable skill when pattern is repeatable:
   - Add/adjust `SKILL.md`
   - Add scripts under `scripts/` for deterministic steps
   - Keep instructions concise and invocation-focused
   - Prefer adding a verification script for fast capability checks

4. Log event in `memory/YYYY-MM-DD.md`:
   - What changed
   - How to verify
   - Any limits/known caveats

5. Inform current conversation:
   - Summarize new capability
   - Show exact invocation command or trigger phrase

6. Propagate to active related sessions/agents:
   - If likely relevant, send brief sync via `sessions_send`
   - Include only invocation + critical caveat

## Required output format in chat (short)

- **New capability:** <what is newly possible>
- **Use it with:** <exact command / trigger>
- **Scope:** Applies to all channels and sessions using this workspace
- **Caveat:** <if any>

## Quick Verification Helper

Use bundled script to verify interpreter + modules before claiming capability:

```bash
scripts/check_capability.sh <python-bin> <module1> [module2 ...]
```

Example:

```bash
scripts/check_capability.sh ~/.openclaw/workspace/.venv-img/bin/python cv2 PIL numpy
```

## Guardrails

- Do not assume global python/node paths; prefer workspace-scoped env paths
- Do not claim capability before running verify command
- Keep cross-session notices minimal to avoid spam
- If capability is channel-specific (provider restriction), state that explicitly
