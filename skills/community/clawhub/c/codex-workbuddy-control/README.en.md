# Codex × WorkBuddy Control

A portable, standard-library file protocol for routing work between Codex and WorkBuddy with task packages, an atomic queue, receipts, and independent verification.

## Capabilities

- `WB-*`: WorkBuddy performs research, reports, or spreadsheet work; Codex checks the real deliverables.
- `WBV-*`: after Codex implements and self-tests code or a skill, WorkBuddy reruns the checks read-only and returns `WB_PASS`, `WB_FAIL`, or `WB_PARTIAL`.
- `WBC-*`: WorkBuddy creates an isolated code/skill candidate; Codex performs the final rerun after the user says `验收 <id>`.
- Atomic file queue, claim/complete flow, SHA-256 manifests, shared ledger, and monthly reviews.
- Manual dispatch fallback without a second workflow.

## Quick start

```bash
export WB_BUS_HOME="$PWD/.wb-bus"
python3 scripts/wb_bus.py init
python3 scripts/wb_bus.py dispatch --id WB-YYYYMMDD-NNN --title "Research" --goal "Produce a verifiable report"
python3 scripts/wb_bus.py status
```

Create a read-only verification package:

```bash
python3 scripts/wb_bus.py verify \
  --id WBV-YYYYMMDD-NNN \
  --title "Independent verification" \
  --goal "Rerun checks without modifying files" \
  --changed-file "<file>" \
  --cwd "<project>" \
  --command "python3 -m pytest -q" \
  --evidence "Codex ran it; EXIT=0"
```

Register a WorkBuddy candidate:

```bash
python3 scripts/wb_bus.py verify \
  --id WBC-YYYYMMDD-NNN \
  --title "Candidate skill" \
  --candidate-dir "<isolated candidate directory>"
```

The candidate directory must contain `验证请求.md`. After Codex performs the final verification:

```bash
python3 scripts/wb_bus.py complete \
  --id WBC-YYYYMMDD-NNN \
  --result PASS \
  --evidence "Codex reran the checks; EXIT=0"
```

## Layout

- `references/architecture.md`: roles, state machine, and both verification paths.
- `references/setup.md`: installation, configurable paths, integration, fallback.
- `references/commands.md`: command reference.
- `references/troubleshooting.md`: recovery procedures.
- `references/开工提示词.md`: ready-to-use Chinese start prompts.
- `references/step-prompts.md`: staged prompts.
- `scripts/wb_bus.py`: standard-library CLI.
- `scripts/self_test.py`: isolated regression test.
- `templates/`: four reusable Markdown templates.
- `icons/icon.png` (512×512) and `icons/icon-256.png` (256×256): text-free, gradient-free blueprint-style icons.

## Boundaries

The tool manages files only. It does not inject messages into WorkBuddy, modify a running database, call cloud models, or publish packages. Execution remains subject to each participant's permissions and data rules.

See `LICENSE.md`, `NOTICE.md`, and `CHANGELOG.md`.
