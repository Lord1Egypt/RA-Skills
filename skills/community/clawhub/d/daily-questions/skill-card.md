## Description:

Daily Questions helps an agent run a daily Telegram questionnaire that asks about the user and preferred agent behavior, then updates USER.md and SOUL.md with the answers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daijo-bu](https://clawhub.ai/user/daijo-bu)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to schedule a lightweight daily routine that asks preference questions over Telegram and keeps USER.md and SOUL.md current. It supports personalization by turning answers into organized memory and behavior guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The routine can collect personal preferences and store them in USER.md and SOUL.md for future agent behavior.

Mitigation: Avoid sharing sensitive information, and periodically review, edit, or delete USER.md and SOUL.md when preferences change.

Risk: Questions and answers are exchanged over Telegram, which creates privacy considerations for the user's chosen channel.

Mitigation: Use the routine only when comfortable with Telegram for these questions, and keep answers limited to information appropriate for that channel.

## Reference(s):

- [Example Question Categories](references/example-questions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text, Telegram message payloads, cron setup guidance, and updates to USER.md and SOUL.md]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Questions are sent one at a time with Telegram inline buttons and unique callback IDs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
