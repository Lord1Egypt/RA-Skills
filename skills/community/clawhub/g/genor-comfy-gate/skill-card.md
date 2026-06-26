## Description: <br>
Comprehensive multi-modal gateway for ComfyUI enabling audio generation with ACE-Step 1.5 and photorealistic image creation via SDXL workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[genortg](https://clawhub.ai/user/genortg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate a local ComfyUI gateway for audio and image generation, workflow management, media retrieval, and MCP-based tool access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The gateway exposes broad agent-accessible ComfyUI administration, media, and file-handling capabilities. <br>
Mitigation: Install only for an intended local or trusted-network gateway, require a non-empty API key, and review access before exposing it to other users or agents. <br>
Risk: Raw generation, workflow upload, media resource access, and restart features can materially change gateway behavior or expose generated content. <br>
Mitigation: Disable or restrict those features unless they are needed, and review workflow uploads and generated outputs before sharing them. <br>
Risk: Generated media access links can behave like long-lived bearer URLs. <br>
Mitigation: Treat media links as private credentials, prefer short TTLs where possible, and avoid publishing them in shared logs or chats. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/genortg/genor-comfy-gate) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/genortg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON API or MCP payloads, configuration notes, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return workflow metadata, generated media URLs, and saved audio or image file paths when used with a running gateway.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
