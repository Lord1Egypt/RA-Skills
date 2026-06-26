## Description: <br>
Provides local speech-to-text transcription using FunASR SenseVoice by default or OpenAI Whisper for multilingual transcription and translation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentlau2046-sudo](https://clawhub.ai/user/vincentlau2046-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to transcribe local audio files, choose FunASR or Whisper, set language and model options, and optionally save transcripts to a file. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default FunASR path can run downloaded model code. <br>
Mitigation: Use an isolated Python environment and review or pin the ModelScope model and dependencies before deployment. <br>
Risk: First run downloads model weights into the local cache. <br>
Mitigation: Allow downloads only from approved sources or pre-populate a reviewed cache in controlled environments. <br>
Risk: The script prepends a hard-coded /home/vincent dependency path. <br>
Mitigation: Remove or adjust the path before use so dependency resolution matches the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/vincentlau2046-sudo/asr-funasr) <br>
- [Skill source README](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands] <br>
**Output Format:** [Plain text transcript on stdout with optional transcript file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Engine, language, task, model size, and output path options affect runtime, quality, and saved output.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
