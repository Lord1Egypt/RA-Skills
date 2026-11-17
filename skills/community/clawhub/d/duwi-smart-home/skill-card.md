## Description:

Duwi Smart Home helps agents use the Duwi Open Platform API to query home structure and device status, control smart-home devices, and execute scenes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duwi2024](https://clawhub.ai/user/duwi2024)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to map smart-home requests into Duwi CLI commands for account setup, home and room lookup, device status checks, device control, scene execution, and cache management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate commands that directly control physical smart-home devices and scenes.

Mitigation: Confirm the target house, room, device, scene, and action with the user before running control commands.

Risk: Credential, token, and cache files may contain sensitive household access data.

Mitigation: Use interactive hidden credential entry where possible, avoid placing secrets in shell history, and treat local config, token, and cache files as sensitive.

Risk: The security review flagged unsafe credential-entry patterns and limited user-control safeguards.

Mitigation: Install only when the Duwi publisher account and machine context are trusted, and review commands before execution.

## Reference(s):

- [Duwi Smart Home on ClawHub](https://clawhub.ai/duwi2024/skills/duwi-smart-home)
- [Duwi Open Platform API](https://openapi.duwi.com.cn/homeApi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI argument guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that operate physical smart-home devices and local credential, token, and cache files.]

## Skill Version(s):

1.0.6 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
