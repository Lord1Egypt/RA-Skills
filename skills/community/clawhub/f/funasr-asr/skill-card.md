## Description:

Local speech recognition using Alibaba DAMO Academy's FunASR for transcribing audio and video files with SenseVoiceSmall by default and multilingual support for Chinese, English, Japanese, Korean, and Cantonese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruitao](https://clawhub.ai/user/ruitao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert local audio, voice messages, and video sources into text through a local FunASR workflow. It is intended for speech-to-text tasks where local model execution, segmentation, and memory-aware transcription are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wrapper can execute shell commands from user-controlled file paths.

Mitigation: Review before installing, use trusted local media paths, avoid elevated privileges, and prefer an isolated environment.

Risk: The video workflow accepts unrestricted URLs.

Mitigation: Use trusted public video URLs only, validate URLs before use, and run the skill in a constrained environment.

Risk: Broad dependency installation can change runtime behavior over time.

Mitigation: Pin dependencies and review package updates before broad use.

## Reference(s):

- [FunASR Installation Guide](references/installation.md)
- [Memory Optimization Guide](references/memory-optimization.md)
- [Model Comparison](references/model-comparison.md)
- [Video Transcription Workflow](references/video-workflow.md)
- [ClawHub Skill Page](https://clawhub.ai/ruitao/skills/funasr-asr)
- [Publisher Profile](https://clawhub.ai/user/ruitao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Plain text or JSON transcription results, plus Markdown guidance with shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download local ASR models on first use and may use ffmpeg or yt-dlp for video workflows.]

## Skill Version(s):

2.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
