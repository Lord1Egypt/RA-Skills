## Description:

Analyze reviews or public customer feedback across multiple sources and produce themes, sentiment signals, and product actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn public customer reviews and feedback into traceable themes, sentiment signals, source-bias notes, and prioritized product actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dataify API tokens may be exposed through task polling or download URLs.

Mitigation: Use a limited or easily rotated token, monitor credit usage, and rotate the token if exposure is suspected.

Risk: Public URLs and collected review data are sent to Dataify.

Mitigation: Use only public, non-sensitive URLs and review the collected data before relying on it for product or reputation decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-review-intelligence)
- [Dataify token setup](artifact/_dependencies/skills/dataify-task-operations/references/token-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries and JSON reports with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write state, raw evidence, report.json, and report.md files in a run directory; preserves task IDs for safe resume.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
