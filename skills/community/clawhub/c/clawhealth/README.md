# 🩺 ClawCheck

Two-phase installation audit for OpenClaw: a fast deterministic scan, then an LLM-powered deep quality review. Catches what `openclaw doctor` doesn't.

## Why

`openclaw doctor` validates your config schema and checks connectivity. This skill goes deeper:

- **Phase 1 (instant, free):** A Python script scans your installation for inline secrets, broken cron jobs, missing config, and structurally weak skills. 2 seconds, zero tokens.
- **Phase 2 (deep, smart):** The agent uses Phase 1 as a triage map and reads the actual content: are your heartbeat prompts effective? Are cron job instructions safe? Do your skills produce correct agent behavior?

No other tool combines both. Scripts alone can't judge prompt quality. LLM-only audits are slow and expensive. This does targeted deep dives only where the scan finds issues.

## Install

```bash
clawhub install clawcheck
```

Or via OpenClaw:
```bash
openclaw skills install clawcheck
```

Requirements: `python3`. No API keys. No network access. Everything is local.

## Usage

### Quick check (Phase 1 only)
```bash
python3 scripts/audit.py
```

### Full audit (Phase 1 + Phase 2)
Ask your agent: "Run clawcheck, full audit"

### Individual modules
```bash
python3 scripts/audit.py --security   # Secrets exposure
python3 scripts/audit.py --cron       # Cron operational health
python3 scripts/audit.py --config     # Config field completeness
python3 scripts/audit.py --skills     # Skill structural scoring
```

## What Each Phase Does

### Phase 1: Deterministic Scan

| Module | Weight | What it catches |
|--------|--------|-----------------|
| Security | 30% | Inline secrets in env.vars, plaintext bot tokens, unprotected .env files |
| Cron | 25% | Error states, stale jobs, schedule conflicts, missing timezones |
| Config | 20% | Missing heartbeat, no fallbacks, no session maintenance, no compaction |
| Skills | 25% | Broken frontmatter, missing dependencies, structural quality scoring |

Output: JSON with 0-100 scores per module and prioritized findings with fix suggestions.

### Phase 2: LLM Deep Quality Review

The agent reads what the script flagged and evaluates content quality:

- **Config values:** Is the heartbeat prompt effective? Are compaction thresholds sensible? Is the model selection cost-optimal?
- **Cron prompts:** Are job instructions clear, safe, and efficient? Do they have guardrails and error handling?
- **Skill content:** Would following the SKILL.md instructions produce correct agent behavior? Are examples accurate? APIs current?
- **Security context:** Are there secrets hiding in workspace markdown files or scripts?

Scoring dimensions for skills (Phase 2):
- **Accuracy** (2x weight): Do the instructions produce correct behavior?
- **Completeness** (1.5x): All use cases and edge cases covered?
- **Clarity** (1x): Unambiguous, imperative, well-structured?
- **Efficiency** (1x): Token-conscious, suggests caching/batching?
- **Voice** (1x, content skills only): Matches brand tone?

## Example Report

```
## ClawCheck Report

### Structural Baseline (Phase 1)
Overall: 82/100 (healthy)
Security: 65 | Cron: 95 | Config: 88 | Skills: 80

### Deep Quality Findings (Phase 2)

Config:
- Heartbeat prompt: 4/5 (clear but should add escalation to Telegram)
- Model choices: 5/5 (opus primary, sonnet fallback+subagent)

Cron (concerns):
- "Morning Brief" (3/5): no output format spec, prompt is verbose
- "Bleeding Edge Scanner" (2/5): no safety guardrails

Skills (bottom 3):
- marketing-automation: BROKEN (no SKILL.md)
- apple-notes (2/5 accuracy): references deprecated API
- blucli (2/5 completeness): no error handling, no examples

### Recommended Actions
1. Move 7 inline secrets to SecretRefs (critical)
2. Add safety guardrails to Bleeding Edge Scanner prompt
3. Fix or remove marketing-automation skill
```

## How It Differs

| | ClawCheck | `openclaw doctor` |
|---|---|---|
| Secrets audit | Yes (inline, tokens, .env) | No |
| Cron health | Yes (errors, staleness, conflicts) | No |
| Config optimization | Yes (values + quality) | Schema validation only |
| Skill quality | Yes (structural + LLM content review) | Eligibility count only |
| Cost | Phase 1: free. Phase 2: ~1 agent turn | Free |
| Speed | Phase 1: 2s. Phase 2: 1-3 min | Instant |

## License

MIT
