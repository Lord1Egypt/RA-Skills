## Description:

Runs local ClawUsage monitoring commands from Telegram or Feishu chat to check Codex usage, manage automatic idle alerts, set thresholds, and switch language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fantasyengineercdream](https://clawhub.ai/user/fantasyengineercdream)

### License/Terms of Use:


## Use Case:

Developers and external OpenClaw users on Windows use this skill from chat to inspect Codex usage, configure idle reminders, and return the local command output directly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads OpenClaw authentication and session files and uses a local token to query ChatGPT usage.

Mitigation: Install only in a trusted Windows profile, review the behavior before use, and avoid enabling it where local OpenClaw credentials should remain inaccessible to skills.

Risk: Automatic idle alerts install a hidden recurring Windows scheduled task.

Mitigation: Enable auto alerts only deliberately, review the scheduled task named ClawUsageAuto, and run /clawusage auto off to remove it when no longer needed.

Risk: Usage and session snapshots are cached under the user's profile.

Mitigation: Treat the .clawusage state directory as sensitive local data and delete it when clearing local usage history.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fantasyengineercdream/skills/clawusage-windows-hardlock)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns stdout directly without model post-formatting.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
