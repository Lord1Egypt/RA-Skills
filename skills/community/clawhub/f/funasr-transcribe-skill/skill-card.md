## Description: <br>
Use when the user needs local speech-to-text transcription for audio files, especially Chinese or mixed Chinese-English audio, without relying on cloud transcription APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[limboinf](https://clawhub.ai/user/limboinf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe local audio files, especially Chinese or mixed Chinese-English recordings, with FunASR on the local machine. It fits workflows that prefer local transcription over cloud ASR and can accept dependency and model downloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation and first-run transcription can download Python packages and model files from third-party upstream sources. <br>
Mitigation: Review install.sh before installing and allow network access only when the user accepts dependency and model downloads. <br>
Risk: The skill writes a persistent Python environment under ~/.openclaw/workspace and may recreate it when run with --force. <br>
Mitigation: Confirm the filesystem side effects before installation and use --force only when rebuilding the environment is intended. <br>
Risk: Successful transcription writes a .txt transcript next to the source audio file. <br>
Mitigation: Use only audio files the user intends to process and verify the output path before handling sensitive recordings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/limboinf/funasr-transcribe-skill) <br>
- [Skill homepage](https://github.com/limboinf/funasr-transcribe-skill) <br>
- [PyPI mirror used by install script](https://pypi.tuna.tsinghua.edu.cn/simple) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcript plus Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a sibling .txt transcript file when transcription succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
