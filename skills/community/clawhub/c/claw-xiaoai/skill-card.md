## Description: <br>
Claw Xiaoai is an energetic ex-trainee turned tech-company intern companion persona for consistent selfie prompts, captions, and OpenClaw companion configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MoveCall](https://clawhub.ai/user/MoveCall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, plugin authors, and OpenClaw users use this skill to keep Claw Xiaoai's persona, visual identity, selfie-trigger behavior, and ModelScope-backed image generation configuration consistent across integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selfie generation sends prompts to the external ModelScope image API. <br>
Mitigation: Use a dedicated ModelScope API key and avoid sensitive or sexualized prompt details. <br>
Risk: The skill can keep limited local prompt-continuity state. <br>
Mitigation: Review or delete ~/.openclaw/claw-xiaoai-state.json when local retention matters. <br>
Risk: Ambiguous requests such as "what are you doing" may trigger image generation. <br>
Mitigation: Add a confirmation step before generating images from ambiguous prompts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/MoveCall/claw-xiaoai) <br>
- [Claw Xiaoai Character Reference](references/claw-xiaoai-prompt.md) <br>
- [Visual Identity Anchor](references/visual-identity.md) <br>
- [Caption Style](references/caption-style.md) <br>
- [Config Template](references/config-template.md) <br>
- [Integration Notes](references/integration-notes.md) <br>
- [ModelScope Access Token](https://modelscope.cn/my/myaccesstoken) <br>
- [ModelScope Inference API](https://api-inference.modelscope.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, JSON configuration examples, shell commands, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call ModelScope for image generation and save generated selfies to local files when credentials are configured.] <br>

## Skill Version(s): <br>
0.0.9 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
