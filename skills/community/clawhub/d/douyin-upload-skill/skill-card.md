## Description: <br>
Login and publish Douyin (China mainland) videos from local files with OAuth, local speech-to-text, and generated caption drafts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YJLi-new](https://clawhub.ai/user/YJLi-new) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to authorize a Douyin account, prepare captions from local video audio, and publish through Douyin OpenAPI or export an outbox package when publishing permission is unavailable. <br>

### Deployment Geography for Use: <br>
China mainland <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Douyin OAuth publishing access and stores local tokens/config. <br>
Mitigation: Install only when that access level is acceptable, protect the local configuration directory, and rotate or revoke Douyin credentials if the machine is shared or compromised. <br>
Risk: The default ASR mode can send extracted video audio to a remote ASR API. <br>
Mitigation: For sensitive videos, set ASR mode to whisper-cpu or whisper-gpu before running prepare; use api mode only when the configured ASR provider is intentionally trusted. <br>
Risk: Unattended publishing can occur if auto-confirm is enabled. <br>
Mitigation: Keep auto-confirm disabled unless unattended publishing is explicitly required, and review final captions and visibility settings before publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/YJLi-new/douyin-upload-skill) <br>
- [Publisher profile](https://clawhub.ai/user/YJLi-new) <br>
- [Douyin Open Platform](https://developer.open-douyin.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON CLI output contracts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI returns machine-readable JSON and may create local outbox files for fallback publishing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
