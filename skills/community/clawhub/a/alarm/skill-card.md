## Description:

Analyzes Feishu/Lark text or voice messages for reminder intent, parses Chinese deadline expressions, stores one-time reminders in SQLite, and sends confirmation and due reminder messages through Feishu after optional SenseAudio ASR transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hei-maom](https://clawhub.ai/user/hei-maom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers integrating Feishu or Lark bots use this skill to detect reminder requests in Chinese text or voice messages, create reminders, and send a single confirmation and due reminder back to the original chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials, voice files, and message content can be sent to configurable Feishu and SenseAudio API hosts.

Mitigation: Pin Feishu and SenseAudio base URLs to trusted HTTPS endpoints and restrict who can change runtime configuration.

Risk: Reminder content, sender identifiers, message identifiers, and audio-derived transcript data may be stored in the local SQLite database.

Mitigation: Protect the process environment and database file, and define retention and deletion rules for stored reminder data.

Risk: Unrestricted reminder creation or use of --no-confirm could create reminders without the expected user-facing confirmation.

Mitigation: Restrict who can invoke reminder creation and --no-confirm in production workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hei-maom/skills/alarm)
- [Feishu integration guide](references/integration_cn.md)
- [Chinese time parsing rules](references/time_rules_cn.md)
- [Feishu Open Platform](https://open.feishu.cn)
- [SenseAudio API endpoint](https://api.senseaudio.cn)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [JSON command output plus plain-text Feishu confirmation and reminder messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist reminder records in a local SQLite database and send Feishu messages when create or polling commands are invoked.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
