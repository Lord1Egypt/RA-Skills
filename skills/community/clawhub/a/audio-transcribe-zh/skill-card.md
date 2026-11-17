## Description:

批量将中文音频或视频文件转录为文本，并为每个文件生成同目录的 .txt 输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[swortect](https://clawhub.ai/user/swortect)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up a local Chinese transcription workflow for batches of audio or video files. It is intended for CUDA GPU or CPU execution with FFmpeg audio extraction and FunASR Paraformer transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes unverified remote installer commands and a third-party executable download proxy.

Mitigation: Prefer package-manager installs or pinned downloads with checksums for uv and FFmpeg, and avoid the gh-proxy executable download unless it has been audited.

Risk: The included batch script contains hardcoded local Windows paths.

Mitigation: Review and replace local paths before running the script in another workspace or on another machine.

Risk: Cache-deletion commands can remove local model or transcription-related caches.

Mitigation: Check each cache path before copying cleanup commands, especially on shared machines.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/swortect/skills/audio-transcribe-zh)
- [ModelScope Paraformer-large ASR model](https://www.modelscope.cn/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch)
- [FFmpeg Builds](https://github.com/BtbN/FFmpeg-Builds)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and Python code blocks, plus generated .txt transcript files when the script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transcription quality and runtime depend on local media quality, FFmpeg availability, model downloads, and CPU or CUDA GPU configuration.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
