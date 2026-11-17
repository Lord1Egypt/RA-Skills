## Description:

帮助广告投手、品牌增长团队和创意代理商将商品、受众、投放平台、预算和合规约束转化为创意假设、钩子矩阵、静态图、短视频脚本、变量表和 A/B 测试计划。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, brand growth teams, and creative agencies use this skill to plan e-commerce ad creative workflows and prepare reviewable image, video, copy, prompt, command, and A/B-test deliverables. When generation is requested, it guides users through AI-HIVE model configuration, cost-aware routing, task submission, polling, and delivery review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys or selected media could be exposed if generation commands are pointed at an untrusted AI-HIVE base URL.

Mitigation: Use the default AI-HIVE URL, avoid untrusted AI_HIVE_BASE_URL or --base-url values, and use a limited, rotatable API key.

Risk: Reference images, videos, or audio supplied for creative generation may be uploaded to the AI-HIVE workflow.

Mitigation: Submit only media that the user is authorized to use and that is acceptable to share with the AI-HIVE service.

Risk: Task result downloads and broad network behavior remain higher-risk until host and size controls are tightened.

Mitigation: Restrict trusted hosts, validate upload and download URLs, and add download size limits before treating deployment as low-risk.

Risk: Ad creative outputs could contain unsupported claims, copied protected expression, fake testimonials, or platform-rule issues.

Mitigation: Review product facts, rights, claims, platform rules, and human approval before publishing or scaling generated creatives.

Risk: Image and video generation may incur cost, especially for batch tasks.

Mitigation: Confirm prompts, model mode, routing, and pricing snapshots before submission, and run a small sample before batch generation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/ecommerce-ad-creative-studio-ai-hive)
- [AI-HIVE Workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API Base URL](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include creative briefs, prompts, shot lists, task IDs, pricing snapshots, status records, file locations, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
