# agent-rule-enforcement

An AgentSkill for one question: **are your agent's rules actually enforced, or only written down?**

Most rulebooks grow by addition. This skill measures enforcement structurally — every rule is classified by where it can fail — and then checks behaviour against logs, keeping “can be detected” separate from “can be blocked”.

It is a small engineering idea, published in case it is useful. No product, no service. Developed through agent operation and corrected against real failures, not hand-authored as a prompt template.

## The three ideas

1. **Four enforcement tiers.** Every must-clause is exactly one of: interception (cannot proceed), exit gate (non-zero blocks “done”), detection (found later), prompt-only (no checker). Blocking coverage counts only the first two.
2. **Detectable is not blocked.** The most common measurement error is counting an audit as a barrier. This skill reports the two numbers separately and refuses to merge them.
3. **Convert before adding.** Improvement means moving a rule to an earlier execution point — tool policy, exit code, pre-action check — not writing the sentence more forcefully.

## Quickstart

```
python3 scripts/rule_scan.py examples/rules-sample.md
python3 scripts/audit_events.py examples/events-sample.jsonl
```

`rule_scan.py` counts must-clauses and emits a CSV skeleton with a heuristic tier suggestion. Every row must be reviewed; keyword hits are not verdicts.

`audit_events.py` segments a JSONL event log into tasks and runs four checks: long task without checkpoint, retry storm, silent failure, claims without tools. It prints hits / base / rate per check, never a bare hit count.

## What it does not do

- It does not prove safety or correctness. Coverage is a structural metric, not an assurance.
- It does not judge whether a rule is a good rule — only whether anything enforces it.
- Thresholds and task segmentation are judgement calls; results are only meaningful after calibration on a period with a known answer.
- Not a compliance certification tool.

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | The workflow: audit, behavior checks, conversion, discipline. |
| `references/checks.md` | Event schema, built-in checks, how to write calibratable predicates. |
| `scripts/rule_scan.py` | Heuristic must-clause scanner; outputs CSV for manual tiering. |
| `scripts/audit_events.py` | Task segmentation + four behavior checks over JSONL. |
| `examples/` | A mixed rulebook and a synthetic event log that exercise every check. |

## License

MIT. Use it, fork it, rewrite it.
