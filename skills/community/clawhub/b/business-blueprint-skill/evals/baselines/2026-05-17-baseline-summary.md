# Business Blueprint Skill Eval Baseline - 2026-05-17

Command:

```bash
python3 scripts/run-skill-evals.py --root . --runner fixture --format json --json-out evals/baselines/2026-05-17-skill-evals-fixture.json
```

Baseline score:

| Metric | Value |
| --- | ---: |
| Cases | 6 |
| Passed | 6 |
| Failed | 0 |
| Incomplete | 0 |
| Average score | 99.67 |
| Outcome average | 25.00 |
| Process average | 25.00 |
| Style average | 24.67 |
| Efficiency average | 25.00 |

Case scores:

| Case | Score | Outcome | Process | Style | Efficiency |
| --- | ---: | ---: | ---: | ---: | ---: |
| explicit-blueprint | 100 | 25 | 25 | 25 | 25 |
| implicit-meeting-notes | 99 | 25 | 25 | 24 | 25 |
| contextual-domain-knowledge | 100 | 25 | 25 | 25 | 25 |
| boundary-projection-handoff | 99 | 25 | 25 | 24 | 25 |
| negative-report | 100 | 25 | 25 | 25 | 25 |
| negative-slide-deck | 100 | 25 | 25 | 25 | 25 |

The default baseline is agent-agnostic: it uses checked-in normalized fixture
traces and never invokes Codex, Claude, Qoder, OpenClaw, model APIs, or network
access.
