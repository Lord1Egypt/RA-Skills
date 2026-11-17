## Description:

Generate complete Amazon listing drafts with title, bullets, image plan, prompts, and video script.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lenger666](https://clawhub.ai/user/lenger666)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, marketers, and agent users use this skill to draft Amazon listing copy, image plans, image prompts, and a product video script from supplied product details and market direction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product details, prompts, image URLs, and configured API credentials may be sent to external model or image services.

Mitigation: Use tightly scoped keys, avoid sensitive product data unless the external services are approved, and review service configuration before enabling the skill.

Risk: Optional image generation includes recipient-routing and outbound Feishu image messaging behavior.

Mitigation: Review Feishu recipient settings and routing behavior before enabling image generation or outbound messaging.

Risk: The server security summary flags under-disclosed credential, logging, recipient-discovery, and outbound messaging behavior.

Mitigation: Avoid shared or writable skill directories, do not put untrusted content in .env, and rotate image workflow keys if this version has already run with logging enabled.

## Reference(s):

- [Amazon Listing Factory ClawHub release](https://clawhub.ai/lenger666/skills/amazon-listing-factory)
- [Complete tutorial](https://my.feishu.cn/docx/DzpHdBjJdosX6Nx7CAMc9OY5nZf)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON containing Markdown-formatted listing content, image prompts, video script fields, and optional image URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional image generation can call external model and image workflow services when configured.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
