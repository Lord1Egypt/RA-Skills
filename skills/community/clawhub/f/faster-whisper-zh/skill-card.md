## Description: <br>
使用 faster-whisper 的本地语音转文字工具，支持 GPU 加速转录、词级时间戳和蒸馏模型。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mapleshadow](https://clawhub.ai/user/mapleshadow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transcribe local audio files into Chinese or multilingual text, with optional word timestamps, JSON output, voice activity detection, and batch processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports that the batch script hardcodes a third-party model mirror. <br>
Mitigation: Prefer the official Hugging Face endpoint unless hf-mirror.com is explicitly trusted for the deployment environment. <br>
Risk: The security summary reports unsafe shell command construction in the batch script. <br>
Mitigation: Avoid running batch transcription on directories containing untrusted filenames until the command construction is reviewed and fixed. <br>
Risk: Installing and running the skill downloads model and runtime dependencies before local transcription. <br>
Mitigation: Review before installing and use it only for audio the user intends to transcribe. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mapleshadow/faster-whisper-zh) <br>
- [Publisher profile](https://clawhub.ai/user/mapleshadow) <br>
- [Hugging Face mirror endpoint used by artifact](https://hf-mirror.com) <br>
- [PyTorch CUDA wheel index used by setup script](https://download.pytorch.org/whl/cu121) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Plain text or JSON transcription output, with shell commands and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write transcript files and a batch summary to the selected output directory.] <br>

## Skill Version(s): <br>
1.0.5 (source: evidence.release.version and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
