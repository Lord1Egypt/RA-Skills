## Description:

Generate speech from text with Fish Audio S1 and optionally upload MP3 audio files to NextCloud over WebDAV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gtank1](https://clawhub.ai/user/gtank1)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to generate spoken audio from text, select voices and emotion tags, and manage optional upload of generated MP3 files to NextCloud.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an exposed NextCloud password in defaults and examples.

Mitigation: Rotate the exposed credential, remove hard-coded secret defaults, and require users to provide credentials through their own environment variables.

Risk: The security review reports use of unencrypted HTTP for TTS requests and NextCloud Basic authentication.

Mitigation: Use HTTPS endpoints for TTS and NextCloud, and avoid sending sensitive text, audio, or credentials unless the services and network path are trusted.

Risk: The security review advises review before installing or running the skill as-is.

Mitigation: Review and test temporary-file handling, upload commands, and service configuration before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gtank1/skills/fish-tts)
- [Publisher profile](https://clawhub.ai/user/gtank1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate local MP3 files and provide upload commands or paths when connected services are configured.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
