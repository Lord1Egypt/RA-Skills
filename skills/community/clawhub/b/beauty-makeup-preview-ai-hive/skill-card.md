## Description:

This skill helps beauty brands, cosmetics sellers, creators, and content marketing teams turn authorized portraits, product shade information, visual references, channel constraints, and budget limits into makeup preview plans, prompts, runnable AI-HIVE commands, and delivery checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create production-ready AI makeup preview workflows for ecommerce, advertising, social commerce, and marketing content. It emphasizes authorized source assets, truthful product and shade anchors, reviewable intermediate plans, AI-preview labeling, and careful handling of billable AI-HIVE generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an AI-HIVE API key and allows the AI-HIVE base URL to be overridden, which could expose credentials if pointed at an untrusted endpoint.

Mitigation: Use only the documented AI-HIVE base URL or a trusted internal proxy, avoid untrusted --base-url, AI_HIVE_BASE_URL, and ~/.ai-hive/config.json base_url values, and prefer a dedicated low-limit API key.

Risk: Image generation and media upload tasks may consume credits and send selected portrait or brand assets to AI-HIVE.

Mitigation: Confirm final prompts, routing, model choice, budget, media authorization, and AI-preview labeling before running generation, and start with a small sample batch.

Risk: Makeup preview outputs could be mistaken for real product performance, exact color proof, or verified testimonials.

Mitigation: Label generated results as AI visual previews, keep unverified claims marked for review, and do not use model output as a substitute for product testing, platform data, or legal review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/beauty-makeup-preview-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task records such as routing, model, price snapshot, taskId, status, and downloaded file locations when generation is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
