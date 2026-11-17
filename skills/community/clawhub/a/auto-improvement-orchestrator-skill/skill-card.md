## Description:

Evaluates, proposes, gates, executes, and iterates improvements to agent skill files using structural scoring, task evaluation, Pareto regression checks, feedback analysis, and rollback support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to measure, improve, and continuously optimize agent skills through candidate generation, multi-signal scoring, execution checks, quality gates, and rollback-aware application of approved changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated improvement modes may edit target skill files and retain changes after gate decisions.

Mitigation: Review generated candidates, diffs, receipts, and backups before enabling auto mode; start with read-only scoring or a single bounded iteration.

Risk: Feedback analysis can inspect local conversation history directories.

Mitigation: Run feedback analysis with --no-snippets and narrow --session-dir or --skill-filter values to limit what is read and stored.

Risk: Persistent or scheduled loops can run unattended and consume budget or repeat unwanted changes.

Mitigation: Avoid cron or continuous mode unless expiry, status checks, approval gates, and explicit cost caps are configured.

Risk: Configured LLM-backed evaluation or judging endpoints may send task or skill content outside the local environment.

Mitigation: Review any configured LLM endpoint and use mock, heuristic, or local-only modes where data handling requirements prohibit external calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanyasheng/skills/auto-improvement-orchestrator-skill)
- [Publisher profile](https://clawhub.ai/user/lanyasheng)
- [README](README.md)
- [Evaluation report](EVALUATION_REPORT.md)
- [Skill improvement pipeline article](docs/article-skill-improvement-pipeline.md)
- [User feedback loop design](docs/design/user-feedback-loop.md)
- [Improvement orchestrator architecture](skills/improvement-orchestrator/references/architecture.md)
- [Improvement orchestrator guardrails](skills/improvement-orchestrator/references/guardrails.md)
- [Improvement phases](skills/improvement-orchestrator/references/phases.md)
- [Skill evaluator adapter](skills/improvement-orchestrator/references/skill-evaluator-adapter.md)
- [End-to-end demo](skills/improvement-orchestrator/references/end-to-end-demo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance, shell command examples, JSON artifacts, diffs, receipts, and modified skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local state, candidate, ranking, execution, receipt, backup, rollback, and feedback artifacts depending on mode and CLI options.]

## Skill Version(s):

1.0.3 (source: ClawHub server release evidence; artifact frontmatter declares 2.0.0 and pyproject.toml declares 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
