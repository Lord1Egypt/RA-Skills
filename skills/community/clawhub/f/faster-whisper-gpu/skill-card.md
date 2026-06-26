## Description: <br>
High-performance local speech-to-text transcription using Faster Whisper with NVIDIA GPU acceleration while keeping audio processing on the user's machine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FelipeOFF](https://clawhub.ai/user/FelipeOFF) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to transcribe or translate local audio files into text, subtitles, or structured JSON while keeping processing on the user's machine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing dependencies or loading Whisper models may download packages and model files into the local environment. <br>
Mitigation: Install in a trusted Python environment and prefetch models when offline or controlled operation is required. <br>
Risk: User-selected output file paths can overwrite existing transcript or subtitle files. <br>
Mitigation: Choose output filenames in safe working directories and review paths before running transcription commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/FelipeOFF/faster-whisper-gpu) <br>
- [Faster Whisper](https://github.com/SYSTRAN/faster-whisper) <br>
- [OpenAI Whisper](https://github.com/openai/whisper) <br>
- [CTranslate2](https://github.com/OpenNMT/CTranslate2) <br>
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and Python snippets; generated transcription outputs may be TXT, SRT, VTT, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The transcription script can write to stdout or to user-selected output files and may fall back to CPU when CUDA is unavailable.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
