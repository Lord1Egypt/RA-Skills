---
name: btc-sprint-stack
description: Trade BTC 5m/15m Polymarket fast markets on Simmer with dry-run-first execution, fee-aware filtering, bankroll limits, flat signal_data, journaling, heartbeat summaries, and a strict BTC-only LLM decision layer.
metadata:
  author: "Codex"
  version: "0.1.0"
  displayName: "BTC Sprint Stack"
  difficulty: "advanced"
---

# BTC Sprint Stack

Use this skill to operate a conservative BTC 5m/15m sprint bot on Simmer.

> **This is a template.** The default signal is short-horizon BTC momentum plus
> Simmer context filters. Replace the signal source, confidence model, or edge
> inputs without changing the execution, journaling, and risk plumbing.

## Operating constraints
- Default to dry-run.
- Use the official `SimmerClient` from `simmer-sdk`.
- Only target BTC fast markets (`5m`, `15m`) from Polymarket.
- Enforce risk defaults from `config/defaults.json`.
- Merge learned tunables from `data/live_params.json` before env overrides.
- Every trade must include:
  - `source`
  - `skill_slug`
  - `reasoning`
  - `signal_data.edge`
  - `signal_data.confidence`
  - `signal_data.signal_source`
- LLM decisions must validate to strict JSON and remain BTC-only.

## Entrypoint
```bash
./.venv/bin/python skills/btc-sprint-stack/main.py --once --dry-run --validate-real-path
```

## Files
- `main.py` — orchestration
- `modules/btc_sprint_signal.py` — momentum and fallback signal
- `modules/btc_regime_filter.py` — time, spread, edge, confidence, fee checks
- `modules/btc_sprint_executor.py` — dry-run/live execution wrapper
- `modules/btc_position_manager.py` — bankroll and position sizing
- `modules/btc_trade_journal.py` — JSONL journal
- `modules/btc_self_learn.py` — bounded parameter suggestions
- `modules/btc_heartbeat.py` — run summary and briefing
- `modules/btc_llm_decider.py` — strict JSON decision layer, provider abstraction, and learning store helpers
- `data/live_params.json` — learned tunables overlay
- `data/pending_rules.json` — pending and applied rule suggestions
- `data/llm_decisions.jsonl` — per-cycle LLM decision log
