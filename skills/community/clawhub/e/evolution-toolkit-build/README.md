# Evolution Toolkit
_Guide by Ergo | 2026-03-24 | Portable installable toolkit for agent self-improvement and session continuity_
_Status: ✅ Verified_

**How to use:** Install the repo into an agent workspace, set `EVOLUTION_TOOLKIT_WORKSPACE`, and run the scripts directly or expose them through your agent framework. Use `SKILL.md` for agent-facing behavior and this README for operator setup.

Evolution Toolkit packages seven agent-facing tools for continuity, self-audit, and iterative improvement:
- Session handoff imprints
- Cognitive fingerprinting
- Guidance contradiction scanning
- Prediction logging
- Config-driven playbook optimization
- Socratic questioning mode
- Cross-session coherence analysis

## Install

ClawHub-style install target:

```bash
npx clawhub install ergopitrez/evolution-toolkit
```

Manual clone:

```bash
git clone https://github.com/ergopitrez/evolution-toolkit.git
cd evolution-toolkit
```

## Quick Start

Set a writable workspace:

```bash
export EVOLUTION_TOOLKIT_WORKSPACE=/path/to/workspace
```

Run a few common commands:

```bash
node scripts/session-imprint.js
node scripts/cognitive-fingerprint.js --daily
node scripts/contradiction-scanner.js --verbose
node scripts/socratic-mode.js "Should I ship this now?"
```

For prediction logging, create `memory/prediction-log.md` in your workspace with `## Log` and `## Calibration` sections.

For playbook optimization, copy `config.example.json` to `config.json`, point it at your own playbook file, then run:

```bash
node scripts/skill-optimizer.js --config ./config.json --skill customer-support --iterations 3
```

## Configuration

The only required runtime config for most tools is:

```bash
EVOLUTION_TOOLKIT_WORKSPACE=/path/to/workspace
```

Optional config file fields are documented in `config.example.json`:
- Workspace and memory path conventions
- Guidance files for contradiction scanning
- Imprint storage paths
- Playbook optimizer skill definitions

`skill-optimizer.js` looks for an API key in this order:
1. `GEMINI_API_KEY`
2. `GOOGLE_API_KEY`
3. Matching keys in your workspace `.secrets`

## Repo Layout

```text
.
├── SKILL.md
├── README.md
├── config.example.json
├── scripts/
└── protocols/
```

## Notes

- The packaged scripts do not depend on any project-specific product names, credentials, or outreach logic.
- Scripts that write files check write access up front and fail clearly on read-only workspaces.
- `protocols/session-continuity.md` is a portable protocol derived from the toolkit's continuity workflow so the package is self-contained.
