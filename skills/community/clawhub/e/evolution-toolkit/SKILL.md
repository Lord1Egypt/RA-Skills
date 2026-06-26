---
name: evolution-toolkit
description: Use this skill when you need portable agent self-improvement tooling: capture session handoffs, measure reasoning style, scan guidance for contradictions, log predictions, optimize playbooks, run Socratic questioning, or analyze cross-session coherence.
---

# Evolution Toolkit
_Skill by Ergo | 2026-03-24 | Portable toolkit for agent self-improvement across workspaces_
_Status: ✅ Verified_

**How to use:** Set `EVOLUTION_TOOLKIT_WORKSPACE` to the target workspace, then run the script that matches the cognitive task. Load `protocols/session-continuity.md` or `protocols/thinking-partner.md` when the task is about handoffs or problem framing.

## Triggers

Use this skill when the request is about any of these:
- Session end, handoff, continuity, preserving context between runs
- "How am I reasoning?" or "compare these sessions/documents"
- Contradictions, drift, conflicting instructions, stale guidance
- Prediction logging, confidence calibration, decision audits
- Improving a prompt/playbook through repeated eval loops
- Switching into Socratic questioning instead of direct advice
- Cross-session consistency, identity drift, recurring themes

## Workspace

Export a writable workspace before running any script that writes state:

```bash
export EVOLUTION_TOOLKIT_WORKSPACE=/path/to/workspace
```

Expected layout:
- `memory/`
- `memory/imprints/` for session imprints
- `memory/research/` for coherence reports
- `CURRENT.md` if you want session-imprint context
- `memory/prediction-log.md` if you want prediction logging

## Scripts

`scripts/session-imprint.js`
- Interactive session-end handoff.
- Use `--read`, `--list`, or `--diff` to inspect existing imprints.

`scripts/cognitive-fingerprint.js`
- Measures reasoning style across 14 dimensions.
- Useful for one file, today's log, all imprints, or historical comparisons.

`scripts/contradiction-scanner.js`
- Scans guidance files in the workspace for conflicting directives, stale references, and drift.

`scripts/predict.js`
- Logs predictions and audits calibration.
- Requires `memory/prediction-log.md` with `## Log` and `## Calibration` sections.

`scripts/skill-optimizer.js`
- Runs an iterative generate -> evaluate -> improve loop for a configurable playbook.
- Requires a config file; see `config.example.json`.

`scripts/socratic-mode.js`
- Classifies a problem into thinking phase and outputs friction-injecting questions.

`scripts/session-coherence.js`
- Analyzes daily logs for persistent themes, energy, and drift.
- Writes a report to `memory/research/` by default.

## Quick Commands

```bash
node scripts/session-imprint.js
node scripts/cognitive-fingerprint.js --daily
node scripts/contradiction-scanner.js --verbose
node scripts/predict.js add
node scripts/socratic-mode.js "Should I launch now or keep polishing?"
node scripts/session-coherence.js --days 14 --portrait
node scripts/skill-optimizer.js --config ./config.json --skill customer-support --iterations 3
```

## Protocols

Read these only when relevant:
- `protocols/session-continuity.md`: how to end and resume sessions cleanly
- `protocols/thinking-partner.md`: how to add useful friction instead of reflexive answers

## Notes

- Write-capable scripts exit early with a clear warning if the target workspace is not writable.
- `skill-optimizer.js` is intentionally config-driven so the package stays product-neutral.
- The toolkit does not ship credentials. API keys must come from env vars or your own workspace secrets.
