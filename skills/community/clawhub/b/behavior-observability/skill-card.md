## Description:

Behavior Observability records agent and automation pipeline actions as structured events for querying, metrics, and timeline replay to support audit, debugging, and tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add local behavior tracing to autonomous agents and automation pipelines, inspect error and latency metrics, and replay timelines for audits and postmortems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The learning helper stores local usage patterns and preferences that may influence future behavior.

Mitigation: Treat learned_patterns.json as untrusted local state and do not store secrets, sensitive notes, or policy decisions in it.

Risk: The skill describes automatic SKILL.md rewrites after repeated errors or usage thresholds.

Mitigation: Require human review before accepting any generated changes to SKILL.md or other skill instructions.

Risk: The observability CLI does not provide durable cross-run event history.

Mitigation: Verify that the logging model meets the deployment use case before relying on it for audit trails or incident review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/behavior-observability)
- [Publisher profile](https://clawhub.ai/user/qq435912743)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python CLI commands and JSON event, query, metrics, and timeline output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The observability CLI keeps events in memory for each invocation; the learning helper can persist local usage patterns in learned_patterns.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
