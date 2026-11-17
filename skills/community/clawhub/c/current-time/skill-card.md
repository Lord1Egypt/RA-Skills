## Description:

Current Time returns formatted date, time, and timezone information from the local system clock.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changsheng0804](https://clawhub.ai/user/changsheng0804)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Chinese-language current time and date prompts, producing formatted local date, time, and timezone text for scheduling, logging, or quick checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is written for Chinese prompts and output, which may not match every workflow.

Mitigation: Install it when Chinese-language time responses are acceptable, or review and adapt the output format before deployment.

Risk: Time and timezone output depends on the local system date command and host timezone settings.

Mitigation: Confirm the host timezone convention and output format before relying on the result for scheduling or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/changsheng0804/skills/current-time)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with optional Markdown bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local date command; output follows the system clock and timezone unless the agent adapts the format.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
