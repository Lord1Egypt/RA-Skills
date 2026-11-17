## Description:

Push images or markdown to a Bloomin8 e-ink photo frame via cloud API or local BLE and LAN workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xander887](https://clawhub.ai/user/xander887)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and device operators use this skill to prepare and deliver images or markdown content to Bloomin8 e-ink photo frames, either remotely through the cloud API or immediately through local BLE and LAN access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local uploads and upstream settings can send images or tokens over unauthenticated local HTTP.

Mitigation: Use the skill only on trusted local networks and with trusted Bloomin8 devices; confirm the target device and IP before uploads or upstream changes.

Risk: API tokens or upstream tokens can be exposed if passed directly on the command line or displayed in logs.

Mitigation: Prefer environment variables for cloud tokens, avoid echoing token values, and review any upstream-token command before execution.

Risk: BLE scans, IP probes, private image uploads, and persistent upstream reconfiguration can affect user privacy or device behavior.

Mitigation: Obtain explicit user consent before scanning, probing local hosts, uploading private images, or changing device upstream settings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xander887/skills/bloomin8)
- [Bloomin8 OpenClaw Skill Homepage](https://github.com/xander887/bloomin8-openclaw-skill)
- [Bloomin8 Open API Help](https://einkshot-349134901638.us-central1.run.app/open-api/help)
- [Bloomin8 Help Center](https://support.bloomin8.com/)
- [Bloomin8 Website](https://www.bloomin8.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON examples, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call local BLE/LAN workflows or cloud API endpoints when the user provides authorization and required credentials.]

## Skill Version(s):

2.2.5 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
