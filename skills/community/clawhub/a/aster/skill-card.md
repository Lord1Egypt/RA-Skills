## Description:

Your AI CoPilot on Mobile - or give your AI its own phone. Make calls, send SMS, speak via TTS on speakerphone, automate UI, manage files, search media, and 40+ more tools via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[satyajiit](https://clawhub.ai/user/satyajiit)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to connect an AI agent to an Android device through MCP for phone control, messaging, screen interaction, media search, file access, and event-driven mobile workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control Android phone features and may access calls, SMS, notifications, location, files, clipboard, media, and screen contents.

Mitigation: Install only after review, grant only the permissions needed for the intended workflow, and prefer a spare Android device with minimal personal data.

Risk: The setup depends on external mutable software, including an npm package and Android APK.

Mitigation: Pin and verify package and APK versions before deployment.

Risk: Callback forwarding can transmit sensitive SMS and notification content to configured endpoints.

Mitigation: Enable callbacks only to HTTPS endpoints you control and limit forwarded workflows to data you are prepared to expose to the receiving agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/satyajiit/skills/aster)
- [Aster website](https://aster.theappstack.in)
- [Aster project repository](https://github.com/satyajiit/aster-mcp)
- [Aster releases](https://github.com/satyajiit/aster-mcp/releases)
- [Tailscale](https://tailscale.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, Code]

**Output Format:** [Markdown with command examples, JSON configuration, and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces instructions and tool-use guidance for Android device control through an HTTP MCP server.]

## Skill Version(s):

0.1.14 (source: evidence.json release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
