## Description: <br>
Local text-to-speech using Piper for voice message delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bewareofddog](https://clawhub.ai/user/bewareofddog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to generate local text-to-speech audio from a text prompt and return the resulting MP3 path for voice-message delivery in supported channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup script can change the local environment by installing Python packages, installing ffmpeg through a system package manager, and downloading voice model files. <br>
Mitigation: Review the setup script before running it and install dependencies only in an environment where pip installs, system package changes, and Hugging Face downloads are acceptable. <br>
Risk: The server security review reports unsafe voice-name path handling. <br>
Mitigation: Use only known Piper voice names until the path handling is fixed, and avoid passing untrusted voice names to the scripts. <br>


## Reference(s): <br>
- [Piper](https://github.com/rhasspy/piper) <br>
- [Piper voices](https://huggingface.co/rhasspy/piper-voices) <br>
- [ClawHub skill page](https://clawhub.ai/bewareofddog/beware-piper-tts) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a generated MP3 file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local MP3 audio files in a temporary directory for voice-message delivery.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata, released 2026-02-22) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
