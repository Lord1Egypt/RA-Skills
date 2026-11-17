## Description:

Claw Xiaoai is an energetic ex-trainee turned tech-company intern companion skill for maintaining a consistent persona, selfie behavior, captions, and image-generation configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[movecall](https://clawhub.ai/user/movecall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to keep Claw Xiaoai's character prompt, selfie trigger rules, visual identity, captions, and companion configuration consistent across OpenClaw integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selfie requests and generated prompts may be sent to ModelScope.

Mitigation: Avoid including private, sensitive, or identifying details in selfie requests and prompts.

Risk: The skill saves recent request continuity state under ~/.openclaw.

Mitigation: Clear the Claw Xiaoai state file when local prompt history should not persist.

Risk: Image generation can write files to caller-provided output paths.

Mitigation: Use narrowly scoped output directories and review generated paths before wiring the skill into another host.

Risk: Broad conversational triggers may generate images when the user asks about photos, location, outfit, mood, or activity.

Mitigation: Keep trigger handling explicit in host integrations and confirm image generation behavior where consent or cost matters.

## Reference(s):

- [Claw Xiaoai Skill Page](https://clawhub.ai/movecall/skills/claw-xiaoai)
- [Claw Xiaoai Character Reference](artifact/references/claw-xiaoai-prompt.md)
- [Visual Identity Anchor](artifact/references/visual-identity.md)
- [Caption Style](artifact/references/caption-style.md)
- [Config Template](artifact/references/config-template.md)
- [Integration Notes](artifact/references/integration-notes.md)
- [ModelScope Access Token](https://modelscope.cn/my/myaccesstoken)
- [ModelScope API Endpoint](https://api-inference.modelscope.cn/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON configuration examples, shell command snippets, and generated image files when the backend is available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses ModelScope image generation with Node.js scripts; generated images are saved to caller-provided local paths.]

## Skill Version(s):

0.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
