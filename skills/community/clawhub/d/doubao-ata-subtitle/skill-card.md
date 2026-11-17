## Description:

Generate subtitles with automatic time alignment using the Volcengine ATA API for audio and transcript inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackeight4752](https://clawhub.ai/user/blackeight4752)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, media producers, and agent operators use this skill to create time-aligned subtitle files from WAV audio and a plain-text transcript. It is intended for workflows that need SRT or ASS output and can use Volcengine ATA credentials for real alignment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio, transcript text, and the API token may be sent to a configured external endpoint.

Mitigation: Use the documented HTTPS Volcengine endpoint, avoid custom endpoints unless fully trusted, and review the skill before processing recordings.

Risk: Credential files may expose Volcengine application secrets if stored with broad permissions.

Mitigation: Protect ~/.volcengine_ata.conf with restrictive permissions and prefer short-lived or narrowly scoped API tokens.

Risk: Sensitive recordings may be exposed before endpoint validation and upload disclosure gaps are addressed.

Mitigation: Do not process sensitive recordings until those gaps have been reviewed and accepted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/blackeight4752/skills/doubao-ata-subtitle)
- [Volcengine ATA Documentation](https://www.volcengine.com/docs/6561/163043?lang=zh)
- [Volcengine Speech App Console](https://console.volcengine.com/speech/app)
- [OpenClaw Documentation](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated SRT or ASS subtitle files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WAV 16 kHz mono PCM audio and one-sentence-per-line UTF-8 text input; uses mock output when API credentials are absent.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
