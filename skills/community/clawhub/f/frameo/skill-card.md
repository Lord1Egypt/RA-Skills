## Description:

Control Frameo digital photo frames via cloud API for frame and account information or ADB for photo upload, brightness, screen, and navigation control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[850media](https://clawhub.ai/user/850media)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to list paired Frameo frames, inspect account data, and control frames they own through Frameo cloud API calls or ADB commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Frameo account tokens and may cache them in ~/.frameo_token.

Mitigation: Treat tokens as secrets, use restrictive file permissions or a credential store, and avoid sharing logs that may contain account or token data.

Risk: Wireless ADB can provide broad control of a Frameo device on the network.

Mitigation: Use the skill only with frames, accounts, and networks you control, and disable wireless ADB when finished.

Risk: ADB delete and wildcard commands can remove unintended photos or files.

Mitigation: Review rm and wildcard commands carefully before running them and confirm the target frame path is correct.

## Reference(s):

- [Frameo Cloud API Endpoints](references/api-endpoints.md)
- [Frameo ADB Commands Reference](references/adb-commands.md)
- [Frameo API](https://api.frameo.net)
- [Frameo Auth Endpoint](https://auth.frameo.net/auth/realms/frameo/protocol/openid-connect/token)
- [ClawHub Skill Page](https://clawhub.ai/850media/skills/frameo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, Python command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that read Frameo account data, cache access tokens, upload or delete photos, and control a frame over ADB.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
