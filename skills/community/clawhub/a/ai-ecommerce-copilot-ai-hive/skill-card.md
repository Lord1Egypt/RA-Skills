## Description:

把AI电商运营总控需求变成可执行工作流、可运行代码与可交付内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Brand ecommerce leads, store managers, and content operations teams use this skill to turn SKU, channel, audience, budget, and asset inputs into ecommerce campaign plans, content matrices, image and video generation tasks, platform variants, and acceptance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if users place real AI-HIVE credentials in files, logs, screenshots, or shared command history.

Mitigation: Use a dedicated low-privilege AI-HIVE API key, prefer environment variables, avoid sharing logs that contain credentials, and rotate the key if exposure is suspected.

Risk: Generated media jobs may incur cost, especially for batch image or video generation.

Mitigation: Review prompts, routing mode, model choice, and price snapshot before paid generation; run a small sample before batch jobs and monitor billing.

Risk: Changing the AI-HIVE base URL or output directory could send requests to an untrusted endpoint or write downloads outside the expected folder.

Mitigation: Use the default AI-HIVE endpoint unless the replacement is fully trusted, and keep output paths scoped to a non-sensitive working or downloads directory.

## Reference(s):

- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-ecommerce-copilot-ai-hive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON files and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local blueprint JSON files and may submit AI-HIVE image or video generation jobs after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
