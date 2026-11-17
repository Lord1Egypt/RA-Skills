## Description:

Automatically write daily/weekly/monthly diary summaries and extract insights to auto-learn.md for HexaLoop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to schedule daily, weekly, and monthly diary summaries, capture actionable insights in auto-learn.md, and optionally send Feishu interactive cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private workspace memory, current state, farm status, diary summaries, decisions, and next steps may be retained locally and posted to a fixed Feishu chat.

Mitigation: Install only when you control the Feishu chat, make the recipient user-configurable, and add preview/redaction before enabling delivery.

Risk: Scheduled cron runs can repeatedly generate and send diary summaries without an interactive review step.

Mitigation: Review cron jobs before enabling recurring runs and keep delivery disabled until scheduled behavior is confirmed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/0xcjl/skills/auto-diary-0xcjl)
- [Diary template](artifact/templates/diary_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Markdown diary and review files, auto-learn.md insight entries, Feishu interactive-card JSON, and OpenClaw cron commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes diary and insight files under the user's OpenClaw workspace and can post summaries to a Feishu chat when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
