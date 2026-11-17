## Description:

Collects public Bilibili ranking data across 21 charts, analyzes trends, detects anomalies, and stores JSON data and Markdown reports locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rookiecoder-jsjs](https://clawhub.ai/user/rookiecoder-jsjs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect public Bilibili ranking data, track creator and topic trends, detect anomalies, and generate Chinese Markdown analysis reports for selected rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic analysis can pass public ranking content and creator fields to a spawned sub-agent.

Mitigation: Use manual mode or a tool-restricted analysis agent when sub-agent file, tool, or credential access should be constrained.

Risk: The skill persists ranking data, trend history, alert records, reports, and creator fields locally.

Mitigation: Set BILIBILI_WORKSPACE to a contained directory and review retained files before sharing or deploying the workspace.

Risk: Daemon or frequent collection can create repeated outbound requests and grow local history over time.

Mitigation: Use rank filters and reasonable collection intervals, and stop daemon mode when continuous monitoring is not needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rookiecoder-jsjs/skills/bilibili-trending)
- [Bilibili all-rank workflow](references/workflow.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON data files, command-line text, and reusable analysis prompts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local ranking data, trend history, alert records, creator fields, and reports under the configured BILIBILI_WORKSPACE.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
