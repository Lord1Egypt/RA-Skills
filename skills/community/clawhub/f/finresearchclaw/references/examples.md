# FinResearchClaw Examples

## Preferred execution order

1. Codex
2. Claude Code
3. Direct API / CLI mode

## Default repo

- Local path: `~/.openclaw/workspace/AutoResearchClaw`
- Remote: `https://github.com/ChipmunkRPA/FinResearchClaw`

## Example configs

- `examples/finance_event_study.config.yaml`
- `examples/accounting_forecast_error.config.yaml`

## Example experiment plans

- `examples/finance_event_study.exp_plan.yaml`
- `examples/factor_model_starter.exp_plan.yaml`

## Suggested workflow mapping

### Event study
- Config: `examples/finance_event_study.config.yaml`
- Plan: `examples/finance_event_study.exp_plan.yaml`

### Accounting forecast error / accrual quality
- Config: `examples/accounting_forecast_error.config.yaml`

### Factor model / alpha research
- Plan: `examples/factor_model_starter.exp_plan.yaml`

## Direct CLI fallback

If no coding-agent route is available:

```bash
cd ~/.openclaw/workspace/AutoResearchClaw
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
researchclaw run --config examples/finance_event_study.config.yaml --auto-approve
```

## Notes

- Prefer Codex for iterative repo work and experiment refinement.
- Prefer Claude Code only if Codex is unavailable or explicitly requested.
- Use direct CLI mode as the last resort.
- The install/update helper fetches remotes but does not auto-merge existing working clones.
- If an installed script is not executable after ClawHub install, invoke it as `bash scripts/<name>.sh`.
