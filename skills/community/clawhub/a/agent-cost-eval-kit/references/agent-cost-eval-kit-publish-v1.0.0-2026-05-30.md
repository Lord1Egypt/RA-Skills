# Agent Cost Eval Kit — Publish v1.0.0 (2026-05-30)

## Pre-Release Gate

Inspected existing skills:
- waste-audit (v1.8.12): finds recurring OpenClaw job waste
- agent-routing-waste-audit (v1.2.2): finds routing/retry/fallback/model-assignment waste

Gate criteria:

| Criterion | Result |
|---|---|
| User value | PASS — real problem: evaluating whether a change actually worked |
| Clear scope | PASS — evaluation-only, not another audit skill |
| Non-overlap | PASS — does not duplicate waste-audit or agent-routing-waste-audit |
| Verifiability | PASS — before/after summaries, samples, token/cost/latency data, human notes |
| Safety | PASS — no auto-edit, no unsafe model downgrade |

**Decision: Release-ready.**

## Publish

- Source: `/root/.hermes/skills/tokensave/agent-cost-eval-kit/SKILL.md`
- Command: `clawhub publish /root/.hermes/skills/tokensave/agent-cost-eval-kit/ --slug agent-cost-eval-kit --name "Agent Cost Eval Kit" --version 1.0.0 ...`
- Commit ID: `k972negcy48q8hbb5tj2t5nam587padr`
- Public URL: https://clawhub.ai/choosenobody/agent-cost-eval-kit

## Verification

- Title: "Agent Cost Eval Kit" ✓
- Summary: correct ✓
- Install in body: `openclaw skills install agent-cost-eval-kit --global` ✓
- Activation: `eval agent cost change` ✓
- Output format (1-8): all present ✓
- Safety Boundaries: all 10 items present ✓
- Relationship table: all 3 skills present ✓
- What This Will Not Do: all 8 bullets present ✓
- Top install block: `openclaw skills install agent-cost-eval-kit` ✓ (auto-generated, cannot customize)

## Security Audit

Unavailable — no automated security scan on publish.
