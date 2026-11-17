## Description:

AI-powered Apple TV remote control with vision that navigates apps autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akivasolutions](https://clawhub.ai/user/akivasolutions)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use ClawTV to control an Apple TV from natural-language goals, direct remote commands, screenshots, and optional Plex actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls Apple TV playback, navigation, and optional Plex clients.

Mitigation: Use it only on trusted local devices and review actions before enabling autonomous AI mode.

Risk: AI mode sends Apple TV screenshots and user instructions to Anthropic and may expose sensitive on-screen content.

Mitigation: Avoid sensitive screens in AI mode, prefer manual commands for private workflows, and regularly delete local screenshot history.

Risk: Apple TV pairing credentials and optional Plex tokens are stored in ~/.clawtv/config.json.

Mitigation: Restrict file permissions on ~/.clawtv, protect the host account, and treat Plex tokens as high-value credentials.

Risk: Autonomous vision loops can incur API costs and may spend multiple steps when navigation is unclear.

Mitigation: Use a budget-limited Anthropic API key, monitor usage, and prefer direct commands or Plex direct control when possible.

Risk: The authoritative security summary reports an AppleScript injection risk.

Mitigation: Review local command inputs and host trust boundaries before deployment, especially where user-controlled values can reach AppleScript automation.

## Reference(s):

- [ClawTV ClawHub listing](https://clawhub.ai/akivasolutions/skills/clawtv)
- [ClawTV homepage](https://github.com/akivasolutions/clawtv)
- [Lookout tvOS companion app](https://github.com/akivasolutions/lookout-tvos)
- [pyatv](https://github.com/postlund/pyatv)
- [python-plexapi](https://github.com/pkkid/python-plexapi)
- [Plex token documentation](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)
- [Anthropic data retention documentation](https://support.anthropic.com/en/articles/7996885-how-long-do-you-store-personal-data)
- [QuickTime Player documentation](https://support.apple.com/guide/quicktime-player/)
- [Xcode](https://developer.apple.com/xcode/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide local device-control workflows that use screenshots, Apple TV remote commands, and optional Plex commands.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
