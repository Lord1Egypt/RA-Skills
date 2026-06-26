## Description: <br>
Converts Chinese text into natural-sounding local speech with ChatTTS, including controls for speed, pitch, emotion, and repeatable voice seeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wodecanyun66-spec](https://clawhub.ai/user/wodecanyun66-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to generate Chinese voice replies, document narration, notification audio, and long-text speech from local ChatTTS models. It is suited to workflows that need an agent to invoke local text-to-speech scripts and return a generated audio file reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First use can install unpinned Python packages and download ChatTTS model files. <br>
Mitigation: Run it in an isolated virtual environment or container, preinstall trusted pinned dependencies, and verify downloaded model artifacts before use. <br>
Risk: The skill is presented as local, but setup and first use can require network access for model downloads. <br>
Mitigation: Treat it as network-dependent until setup is complete, review allowed download endpoints, and cache approved model files for offline operation. <br>


## Reference(s): <br>
- [ChatTTS model on Hugging Face](https://huggingface.co/2Noise/ChatTTS) <br>
- [Hugging Face mirror used by artifact scripts](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with bash commands and qqvoice file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [References generated WAV or MP3 speech files; documented sample rate is 24000 Hz.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
