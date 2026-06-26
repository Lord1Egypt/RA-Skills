## Description: <br>
Update OpenClaw safely on macOS (brew cask install) with automatic snapshot of the npm package + .app bundle, post-update health check, and automatic rollback to the previous version if the gateway doesn't come back. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[klouddy-cloud](https://clawhub.ai/user/klouddy-cloud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to update an OpenClaw macOS installation while preserving a rollback path if the gateway fails to return. It is intended for brew cask installations with Telegram configured for status notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad OpenClaw maintenance authority, including update, restart, deletion, replacement, rollback, and detached background execution. <br>
Mitigation: Install only from a trusted publisher, require explicit approval before launch, and confirm the OpenClaw binary, app bundle, npm package, LaunchAgent, and snapshot paths before running. <br>
Risk: The update script reads Telegram bot credentials and chat targets from the OpenClaw configuration to send progress notifications. <br>
Mitigation: Use only if Telegram credential exposure is acceptable, keep the configuration file permission-restricted, and prefer a bot token scoped to this notification workflow. <br>
Risk: Rollback and rescue paths can remove or replace OpenClaw application files if the gateway fails to recover. <br>
Mitigation: Verify the snapshot exists before destructive restore steps, review logs after failure, and require user approval before manual rescue or brew reinstall actions. <br>


## Reference(s): <br>
- [Rescue prompt for Claude Code](references/rescue-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Launches a detached update script and returns short user-facing status guidance; progress is reported through Telegram.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
