## Description:

Query and track CareMax Health API indicators, including health metrics, lab results, trends, and quick logging for everyday vitals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kittenyang](https://clawhub.ai/user/kittenyang)

### License/Terms of Use:

MIT-0

## Use Case:

External CareMax users and their agents use this skill to browse health indicators, review lab and metric trends, identify abnormal values, and quick-log authenticated everyday vitals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write persistent health readings through quick-log actions.

Mitigation: Require confirmation of the metric, value, unit, date, and profile before executing any quick-log write.

Risk: The skill depends on unpinned external authentication scripts.

Mitigation: Install only from a trusted CareMax source and prefer a pinned, reviewed version of caremax-auth.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kittenyang/skills/caremax-indicators)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text responses with bash command examples and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires authenticated CareMax access through a sibling caremax-auth skill; quick-log writes should confirm metric, value, unit, date, and profile before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
