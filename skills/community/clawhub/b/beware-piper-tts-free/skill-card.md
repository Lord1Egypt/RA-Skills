## Description: <br>
Piper TTS Lite converts short text into local MP3 voice output using the default en_US-kusal-medium Piper voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to generate short English voice messages or MP3 narration locally from single text prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary says the skill mixes local-only claims with API-key, callback, and external-service language. <br>
Mitigation: Review the skill before installing, and do not provide API keys or callback URLs unless the publisher clarifies what service is used and what data is sent. <br>
Risk: The security guidance flags local command execution, package installation, model downloads, and MP3 file writes as operations to review. <br>
Mitigation: Run the skill only in an environment where those local operations are acceptable. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown and text with shell command examples, MP3 file paths, and optional audio_as_voice message wrappers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces one short-text audio result at a time and relies on local Piper, espeak-ng, model files, and writable output storage.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
