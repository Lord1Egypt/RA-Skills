## Description:

Matches a user-described task to two or three suitable local agency roles, asks the user to choose, then loads the selected role profile before producing the task output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wzdongyifan-bit](https://clawhub.ai/user/wzdongyifan-bit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to choose an appropriate specialist role for a requested task before the agent begins work. It is especially oriented toward marketing, ecommerce, advertising, content, growth, and product tasks backed by local role profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected local SOUL.md role files can change the agent's behavior if they are unsafe, modified, or from an untrusted source.

Mitigation: Review local role files before use and only keep role definitions that are trusted, scoped to style and expertise, and appropriate for the task.

Risk: The workflow depends on local role profiles under ~/.openclaw/agency-agents/, so missing or stale profiles can lead to poor or unavailable recommendations.

Mitigation: Confirm the local role directory exists and contains current role profiles before relying on the skill for role matching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wzdongyifan-bit/skills/agency-role-match)
- [Publisher profile](https://clawhub.ai/user/wzdongyifan-bit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown text with role recommendations, reasons, selection options, and selected-role task output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local role profiles under ~/.openclaw/agency-agents/ to complete the selected-role workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
