## Description:

AI大模型专家｜Nano Banana Pro 图片生成与编辑 helps ecommerce, brand, advertising, social media, and cross-border commerce teams generate and edit product, campaign, poster, and reference-guided images through AI-HIVE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, brand, advertising, social media, and cross-border commerce teams use this skill to run Nano Banana Pro image generation and editing workflows through AI-HIVE. It helps prepare prompts, upload selected reference images, choose a routing mode, submit tasks, poll task status, and download results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be implicitly invoked and can upload a user-specified local media path to an external service.

Mitigation: Review before installing, require explicit intent to use AI-HIVE/Nano Banana Pro, and verify each --image or upload path before execution.

Risk: Prompts, selected files, and generated task metadata may be sent to AI-HIVE or object storage.

Mitigation: Do not use sensitive local paths or confidential assets unless the user has approved sending them to the service.

Risk: Generation tasks may consume account quota or incur charges.

Mitigation: Check the routing mode, batch size, model configuration, and pricing snapshot before submitting high-cost or batch work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-nano-banana-pro-image-generation-editing)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task/status output, and downloaded media files when generation completes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI-HIVE API key or local AI-HIVE configuration; may upload selected media files and create billable generation tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
