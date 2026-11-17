## Description:

Control Brix digital signage screens from an agent — list screens and check which are offline, put an image, video or playlist on screens for a set time, import media from a URL, set what a screen plays, reboot or refresh a screen, fire an emergency message, and pull proof-of-play reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benloveitt](https://clawhub.ai/user/benloveitt)

### License/Terms of Use:

MIT-0

## Use Case:

Signage operators and developers use this skill to monitor Brix screens, manage displayed content, run device commands, trigger emergency messages, and review proof-of-play reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Casts, assignments, emergencies, and device commands can affect live screens.

Mitigation: Confirm the intended action and affected screens with the user before changing them.

Risk: An API key with broad permissions can affect more screens than intended.

Mitigation: Create a key with only the needed permissions and location scope.

## Reference(s):

- [Brix Digital Signage on ClawHub](https://clawhub.ai/benloveitt/skills/brix-signage)
- [Brix developer documentation](https://brixsignage.com/developers/)
- [Brix API specification](https://api.brixsignage.com/v1/openapi.json)
- [Brix MCP setup](https://brixsignage.com/developers/mcp/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Brix API key and curl to operate the account.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
