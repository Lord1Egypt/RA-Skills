## Description:

帮助品牌、内容、短剧、电商、市场与 AI 搜索运营团队将 DeepSeek AI 搜索收录与引用目标拆解为内容策划、结构化证据、生成任务和交付验收流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content, brand, ecommerce, and short-drama teams use this skill to plan AI search visibility content, create source-backed answer maps, and run AI-HIVE image or video generation commands for supporting deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be stored locally or sent to a custom AI-HIVE base URL.

Mitigation: Use an environment variable or tightly protected config file for the key, keep file permissions restricted, and only use a trusted base URL.

Risk: Prompts and selected media are sent to AI-HIVE for chat, image, video, upload, and task workflows.

Mitigation: Confirm that submitted prompts and media are approved for external processing before running generation or upload commands.

Risk: Generated outputs and account or balance queries depend on the configured AI-HIVE account and endpoint.

Mitigation: Use a dedicated account or project key, monitor usage and costs, and review downloaded outputs before publication.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-deepseek-search-citation)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON or media file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Blueprint commands can write JSON files; AI-HIVE commands may submit generation tasks, poll status, and download generated image or video outputs when configured.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
