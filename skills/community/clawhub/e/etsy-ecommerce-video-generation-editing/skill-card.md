## Description:

Create and edit Etsy listing videos for handmade, vintage and personalized products, including maker process, scale, customization, packaging and use demonstrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External Etsy sellers and commerce content creators use this skill to produce or edit listing videos that show handmade, vintage, personalized, packaging and product-use details while preserving item authenticity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles an AI Hive API key and selected product media uploads through a configurable API endpoint.

Mitigation: Install only when comfortable sharing those assets with AI Hive, keep the base URL on the official HTTPS endpoint, protect ~/.ai-hive/config.json, and avoid wrappers or environment variables that override AI_HIVE_BASE_URL.

Risk: Runtime dependencies and network calls are needed to submit and retrieve video generation tasks.

Mitigation: Install dependencies in a controlled environment with pinned versions and review generated media before publishing listing content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/etsy-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command examples and prompt guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides AI Hive video generation, editing, extension, media upload, task polling and local result download for Etsy listing assets.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
