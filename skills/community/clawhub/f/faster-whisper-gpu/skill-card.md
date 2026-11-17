## Description:

High-performance local speech-to-text transcription using Faster Whisper with NVIDIA GPU acceleration that transcribes audio files locally without sending data to external services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felipeoff](https://clawhub.ai/user/felipeoff)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to transcribe local audio into text, subtitles, or structured JSON with configurable Faster Whisper models, languages, timestamps, and GPU or CPU execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation may introduce package supply-chain or environment contamination risk.

Mitigation: Install in an isolated virtual environment, avoid running pip as root, and pin or review dependency versions before use.

Risk: First-run model downloads may fetch large model artifacts into the Hugging Face cache.

Mitigation: Review model sources and cache location before use, especially in restricted or offline environments.

Risk: Transcript and subtitle outputs may contain sensitive spoken content.

Mitigation: Store generated output files in private locations and apply normal data-retention controls for sensitive audio-derived text.

## Reference(s):

- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper)
- [OpenAI Whisper](https://github.com/openai/whisper)
- [CTranslate2](https://github.com/OpenNMT/CTranslate2)
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- [Python Downloads](https://www.python.org/downloads/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with command examples; generated transcription outputs can be TXT, SRT, VTT, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write transcript, subtitle, or JSON files to a user-selected output path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
