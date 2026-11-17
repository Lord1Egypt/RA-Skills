## Description: <br>
Helps agents use the dlazy CLI to generate Chinese and English text-to-speech audio with the basic doubao-tts and keling-tts models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content teams, and agent users can use this skill to prepare dlazy CLI commands for basic text-to-speech workflows such as audiobook narration, prototype voice-over, and voice announcements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided text to dlazy's API for text-to-speech generation. <br>
Mitigation: Use the skill only for text that is acceptable to send to dlazy, and avoid submitting sensitive content unless the deployment's data handling requirements permit it. <br>
Risk: Generated MP3 outputs can overwrite existing local files if paths are reused. <br>
Mitigation: Run commands in a dedicated working folder or choose explicit unique output paths before execution. <br>
Risk: The workflow requires a dlazy API key for authentication. <br>
Mitigation: Configure the key through dlazy auth or the DLAZY_API_KEY environment variable, and do not paste keys into agent chat or commit them to version control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/dlazy-audio-generate-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown with inline bash commands and expected JSON or MP3 file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audio output paths or dlazy result URLs; requires a configured dlazy API key.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
