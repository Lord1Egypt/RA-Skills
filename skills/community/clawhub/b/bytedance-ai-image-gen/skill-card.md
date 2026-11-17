## Description:

ByteDance AI Image Gen calls Volcengine Ark Doubao Seedream models to generate and edit single images, image sets, image-to-image edits, and multi-image fusions with automatic model selection and daily usage limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[etmnb](https://clawhub.ai/user/etmnb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate or edit images with Volcengine Ark Doubao Seedream models from natural-language prompts, reference images, or multiple images. It helps agents choose model and size parameters, run the Python CLI, and return generated local image paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and reference images may be sent to Volcengine services.

Mitigation: Use only prompts and images that are acceptable to share with Volcengine; avoid sensitive local images.

Risk: The skill can store prompts, image URLs, usage counts, generated files, and temporary copies locally.

Mitigation: Review and periodically clear the local history, Image, and Temp directories, and set storage paths deliberately when needed.

Risk: The skill instructs agents to execute generation without a second confirmation, which can consume service quota.

Mitigation: Review trigger behavior before installation and restrict use to contexts where automatic execution is acceptable.

Risk: API keys and model endpoint identifiers are required for operation.

Mitigation: Store secrets in secure environment management rather than a skill-directory .env file when possible.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/etmnb/skills/bytedance-ai-image-gen)
- [Volcengine Ark Seedream API Documentation](https://www.volcengine.com/docs/82379/1541523)
- [Volcengine Ark Console](https://console.volcengine.com/ark)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Console text with generated image file paths and status details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save generated images under a local Image directory and keep seven-day prompt and usage history.]

## Skill Version(s):

2.4.2 (source: server release metadata; artifact frontmatter reports 2.3.0 and artifact _meta.json reports 2.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
