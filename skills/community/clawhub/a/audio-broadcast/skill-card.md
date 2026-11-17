## Description:

Controls Xiaoboshu broadcast systems for audio playback, announcements, volume control, scheduled broadcast tasks, device status checks, and text-to-speech broadcasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oxiaom](https://clawhub.ai/user/oxiaom)

### License/Terms of Use:

MIT-0

## Use Case:

External users, operators, and developers use this skill to control Xiaoboshu broadcast devices, play local or URL audio, manage scheduled announcements, adjust volume, inspect devices and files, and generate Chinese TTS broadcasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes a concrete admin token in local configuration.

Mitigation: Do not use the bundled token; revoke or replace it, delete config.json, and authenticate only against a trusted Xiaoboshu server.

Risk: Credentials and control requests may be handled over cleartext HTTP or stored in plaintext files.

Mitigation: Use the skill only with HTTPS, a secure tunnel, or a trusted local network, and restrict access to the configuration file.

Risk: Text-to-speech content may be sent to an external provider or uploaded to the broadcast server.

Mitigation: Avoid sensitive announcement text unless the external TTS path and server handling are acceptable for the deployment.

Risk: Scheduled cleanup can automatically delete server-side TTS files.

Mitigation: Enable cleanup only after confirming that its file-name rules and task-reference checks match the operating environment.

## Reference(s):

- [Xiaoboshu API Reference](artifact/references/api.md)
- [Xiaoboshu Postman API Collection](artifact/references/postman2.1.json)
- [Audio Broadcast on ClawHub](https://clawhub.ai/oxiaom/skills/audio-broadcast)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct an agent to run bundled Python scripts that call the Xiaoboshu HTTP API and update local configuration.]

## Skill Version(s):

1.1.4 (source: frontmatter and server release, released 2026-03-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
