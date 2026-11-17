## Description:

Tracks blood pressure readings, analyzes trends, provides health suggestions, sends abnormal-value alerts, and generates statistics reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to record blood pressure readings, review trends over time, receive health suggestions, and configure abnormal-value alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a health-data workflow and may produce health suggestions or abnormal-value alerts that users could over-rely on.

Mitigation: Review outputs before use and treat suggestions as tracking support rather than professional medical advice.

Risk: The artifact metadata requires curl even though the evidence reports no disclosed network feature.

Mitigation: Review the skill before installing and confirm whether network tooling is actually needed.

Risk: The documented installation command uses a mutable remote installer path.

Mitigation: Prefer a pinned ClawHub installer version before installing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaising-openclaw1/skills/blood-pressure-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and health-tracking guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include blood pressure trend summaries, abnormal-value alerts, statistics, and health suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
