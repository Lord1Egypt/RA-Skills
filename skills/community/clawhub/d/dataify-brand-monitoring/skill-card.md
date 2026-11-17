## Description:

Monitors public brand mentions across news, search, reviews, forums, and public social sources to surface sentiment signals, material changes, and reputation risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users, brand teams, and operators use this skill to collect dated public brand-monitoring snapshots with mention counts, channel mix, sentiment signals, reputation risks, evidence gaps, and recommended response items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Dataify API token, and task status or download requests may place that token in URL query strings.

Mitigation: Use a narrowly scoped or disposable token, monitor account credit usage, avoid pasting tokens into chat, and review logs or command output for token leakage.

Risk: Packaged dependency workflows include broader and inconsistent instructions beyond the brand-monitoring workflow.

Mitigation: Review the bundled dependencies before installation and remove or tighten unrelated workflow material before treating the package as narrowly scoped.

Risk: Automated public-web sentiment and reputation signals can be incomplete, stale, or misleading.

Mitigation: Require human review of evidence, sentiment labels, and recommended responses before commercial or reputation decisions.

## Reference(s):

- [Dataify Brand Monitoring on ClawHub](https://clawhub.ai/dataify-server/skills/dataify-brand-monitoring)
- [Dataify account setup](https://dashboard.dataify.com/login?utm_source=skill)
- [Token setup reference](_dependencies/skills/dataify-task-operations/references/token-setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown summaries with JSON reports and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write dated run directories with state, raw collection outputs, report.json, and report.md; API token values must not be printed.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
