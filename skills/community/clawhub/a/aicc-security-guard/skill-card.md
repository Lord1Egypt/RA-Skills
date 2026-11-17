## Description:

Ensure the AICC native plugin is active before handling confidential data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[senmud](https://clawhub.ai/user/senmud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agents use this skill to confirm the AICC native plugin is installed and enabled before handling confidential or sensitive data. If plugin status cannot be confirmed, the skill directs the agent to stop and provide installation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required native plugin is unverified and may receive or affect confidential data handling.

Mitigation: Install it only after verifying the plugin publisher, version, permissions, and update path.

Risk: Plugin status may be unavailable or self-reported rather than independently confirmed.

Mitigation: Use openclaw plugins list when possible and treat uncertain status as missing before handling sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/senmud/skills/aicc-security-guard)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs the agent to stop before confidential data handling unless plugin status is confirmed.]

## Skill Version(s):

0.1.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
