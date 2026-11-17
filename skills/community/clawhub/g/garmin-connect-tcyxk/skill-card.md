## Description:

Garmin Connect integration for OpenClaw: sync fitness data (steps, HR, calories, workouts, sleep) using OAuth. Supports China (garmin.cn) and Global (garmin.com) regions. Data is stored in SQLite database for fast access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcyxk](https://clawhub.ai/user/tcyxk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to authenticate with Garmin Connect, synchronize fitness, sleep, workout, and health metrics into local SQLite storage, and query or summarize that data through OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Garmin credentials may be exposed through command-line password entry or weak local persistence.

Mitigation: Use interactive secret input or an OS credential store instead of command-line passwords, rotate credentials after setup, and restrict ~/.garth permissions to the current user.

Risk: Private health data is stored locally in SQLite and cache files.

Mitigation: Run on a trusted single-user machine, restrict ~/.clawdbot permissions, and review retention or deletion expectations before enabling regular sync.

Risk: Feishu app secrets, webhook URLs, or report destinations can leak health summaries to unintended recipients.

Mitigation: Rotate any shared or default Feishu secret, verify recipients and webhook URLs, and use least-privilege app permissions before enabling reports.

Risk: Scheduled sync setup may encourage unnecessary elevated privileges.

Mitigation: Run synchronization as the normal user where possible and review systemd timers or services before enabling automatic execution.

## Reference(s):

- [Garmin Connect ClawHub skill page](https://clawhub.ai/tcyxk/skills/garmin-connect-tcyxk)
- [tcyxk ClawHub publisher profile](https://clawhub.ai/user/tcyxk)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local SQLite health data and trigger Garmin synchronization scripts when configured.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
