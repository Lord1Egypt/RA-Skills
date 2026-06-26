## Description: <br>
Create Video helps an agent generate complete HeyGen videos from a text prompt, including script, avatar, visuals, voiceover, pacing, and captions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelwang11394](https://clawhub.ai/user/michaelwang11394) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, developers, and other external users use this skill to turn a brief or idea into a generated HeyGen video. It is useful for explainer, demo, marketing, prototype, and draft videos where the agent can choose the script, avatar, scenes, voiceover, and captions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants broad HeyGen account authority through the HeyGen API key, including video creation, listing, retrieval, and deletion. <br>
Mitigation: Use a scoped or dedicated HeyGen credential where available, limit use to the exact requested task, and require confirmation before deletion or other account-changing actions. <br>
Risk: Video generation can consume HeyGen credits. <br>
Mitigation: Confirm credit-consuming generation requests before execution and check remaining quota when cost or availability matters. <br>
Risk: Prompts, uploaded files, referenced URLs, and generated media may be shared with HeyGen. <br>
Mitigation: Upload or reference only media and prompts the user intends to share with HeyGen, and avoid sensitive or unauthorized content. <br>
Risk: Webhook and URL-import examples may need production hardening. <br>
Mitigation: Treat webhook and URL examples as templates, then add authentication, validation, secret handling, and deployment controls before production use. <br>


## Reference(s): <br>
- [Create Video with Video Agent](https://docs.heygen.com/reference/create-video-with-video-agent) <br>
- [Create Video on ClawHub](https://clawhub.ai/michaelwang11394/create-video) <br>
- [Video Agent Prompt Optimizer](references/prompt-optimizer.md) <br>
- [Visual Style Library](references/visual-styles.md) <br>
- [Video Agent API](references/video-agent.md) <br>
- [Video Status and Polling](references/video-status.md) <br>
- [Asset Upload and Management](references/assets.md) <br>
- [HeyGen Quota and Credits](references/quota.md) <br>
- [Webhooks](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline JSON, curl, TypeScript, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or request HeyGen MCP tool calls or direct API calls that consume credits, upload media, poll generation status, retrieve video URLs, manage videos, or configure webhooks.] <br>

## Skill Version(s): <br>
2.23.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
