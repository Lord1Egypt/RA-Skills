## Description:

Tracks local connection records across people, tools, resources, and Memory events, then generates tracker dashboards and daily or weekly summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[largetool](https://clawhub.ai/user/largetool)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to log interaction, research, tool, and Memory connections locally, score their value, and review daily or weekly activity summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local tracking may collect interaction, research activity, and selected Memory event metadata.

Mitigation: Install only when local tracking is intended, configure automatic triggers narrowly, and periodically review or delete generated files under ~/.openclaw/workspace/connections.

Risk: Untrusted or sensitive record text could be written into local Markdown reports.

Mitigation: Avoid passing untrusted text, API keys, private conversations, or other sensitive data into connection record fields.

## Reference(s):

- [Connection Tracker ClawHub release](https://clawhub.ai/largetool/skills/connection-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown tracker and report files, JSON CLI summaries, and command-line usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local tracker, daily report, and weekly report files under ~/.openclaw/workspace/connections.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
