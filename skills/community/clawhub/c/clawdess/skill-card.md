## Description: <br>
Clawdess helps an agent generate companion-style AI photos, videos, and voice notes through configured third-party media providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xwings](https://clawhub.ai/user/xwings) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to have an agent create or request AI-generated photos, short image-to-video clips, and TTS voice notes using configured provider API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal images, prompts, and voice text may be sent to third-party AI providers. <br>
Mitigation: Use only media and text suitable for those providers, configure the agent to ask before generating media, and review provider terms before use. <br>
Risk: Generated media may be retained in the local media cache. <br>
Mitigation: Periodically clear ~/.openclaw/media/clawdess when local retention is not desired. <br>
Risk: Provider API keys are required for photo, video, and voice generation. <br>
Mitigation: Use least-privilege API keys, store them in the documented environment variables, and rotate them if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xwings/clawdess) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance, media URLs] <br>
**Output Format:** [Markdown or plain text with shell command examples and MEDIA: URLs when generation succeeds.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated media may be cached locally under ~/.openclaw/media/clawdess.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
