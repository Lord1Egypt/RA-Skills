## Description:

A friendly AI English teacher that runs daily lessons via Telegram voice messages, teaching grammar, vocabulary, and conversation with a casual buddy style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiku54](https://clawhub.ai/user/haiku54)

### License/Terms of Use:


## Use Case:

External learners and OpenClaw users use this skill to run a proactive Telegram-based English tutor that conducts onboarding, voice-first lessons, conversation practice, corrections, spaced repetition, and weekly progress reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and runtime behavior make persistent workspace-level changes, including updates to OpenClaw configuration and learner tracking files.

Mitigation: Install in a dedicated OpenClaw workspace and back up openclaw.json, SOUL.md, and HEARTBEAT.md before setup.

Risk: Telegram bot credentials and student identifiers may be stored with insufficient safeguards.

Mitigation: Use a dedicated Telegram bot, protect or rotate the bot token, restrict allowed users, and verify local file permissions.

Risk: The skill sends frequent proactive messages and maintains persistent learner tracking.

Mitigation: Enable the skill only with the student's informed consent and adjust or disable cron jobs if the message frequency is inappropriate.

## Reference(s):

- [English Bestie ClawHub page](https://clawhub.ai/haiku54/skills/english-bestie)
- [OpenClaw](https://openclaw.dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Telegram voice-message text, text correction cards, Markdown reports, JSON tracking updates, and OpenClaw cron commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OpenAI API key, a dedicated Telegram bot, and persistent local tracking files for learner state.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
