## Description:

Helps eyewear brands, ecommerce merchants, and styling content teams turn authorized eyewear and portrait inputs into AI-HIVE workflows for virtual try-on previews, face-angle variants, scene versions, prompts, commands, and delivery checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External teams and developers use this skill to plan and execute Chinese-language AI eyewear try-on content for ecommerce, advertising, social media, and related commercial workflows. It supports production briefs, prompt strategy, optional AI-HIVE OpenAPI image generation, task tracking, and quality review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI-HIVE API client can send a bearer API key to a configurable server.

Mitigation: Use only the official AI-HIVE base URL and keep AI_HIVE_BASE_URL plus ~/.ai-hive/config.json under trusted user control.

Risk: Generated result files are downloaded from task result URLs without independent content validation.

Mitigation: Monitor download source and size, review generated files before reuse, and use no-download mode when only task metadata is needed.

Risk: Eyewear try-on workflows may involve API keys, personal images, brands, or commercial claims.

Mitigation: Use placeholder keys in examples, provide only authorized assets, avoid sensitive images unless the AI-HIVE account and workflow are trusted, and verify product, pricing, and claims before publication.

Risk: Generation calls may incur cost or produce unsuitable outputs.

Mitigation: Confirm final prompts, routing mode, model settings, and budget before execution; run small batches before larger jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/eyewear-tryon-preview-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with runnable shell commands and JSON task or blueprint records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files and downloaded AI-HIVE generation results when the user confirms API use.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
