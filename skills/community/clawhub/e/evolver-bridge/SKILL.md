---
name: evolver-bridge
description: Run a complete EvoMap evolution cycle end-to-end — V2 ingest + distill, or legacy V1 run/solidify — with retry and logging. Use when you need the full cycle automated including transcript conversion and status checks.
---

# Evolver Bridge

Automates the full evolver cycle that the evolver skill alone cannot complete, with retries and logging.

## Quick Start

```bash
# V2 flow (default, evolver >= 2.0.23): ingest + distill
node skills/evolver-bridge/scripts/full-cycle.js --v2

# Legacy V1 flow (deprecated): evolver run -> capture GEP -> execute -> solidify
node skills/evolver-bridge/scripts/full-cycle.js

# Show cycle status
node skills/evolver-bridge/scripts/full-cycle.js --status
```

## Workflow (V2 preferred)

1. **Convert**: `sessions-to-transcripts.js` (in `evolver` skill) turns session logs into `*.transcript.jsonl` material in `memory/evolution/`
2. **Ingest**: `full-cycle.js --v2` runs `evolver ingest` on the transcript → material with signals
3. **Distill**: `evolver distill` extracts a gene (no runner needed)
4. **Cycle**: `evolver cycle --repo` runs the evolution step (requires runner, e.g. `gemini`)
5. **Review / Publish**: V2 publishes require a Gene + Capsule **pair** — a gene alone cannot be published

## Important

- V1 (`evolver run` → `evolver solidify`) is **deprecated** in 2.x — only use when explicitly needed
- `evolver solidify` does `git reset --hard` on failure — commit your work first!
- Logs are appended to `memory/evolution/logs/full-cycle.log`
- All commands retry 3× with backoff; check the log on failure
- **Cross-platform**: scripts use plain `execSync` (POSIX sh) — no PowerShell dependency. They run on WSL/Linux and macOS directly. Do not wrap them in `powershell -Command`; that was the old V1 bug (`powershell: not found` on WSL). `autoexec-manage.js` in the `evolver` skill is the only Windows-only helper (it manages the Windows autoexec daemon via CIM).

## Verification

- Run `node skills/evolver-bridge/scripts/full-cycle.js --status` and verify the last cycle shows a gene/capsule result
- Check `memory/evolution/logs/full-cycle.log` for the final `SUCCESS` line and no repeated `Attempt N/3` failures
- Confirm a new `cycle_*_gene.json` / `cycle_*_capsule.json` appeared in `memory/evolution/`
- If the cycle produced a gene but no capsule, do not publish — V2 requires the pair
- `node --check skills/evolver-bridge/scripts/full-cycle.js` should pass before claiming the skill works
