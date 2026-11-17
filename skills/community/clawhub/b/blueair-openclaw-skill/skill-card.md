## Description:

Use when managing Blueair air purifiers, checking indoor air quality, or responding to respiratory discomfort complaints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[you96](https://clawhub.ai/user/you96)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an agent check Blueair purifier status, interpret indoor air quality readings, and propose or apply purifier controls such as fan speed, auto mode, child lock, and standby.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Blueair account passwords and can control purifier settings.

Mitigation: Install only if comfortable granting Blueair account access; use a dedicated low-privilege Blueair account where possible.

Risk: Local credential storage in ~/.blueair/config.json can expose account access if file permissions are loose.

Mitigation: Avoid password reuse and protect ~/.blueair/config.json with strict local permissions.

Risk: Device-control behavior may change purifier settings in ways the user did not intend.

Mitigation: Review or patch the login and set_state code before relying on the skill, and confirm control actions before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/you96/skills/blueair-openclaw-skill)
- [README](README.md)
- [Basic Usage Examples](examples/basic-usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style guidance with inline shell commands and summarized device status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use local Node.js scripts that return JSON device data before the agent summarizes it for the user.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
