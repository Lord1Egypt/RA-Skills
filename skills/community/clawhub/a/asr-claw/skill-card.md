## Description:

Speech recognition CLI for AI agent automation. Transcribe audio from stdin, files, or URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dionren](https://clawhub.ai/user/dionren)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Asr Claw to transcribe audio from files, URLs, stdin, or live streams into text, JSON, and subtitle formats using local or cloud ASR engines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud ASR engines can send audio to third-party services.

Mitigation: Use local engines for private or regulated recordings, and use cloud engines only when the provider's policies are acceptable for the audio.

Risk: Installation downloads an external executable from a GitHub release.

Mitigation: Confirm the release source is trusted and verify the provided checksum before installing or running the executable.

Risk: The default language setting is Chinese, which may be unexpected for some recordings.

Mitigation: Review and change the default language setting before use when another language is expected.

## Reference(s):

- [Asr Claw ClawHub Skill Page](https://clawhub.ai/dionren/skills/asr-claw)
- [asr-claw Homepage](https://github.com/llm-net/asr-claw)
- [asr-claw Release Checksums](https://github.com/llm-net/asr-claw/releases/latest/download/checksums.txt)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration]

**Output Format:** [JSON envelope, plain text, SRT/VTT subtitle files, and Markdown command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports file, stdin, URL, and streaming audio inputs; transcription output can include segment timing.]

## Skill Version(s):

1.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
