## Description:

Reads Douyin video metadata, official AI chapter summaries, key frames, and timestamped spoken-content transcripts generated from on-screen subtitle OCR.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52siriyue](https://clawhub.ai/user/52siriyue)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to inspect shared Douyin links, summarize what a video says, extract copy, and produce timestamped transcripts when subtitles are visible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill launches a browser and contacts user-supplied video URLs with weak URL validation.

Mitigation: Use it only with Douyin links or other video pages you trust, and run it in a network-restricted environment when possible.

Risk: The skill saves video-derived frames, cropped subtitles, OCR output, and transcripts locally.

Mitigation: Choose the output directory deliberately, review generated files for sensitive content, and delete frames and transcripts when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52siriyue/skills/douyin-video-read)
- [README](README.md)
- [Skill instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON metadata/transcript files, local image frames, and shell commands for browser capture and OCR workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [L1 can print Markdown or JSON metadata and chapter summaries; L2 writes frames, cropped subtitle images, OCR raw text, transcript.md, transcript.json, and manifest.md when OCR is disabled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
