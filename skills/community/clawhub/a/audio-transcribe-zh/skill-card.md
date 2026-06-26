## Description: <br>
Batch transcribes Chinese audio and video files into local text transcripts using FunASR Paraformer and ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swortect](https://clawhub.ai/user/swortect) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up local Chinese speech-to-text transcription for batches of media files, producing one transcript file next to each source video. It is aimed at CUDA GPU or CPU workflows that can use FunASR, ModelScope, PyTorch, and ffmpeg. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote install commands and model or tool downloads may pull code or binaries from external sources. <br>
Mitigation: Review each download source and install command before running them in the target environment. <br>
Risk: The batch script contains hard-coded local paths for input media, ffmpeg, and temporary workspace files. <br>
Mitigation: Edit the paths for the target machine before execution and confirm the temporary workspace is appropriate. <br>
Risk: The script writes transcript files next to source media and cleanup examples remove cache directories. <br>
Mitigation: Run it only on intended media folders, verify expected .txt output behavior, and inspect cache paths before cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swortect/audio-transcribe-zh) <br>
- [Publisher profile](https://clawhub.ai/user/swortect) <br>
- [ModelScope Paraformer-large model](https://www.modelscope.cn/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch) <br>
- [PyTorch CUDA wheel index](https://download.pytorch.org/whl/cu124) <br>
- [BtbN FFmpeg builds](https://github.com/BtbN/FFmpeg-Builds/releases) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets; the runtime script writes UTF-8 .txt transcript files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The batch script recursively processes .mp4 files and skips files that already have matching .txt transcripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
