## Description:

为短剧、漫剧、品牌、电商和市场团队将 ChatGPT、Claude、Gemini 等 AI 搜索与引用目标转化为结构化策划、证据字段、蓝图、图片和视频生成命令及复测记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand teams, e-commerce operators, and AI-search operations teams use this skill to structure answer-ready content, evidence fields, source cards, media prompts, and repeatable visibility checks. Developers can also use its scripts to create project blueprints and call AI-HIVE image or video generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts store and use AI-HIVE API credentials and can send them to a user-configured API endpoint.

Mitigation: Use environment variables or a protected config file, keep config permissions restricted, and only use the official AI-HIVE endpoint unless the alternate server is fully trusted.

Risk: Media generation commands can upload files, create billable generation tasks, poll remote services, and download generated outputs.

Mitigation: Review commands, prompts, uploaded files, model choices, pricing snapshots, and destination paths before execution.

## Reference(s):

- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-chatgpt-claude-gemini-citation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files and may initiate AI-HIVE upload, generation, polling, and download tasks when configured with an API key.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
