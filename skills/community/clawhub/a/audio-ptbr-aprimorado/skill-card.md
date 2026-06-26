## Description: <br>
Audio PTBR provides Brazilian Portuguese speech-to-text, AI response generation, and neural text-to-speech for OpenClaw voice replies with optional Claude API integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[henrique-simoes](https://clawhub.ai/user/henrique-simoes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to add Portuguese-Brazilian audio interaction to OpenClaw or compatible environments, converting voice messages into spoken or text responses. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can modify the host environment and download large audio, ML, and TTS dependencies. <br>
Mitigation: Review install.sh before use and run installation in a virtual environment or container; verify downloaded sources where practical. <br>
Risk: When ANTHROPIC_API_KEY is set, transcribed voice content may be sent to Anthropic for response generation. <br>
Mitigation: Leave ANTHROPIC_API_KEY unset unless external processing is acceptable, and use the OpenClaw fallback for deployments that require local handling. <br>
Risk: The OpenClaw fallback hands transcribed content to the local OpenClaw agent with that environment's configured permissions. <br>
Mitigation: Deploy only in OpenClaw environments whose agent permissions are understood, and validate behavior with health_check.py before production use. <br>


## Reference(s): <br>
- [Audio PTBR ClawHub Release](https://clawhub.ai/henrique-simoes/audio-ptbr-aprimorado) <br>
- [wav2vec2-large-xlsr-53-portuguese model card](https://huggingface.co/jonatasgrosman/wav2vec2-large-xlsr-53-portuguese) <br>
- [Piper TTS](https://github.com/rhasspy/piper) <br>
- [Anthropic Claude API](https://www.anthropic.com/claude) <br>


## Skill Output: <br>
**Output Type(s):** [text, audio, shell commands, configuration, guidance] <br>
**Output Format:** [Audio voice replies, text responses, JSON transcription results, and Markdown guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default OpenClaw mode is designed for silent audio-in/audio-out; explicit text mode and CLI utilities can return text or JSON.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
