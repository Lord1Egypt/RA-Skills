## Description: <br>
设计框架自动生成套件（框架生成器）：收到设计需求后自动生成完整设计框架并发送群预览。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[807209066](https://clawhub.ai/user/807209066) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Design automation users and developers use this skill to turn structured design requests from a Telegram group into a design framework, generated image prompt, and group preview for confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow relies on separate companion scripts that may handle OpenRouter keys, Telegram bot tokens, and group messaging behavior. <br>
Mitigation: Inspect and trust the design-framework-sender scripts before installation, confirm credential storage, and restrict the Telegram bot to the intended chat. <br>
Risk: Design requests or reference images may contain confidential material that is sent through a group workflow and an external API provider. <br>
Mitigation: Avoid confidential design requests or reference images unless the Telegram group and API provider are approved for that material. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown-style design framework text, generated prompt text, and Telegram preview actions executed through companion shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on the separate design-framework-sender scripts for prompt generation, Telegram messaging, and configuration loading.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
