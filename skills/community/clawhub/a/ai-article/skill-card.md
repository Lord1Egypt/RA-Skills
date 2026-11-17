## Description:

自动图文助手根据主题、受众、关键词、平台和品牌要求生成中文图文文章、正文配图、封面素材和可下载交付包。

This skill is ready for commercial/non-commercial use.

## Publisher:

[allinherog-star](https://clawhub.ai/user/allinherog-star)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, operations teams, and content media users use this skill to turn a topic or keyword brief into publishable Chinese long-form and social content with suggested structure, Markdown article output, generated images, and next-step recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided topics, audience details, keywords, and brand requirements are sent to the AI Skills API.

Mitigation: Use only approved API keys and avoid confidential drafts, customer data, or unreleased business plans unless ai-skills.ai is approved for that data.

Risk: Generated article text and images may need editorial and brand review before publication.

Mitigation: Review titles, structure, factual claims, imagery, watermark choices, and brand fit before publishing or distributing the generated artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/allinherog-star/skills/ai-article)
- [Publisher profile](https://clawhub.ai/user/allinherog-star)
- [AI Skills quick start](https://github.com/allinherog-star/ai-skills/tree/main#%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B)
- [AI Skills](https://ai-skills.ai)
- [form-schema.json](references/form-schema.json)
- [skill.json](references/skill.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, Files, API Calls, Configuration]

**Output Format:** [JSON response envelope containing Markdown and image artifact references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISKILLS_API_KEY; accepts JSON parameters including topic, tone, audience, keywords, platform, wordCount, imageCount, watermark settings, and brand requirements.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
