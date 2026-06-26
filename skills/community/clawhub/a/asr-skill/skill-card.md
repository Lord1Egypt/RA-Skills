## Description: <br>
A local speech-to-text skill based on Qwen3-ASR-0.6B that supports multilingual recognition and 22 Chinese dialects for OpenClaw voice interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yszheda](https://clawhub.ai/user/yszheda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to convert uploaded or webhook-delivered speech into text, including supported Chinese dialects and multilingual audio, before passing transcripts to an agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a network-facing audio service with under-scoped endpoints and weak deployment safeguards. <br>
Mitigation: Install only in a controlled environment, bind the service to 127.0.0.1 or protect it with firewall rules, and add authentication or signed webhook validation before exposure. <br>
Risk: Voice recordings and transcripts may contain sensitive information. <br>
Mitigation: Avoid sending sensitive voice recordings unless local storage, transcript handling, and downstream model forwarding have been reviewed for the deployment. <br>
Risk: Runtime dependencies may require review before deployment. <br>
Mitigation: Review and patch dependency versions before use in a managed environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yszheda/asr-skill) <br>
- [README](artifact/README.md) <br>
- [Installation guide](artifact/INSTALL.md) <br>
- [Skill metadata](artifact/skill.yml) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON responses containing transcription text, detected language, confidence, duration, and optional timestamps or alignment data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes audio files or base64 audio through local HTTP endpoints and returns transcript-oriented fields for agent use.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
