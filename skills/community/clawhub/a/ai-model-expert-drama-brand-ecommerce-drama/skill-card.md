## Description:

AI大模型专家｜品牌电商带货短剧 helps short-drama, comic-drama, brand, ecommerce, advertising, and internationalization teams plan assets and use AI-HIVE image and video workflows for deliverable brand and ecommerce short-form drama content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand and ecommerce teams, and developers use this skill to plan short-drama projects, create reusable blueprints and prompts, and run AI-HIVE image/video generation, upload, task polling, and result retrieval workflows for commercial content delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A changed AI-HIVE endpoint could expose API keys or route requests through an unintended service.

Mitigation: Use only the legitimate AI-HIVE endpoint, avoid setting AI_HIVE_BASE_URL or --base-url to untrusted values, and use a limited, revocable API key.

Risk: Uploaded media may contain sensitive, proprietary, or unauthorized brand, likeness, music, or reference material.

Mitigation: Upload only media intended for AI-HIVE processing and confirm rights, privacy, and brand facts before generation.

Risk: Downloaded output handling may write files outside the expected output folder.

Mitigation: Review output locations before use and run the skill in a controlled workspace until path handling has been reviewed.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Install dependencies in a controlled environment and pin reviewed versions for production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-brand-ecommerce-drama)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash examples, JSON configuration, and generated JSON project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE media-generation tasks and retrieve task metadata or generated media files when configured with a valid API key.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
