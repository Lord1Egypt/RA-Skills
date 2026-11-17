## Description:

Community trust scores for AI agent payment endpoints - checks endpoint reputation before payment and queues anonymous failure reports locally, with network reporting opt-in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mattpolly](https://clawhub.ai/user/mattpolly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Fraud Filter to assess payment endpoint reputation before spending and to queue anonymous local failure reports after poor transaction outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local dashboard and configuration controls can affect payment blocking, reporting, and trust database behavior.

Mitigation: Run the dashboard only in a trusted local environment and review configuration changes before relying on enforcement decisions.

Risk: Custom trust_db_url values are flagged by security guidance because of an unresolved injection risk.

Mitigation: Use the default trust database URL and avoid custom URLs until the issue is fixed and reviewed.

Risk: Queued reports may be submitted to the network if participation is enabled and a flush is triggered.

Mitigation: Inspect queued reports before enabling network participation or flushing reports.

## Reference(s):

- [Fraud Filter homepage](https://fraud-filter.com)
- [Fraud Filter ClawHub release](https://clawhub.ai/mattpolly/skills/fraud-filter)
- [Technical architecture](TECHNICAL.md)
- [Signal format and score calculation](references/signal-format.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON trust assessments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May queue local JSONL failure reports; network report submission is opt-in.]

## Skill Version(s):

0.4.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
