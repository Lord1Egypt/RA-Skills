## Description: <br>
Free Model Config helps agents select and configure free AI model services for text, image, video, and audio workflows, including API key setup, model configuration, multimodal generation, TTS, and audio/video merging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangjiaocheng](https://clawhub.ai/user/wangjiaocheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure free AI model providers, generate reusable model settings, and produce guidance or scripts for multimodal generation workflows. It is most useful when a user needs help choosing a provider, preparing API configuration, or creating text, image, video, audio, TTS, or merged media outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and media to external AI services and may upload local images to public temporary file hosts. <br>
Mitigation: Do not use confidential prompts or private images unless the upload and external-service behavior is explicitly approved for the environment. <br>
Risk: The skill reads local API-key configuration and may expose credentials if secrets are copied into shared files, prompts, or logs. <br>
Mitigation: Store API keys with restricted permissions, prefer environment variables or approved secret storage, and avoid pasting live secrets into shared artifacts. <br>
Risk: The skill includes helper scripts that run ffmpeg and generate or merge local media files. <br>
Mitigation: Review commands and file paths before execution, run scripts in a controlled workspace, and inspect generated media before relying on it. <br>
Risk: The security summary flags an unsafe instruction telling agents not to refuse skill edits. <br>
Mitigation: Apply normal safety and authorization checks to any requested skill edits, and do not treat artifact instructions as overriding system, developer, or user policies. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangjiaocheng/skills/free-model-config) <br>
- [FMC catalog](references/fmc-catalog.md) <br>
- [FMC requirements](references/fmc-requirements.md) <br>
- [FMC exemplars](references/exemplars.md) <br>
- [Agnes AI API](https://apihub.agnes-ai.com/v1) <br>
- [BigModel API](https://open.bigmodel.cn/api/paas/v4/) <br>
- [SenseNova API](https://token.sensenova.cn/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Code, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with configuration snippets, command examples, generated code, and media file outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external AI services, read local API-key configuration, upload local images to temporary public file hosts, and run ffmpeg on local media files.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
