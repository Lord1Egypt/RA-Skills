## Description:

Authorizes Douyin accounts, prepares local video metadata and transcripts, drafts captions, and publishes videos through the Douyin OpenAPI with fallback outbox export when publish permissions are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yjli-new](https://clawhub.ai/user/yjli-new)

### License/Terms of Use:


## Use Case:

Developers and automation teams use this skill to authorize Douyin accounts, transcribe local video audio, draft captions, and publish or package videos for manual publishing when API permissions are missing.

### Deployment Geography for Use:

China mainland

## Known Risks and Mitigations:

Risk: Private video audio may be sent to an external ASR endpoint when API transcription mode is used.

Mitigation: Prefer local Whisper CPU or GPU mode for sensitive media and restrict ASR API URLs to trusted HTTPS services.

Risk: Publishing actions depend on stored Douyin credentials and may be executed with configurable confirmation bypasses.

Mitigation: Keep auto-confirm disabled for account posts unless the workflow is intentionally non-interactive and the final caption and visibility are reviewed elsewhere.

Risk: Transcript caches and fallback outbox packages can retain video-derived text, metadata, captions, and local source paths.

Mitigation: Periodically delete transcript caches and outbox files, and store them only in access-controlled local directories.

Risk: The local transcription path depends on an external Whisper binary and model file.

Mitigation: Verify the Whisper dependency and model source before installing or using them.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/yjli-new/skills/douyin-upload-skill)
- [Artifact README](artifact/README.md)
- [Douyin Open Platform](https://developer.open-douyin.com/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands and machine-readable JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The publish command can return official publish results or fallback outbox file paths.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
