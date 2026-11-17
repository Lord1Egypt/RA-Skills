## Description:

Helps users practice spoken English through voice or text conversations with feedback, plus optional scheduled daily phrase pushes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zsy000](https://clawhub.ai/user/zsy000)

### License/Terms of Use:

MIT-0

## Use Case:

External English learners use this skill to practice everyday spoken English, receive pronunciation and expression feedback, and optionally get daily phrase reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security verdict is suspicious because scheduled messaging and external AI scripts handle secrets and configuration unsafely enough to require review before installation.

Mitigation: Review the scripts before installing, keep config.json private, and use a narrowly scoped API key.

Risk: Push delivery can send generated content to a configured recipient through a configured channel.

Mitigation: Verify the API endpoint, message channel, and target recipient before enabling push delivery.

Risk: The security guidance warns against enabling cron until the monthly shell script is fixed or removed.

Mitigation: Leave cron-based monthly summary execution disabled unless the shell script has been reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zsy000/skills/english-speaking-practice)
- [Publisher profile](https://clawhub.ai/user/zsy000)
- [README](artifact/README.md)
- [Configuration guide](artifact/CONFIG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Conversational text or Markdown with optional shell commands and JSON practice records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use TTS, Whisper, message delivery, local JSON storage, and optional scheduled pushes when configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
