## Description:

This skill helps merchants, designers, and content creators turn AI image requests for ecommerce, advertising, marketing, and social media into structured bilingual prompts, negative constraints, reference-image strategies, model suggestions, and optional AI-HIVE generation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, designers, and content creators use this skill to convert image-generation needs into auditable visual briefs, bilingual prompts, negative constraints, reference-image strategies, model recommendations, and production checklists. Operators can also use the included scripts to create project blueprints and submit confirmed AI-HIVE image-generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can be sent to an unvalidated custom server when a custom AI_HIVE_BASE_URL or --base-url is used.

Mitigation: Use the default AI-HIVE endpoint unless the custom endpoint is fully trusted, and use a dedicated low-privilege API key that can be revoked.

Risk: The workflow can upload selected media, store an API key locally, download generated results, and submit billable generation tasks.

Mitigation: Confirm the final prompt, routing mode, model, budget, and media authorization before execution; run a small sample before batch generation.

Risk: Generated marketing or ecommerce content could include unsupported claims, unauthorized likenesses, or overly close reuse of protected source material.

Mitigation: Require source facts and usage rights, avoid unsupported performance or testimonial claims, and keep only abstract structure when reference rights are unclear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-image-prompt-master-ai-hive)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base URL](https://ai-hive.iclip.cn/api)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with prompt structures, checklists, command examples, and JSON or file outputs from helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit billable AI-HIVE generation tasks after user confirmation and may download generated media to a local output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
