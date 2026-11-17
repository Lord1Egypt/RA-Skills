## Description:

Download audio from a GETTR post or streaming page and transcribe it locally with MLX Whisper on Apple Silicon, producing timestamped VTT output for caller-managed summarization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin37li](https://clawhub.ai/user/kevin37li)

### License/Terms of Use:


## Use Case:

Developers and analysts use this skill to extract media URLs from GETTR posts or streams, download the audio locally, and create timestamped transcripts. It is intended for public or otherwise accessible GETTR media and does not handle authentication-gated posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A supplied media URL could point outside GETTR or to untrusted content.

Mitigation: Use only trusted media URLs derived from GETTR pages and confirm the URL before running the pipeline.

Risk: A loose slug or output base path could write files outside the intended transcript folder.

Mitigation: Keep slugs to letters, numbers, dashes, and underscores, and use the default output location unless a reviewed path is required.

Risk: The skill runs local shell scripts and depends on ffmpeg, pip-installed MLX Whisper, Homebrew, and a local model.

Mitigation: Run without elevated privileges and pin dependency and model versions before use in managed environments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kevin37li/skills/gettr-transcribe)
- [GETTR](https://gettr.com)
- [URL Patterns & Reference](references/api_reference.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated local WAV and VTT files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ffmpeg and mlx_whisper; produces audio.wav and audio.vtt under ./out/gettr-transcribe/<slug>/.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
