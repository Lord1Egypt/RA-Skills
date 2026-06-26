---
name: finresearchclaw
description: "Finance, accounting, and investment research automation via the FinResearchClaw repo. Use when asked to run autonomous finance research workflows such as event studies, factor-model research, accounting regressions, forecast-error analysis, valuation research, or investment research pipelines. Prefer execution in this order: (1) Codex/ACP Codex when available, (2) Claude Code/ACP Claude, (3) direct API/config mode only as a fallback."
---

# FinResearchClaw

Use this skill to operate the FinResearchClaw repo as a finance-research engine.

## Execution preference

Always prefer these execution modes in order:

1. **Codex first**
   - Prefer Codex / ACP Codex for repo-driven execution, code edits, and iterative finance research runs.
2. **Claude Code second**
   - Use Claude Code if Codex is unavailable or the user explicitly asks for Claude.
3. **API mode last**
   - Use direct `researchclaw` CLI / config / API-style execution only as fallback when coding-agent execution is unavailable or unsuitable.

Do not choose API mode first when Codex or Claude Code is available.

## Core workflow

1. Ensure the FinResearchClaw repo exists locally.
   - Default repo path: `~/.openclaw/workspace/AutoResearchClaw`
   - GitHub repo: `https://github.com/ChipmunkRPA/FinResearchClaw`
2. Select the closest finance workflow:
   - event study
   - factor model
   - accounting forecast error
   - accounting panel regression
   - valuation / investment research
3. Prefer a coding-agent run path first.
4. Fall back to direct CLI/config mode only if coding-agent paths are unavailable.
5. Use example configs and starter plans when they fit.

## Local helper scripts

Use these scripts when helpful:

- `scripts/install_or_update.sh` — clone or update the repo locally
- `scripts/choose_runner.sh` — print preferred execution order and basic availability
- `scripts/run_finance_example.sh` — launch a chosen example in direct CLI mode

When the skill is installed from ClawHub, executable bits on bundled shell scripts may not be preserved on every system. If a direct script call fails with `permission denied`, run it with `bash`, for example:

```bash
bash scripts/choose_runner.sh
bash scripts/install_or_update.sh
```

## Repo paths and examples

If needed, inspect:

- `references/examples.md`

It documents the main example configs, starter experiment plans, and preferred mode selection.
