## Description:

Query CNKI by journal name or research topic, and create journal or topic subscriptions that periodically push new CNKI paper metadata into the main OpenClaw chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjli-new](https://clawhub.ai/user/yjli-new)

### License/Terms of Use:


## Use Case:

Developers, researchers, and OpenClaw users use this skill to query CNKI paper metadata by journal or topic and to create recurring CNKI watches that surface new matching paper metadata in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses CNKI session credentials and may handle persistent login state.

Mitigation: Use only approved CNKI credentials, provide secrets through the configured environment, and rotate or revoke credentials after use.

Risk: Recurring OpenClaw cron jobs can inject CNKI metadata into the main chat.

Mitigation: Review created subscriptions, keep schedules limited to expected topics or journals, and remove stale jobs when monitoring is no longer needed.

Risk: The security evidence flags automated verification bypass, disabled TLS validation, gateway-token handling, and unpinned npx guidance.

Mitigation: Review and remediate these behaviors before using the skill with real credentials, persistent sessions, or production workflows.

## Reference(s):

- [CNKI Watch Skill Page](https://clawhub.ai/yjli-new/skills/cnki-watch)
- [Command Contract](references/commands.md)
- [Runtime Config](references/config.md)
- [Schedule Format](references/schedule.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell commands and JSON result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns CNKI paper metadata only; recurring subscription runs may inject new paper metadata into the main OpenClaw chat.]

## Skill Version(s):

0.2.1 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
