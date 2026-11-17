## Description:

Searches Douyin videos, filters candidates, verifies the opened video title, extracts speech transcripts, and writes raw, cleaned, and correction-note outputs.

This skill is for research and development only.

## Publisher:

[poca233](https://clawhub.ai/user/poca233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and content researchers use this skill to gather Douyin video material, confirm that a selected result matches the intended video, transcribe speech, and prepare cleaned transcript files for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a persistent Douyin browser profile and a SiliconFlow API key, which can expose account or API credentials if shared or stored insecurely.

Mitigation: Use a dedicated browser profile, protect the profile and API key like credentials, prefer a throwaway or low-risk account, and keep secrets in a restricted environment.

Risk: Extracted audio is sent to SiliconFlow for transcription.

Mitigation: Process only media that is acceptable to upload to that provider and review content, privacy, and rights requirements before transcription.

Risk: The security evidence flags broad unvalidated network downloads.

Mitigation: Run in a sandboxed environment, use restricted output directories, and avoid untrusted links until URL validation and download limits are added.

Risk: Transcript and media outputs are stored locally and may contain sensitive or copyrighted content.

Mitigation: Store outputs in access-controlled directories, review usage rights before reuse, and remove temporary or unneeded files after review.

## Reference(s):

- [Filter Rules for Douyin Video Selection](references/filter-rules.md)
- [Douyin Video Skills Publish Copy](references/publish-copy.md)
- [Douyin Web](https://www.douyin.com/)
- [SiliconFlow](https://cloud.siliconflow.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown transcripts, JSON metadata, plain-text source links, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create per-video output directories containing transcript, cleaned transcript, correction notes, source link, and metadata files.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
