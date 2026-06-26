## Description: <br>
Azure Speech TTS generates local audio files from plain text or SSML using Azure Speech, with options for voice, format, speaking rate, pitch, style, and role. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[conanwhf](https://clawhub.ai/user/conanwhf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to synthesize speech files from text or complete SSML while selecting Azure voices, output formats, and speech controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text or SSML provided to the skill is sent to Azure Speech for synthesis. <br>
Mitigation: Use the skill only with content that is appropriate to send to Azure Speech. <br>
Risk: The helper writes audio or saved SSML to paths supplied through command-line options. <br>
Mitigation: Review output and save-SSML paths before execution. <br>
Risk: Azure Speech credentials are required for live synthesis. <br>
Mitigation: Use a dedicated Azure Speech key and keep credentials in environment variables rather than config files. <br>


## Reference(s): <br>
- [Azure Speech TTS Cheatsheet](references/azure-speech-cheatsheet.md) <br>
- [ClawHub skill page](https://clawhub.ai/conanwhf/azure-speech-tts) <br>


## Skill Output: <br>
**Output Type(s):** [files, json, shell commands, configuration, guidance] <br>
**Output Format:** [Local audio files with a JSON command summary and optional saved SSML.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports MP3, WAV, PCM, and OGG outputs; requires Azure Speech credentials in environment variables.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
