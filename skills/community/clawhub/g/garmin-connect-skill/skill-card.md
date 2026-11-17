## Description:

Garmin Connect integration for OpenClaw: sync fitness data (steps, HR, calories, workouts, sleep) using OAuth. Supports China (garmin.cn) and Global (garmin.com) regions. Data is stored in SQLite database for fast access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tcyxk](https://clawhub.ai/user/tcyxk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw developers use this skill to authenticate with Garmin Connect, synchronize health and workout data into a local SQLite database, and generate status summaries or health reports from that data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Garmin account credentials and personal health records.

Mitigation: Use a disposable or rotated Garmin password for testing, avoid passing real passwords on the command line, and restrict permissions on ~/.garth and ~/.clawdbot.

Risk: The artifact includes Feishu messaging defaults that security evidence identifies for removal.

Mitigation: Remove embedded Feishu defaults and configure any messaging integration with user-controlled secrets before use.

Risk: Background timers or daemons can run synchronization repeatedly and access health data after installation.

Mitigation: Do not enable the timer or daemon until the operator understands what will run, where it stores data, and how to disable it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tcyxk/skills/garmin-connect-skill)
- [Publisher profile](https://clawhub.ai/user/tcyxk)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts may produce text, JSON-like summaries, SQLite records, and outbound health-report messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on local Garmin credentials, Garmin region selection, local SQLite state, and optional Feishu/OpenClaw messaging configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
