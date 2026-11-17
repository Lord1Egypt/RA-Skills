# Long-Conversation Memory Orchestrator

> memory-orchestrator (memory-orchestrator) v1.9.4 · overseas-friendly lightweight layer. 中文版见 [README.md](README.md).

## What it is
Orchestrates long-conversation memory when explicitly invoked by the user or agent, or inspected by a scheduled scan: it counts turns and measured token usage, recommends handoff at thresholds such as 8 turns or 150k tokens, creates recovery packs/checkpoints, compresses history, and archives sessions. Scheduled scans are not a per-turn realtime hook and do not create new dialogs automatically.

## When to use it
Use in any long-running agent workflow that must not lose context or blow past the context window.

## Quick start
```bash
bash scripts/step_orchestrator.sh status --project MyProject
bash scripts/state.sh get
bash $CODEX_HOME/skills/memory-orchestrator/scripts/agent_hook.sh agent=codex active_project=MyProject thread_id=<id>
```

## Install across the three platforms
- **GitHub**: clone or download the repo, copy the skill folder into `$CODEX_HOME/skills/` (or `~/.claude/skills/` / your agent's skill directory).
- **SkillHub**: install the SkillHub lightweight package (text-only). The lightweight package removes platform-only launcher files (`.cmd`/`.ps1`, extensionless scripts and binary language models) and documents the Windows usage inside its own README; the GitHub full package keeps all platform launchers and assets.
- **ClawHub**: install the ClawHub full package, which keeps cross-platform launchers and assets.
- All platform packages serve the same canonical logic; platform copies never change the canonical code.

## Dependencies
Python 3.8+ standard library; optional ctxcompress CLI at $CODEX_HOME/tools/agent-ctx-compress/bin/ctxcompress for history compression.

## Privacy
Monitoring scripts count only turns and token metrics; they do not read message text. Checkpoint/compression reads only the selected project rollout when explicitly invoked, writes locally, and never uploads data. A scheduled scan is a periodic check, not a per-turn lifecycle hook.

## Boundaries / limitations
Does not store chat transcripts; it writes recovery packs and state files locally only.

## License
CC-BY-NC-SA-4.0

---

## Culture note
- `--lang en|zh` controls UI/help/JSON message language (default `zh`); business algorithms are identical in both languages.
- For image-ocr, `--lang` remains the OCR language; UI language is `--ui-lang en|zh`.
- Local Chinese templates and plant/concept dictionaries are NOT replaced; overseas inputs can select alternatives via parameters (e.g. `--plant-library`, `--project-rules`) so existing Chinese users are unaffected.
- Review flags, confidence tiers and evidence coordinates are language-independent fields.
