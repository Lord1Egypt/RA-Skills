## Description: <br>
AI-powered Apple TV remote control with vision that navigates apps autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akivasolutions](https://clawhub.ai/user/akivasolutions) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use ClawTV to control an Apple TV from an agent or terminal, including launching apps, navigating menus, searching for content, playing media, taking screenshots, and using Claude vision for autonomous UI navigation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI mode sends Apple TV screenshots, user goals, and conversation context to Anthropic, and screenshots may include sensitive account, billing, or viewing information. <br>
Mitigation: Avoid AI mode on account or billing screens, use manual commands for privacy-sensitive workflows, and delete old screenshots from ~/.clawtv/screenshots/. <br>
Risk: Apple TV pairing credentials and optional Plex tokens are stored locally in ~/.clawtv/config.json. <br>
Mitigation: Restrict ~/.clawtv/config.json permissions to the local user and configure Plex only when the local credential-storage tradeoff is acceptable. <br>
Risk: The skill uses broad macOS automation and the security scan reports a real script-injection weakness. <br>
Mitigation: Use the skill only in trusted local environments and be cautious pairing with devices whose names you do not control. <br>
Risk: Autonomous vision mode can make repeated Anthropic API calls while navigating. <br>
Mitigation: Use a budget-limited Anthropic key, monitor API usage, and prefer direct manual or Plex commands when the needed action is known. <br>


## Reference(s): <br>
- [ClawTV ClawHub listing](https://clawhub.ai/akivasolutions/clawtv) <br>
- [ClawTV project homepage](https://github.com/akivasolutions/clawtv) <br>
- [Lookout tvOS companion project](https://github.com/akivasolutions/lookout-tvos) <br>
- [pyatv Apple TV control library](https://github.com/postlund/pyatv) <br>
- [python-plexapi Plex integration library](https://github.com/pkkid/python-plexapi) <br>
- [Plex authentication token guide](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/) <br>
- [Anthropic data retention information](https://support.anthropic.com/en/articles/7996885-how-long-do-you-store-personal-data) <br>
- [QuickTime Player documentation](https://support.apple.com/guide/quicktime-player/) <br>
- [Xcode documentation](https://developer.apple.com/xcode/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Apple TV remote-control actions, screenshot workflows, Plex control steps, and local configuration guidance for an agent.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
