## Description: <br>
Downloads audio from a GETTR post or streaming page and transcribes it locally with MLX Whisper on Apple Silicon, producing timestamped VTT transcripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kevin37Li](https://clawhub.ai/user/Kevin37Li) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to turn public or user-provided GETTR media into local timestamped transcripts for downstream review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and processes media URLs supplied by the user or extracted from GETTR. <br>
Mitigation: Use only intended public or authorized media URLs, and review the URL before running the pipeline. <br>
Risk: The pipeline depends on local ffmpeg and mlx-whisper installations. <br>
Mitigation: Install dependencies from trusted package sources and run the skill only in an environment where local media processing is acceptable. <br>
Risk: Private or authentication-gated GETTR content is not handled by the skill. <br>
Mitigation: Avoid private or gated content unless the user is authorized and intentionally provides a direct media URL. <br>
Risk: The skill writes audio and transcript outputs to a local out/gettr-transcribe directory. <br>
Mitigation: Review and manage generated audio.wav and audio.vtt files according to the sensitivity of the source media. <br>


## Reference(s): <br>
- [ClawHub Gettr Transcribe](https://clawhub.ai/Kevin37Li/gettr-transcribe) <br>
- [GETTR](https://gettr.com) <br>
- [URL Patterns & Reference](references/api_reference.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and local VTT transcript files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audio.wav and audio.vtt under ./out/gettr-transcribe/<slug>/; transcription stays in the source language.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
