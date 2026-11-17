## Description:

Don't Be Scary helps agents update OpenClaw on macOS by launching a detached updater that snapshots the npm package and app bundle, runs the update, checks the gateway, sends Telegram status, and rolls back if health checks fail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klouddy-cloud](https://clawhub.ai/user/klouddy-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they want an agent to update a macOS OpenClaw installation while preserving a rollback path if the gateway does not recover. It is intended for OpenClaw installations managed through Homebrew cask with Telegram notifications configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The updater can modify and delete OpenClaw installation paths, restart LaunchAgents, and run detached in the background.

Mitigation: Install only when the publisher is trusted, review configured paths and environment overrides before execution, and keep the rollback snapshot location available.

Risk: The script reads Telegram bot credentials from the OpenClaw configuration and sends update status to Telegram.

Mitigation: Verify the configured bot and chat target before use, prefer a dedicated notification bot, and rotate credentials if the configuration is exposed.

Risk: Unsafe or untrusted environment overrides could redirect snapshot, deletion, restore, or launchctl behavior.

Mitigation: Use the default paths for standard Homebrew cask installations unless the operator has reviewed and approved each override.

## Reference(s):

- [Rescue prompt for Claude Code](references/rescue-prompt.md)
- [ClawHub skill page](https://clawhub.ai/klouddy-cloud/skills/dont-be-scary)

## Skill Output:

**Output Type(s):** [shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Launches a detached updater and reports progress through Telegram and local log files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
