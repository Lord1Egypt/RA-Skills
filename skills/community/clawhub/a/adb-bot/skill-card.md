## Description:

ADB Bot enables OpenClaw agents to control authorized local Android devices through an ADB Bot MCP server for screenshots, UI recognition, taps, swipes, text input, app launch, and multi-device actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hilbp](https://clawhub.ai/user/hilbp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let OpenClaw operate Android devices they own or are authorized to control, including screen inspection, app launch, text entry, navigation, and multi-device automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can control Android devices and may affect sensitive apps or data if used without clear authorization.

Mitigation: Use it only with Android devices you own or are authorized to control, and explicitly approve actions before using it in sensitive apps.

Risk: The release directs users to external ADB Bot installation paths that the security evidence flags as unverified.

Mitigation: Verify downloads independently and prefer pinned, checksum-verified releases over latest-tag or generic installer links.

Risk: The artifact under-discloses device-control risk relative to the breadth of available actions.

Mitigation: Review the skill carefully before installing, keep ADB Bot local, and stop or disconnect device automation when actions do not match user intent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hilbp/skills/adb-bot)
- [ADB Bot website](https://adb-bot.hilbp.com/?utm_source=clawhub&utm_medium=readme)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and MCP tool guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to use local ADB Bot MCP tools for Android device actions after user authorization and setup.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
