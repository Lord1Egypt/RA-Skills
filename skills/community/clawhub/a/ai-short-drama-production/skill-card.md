## Description:

为多集或成套制作需求规划并执行 AI 短剧制作流程，从剧本、分镜和角色一致性设计，到 Seedance 任务、付费生成与交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[frankchenfei](https://clawhub.ai/user/frankchenfei)

### License/Terms of Use:

MIT-0

## Use Case:

短剧创作者和制作团队可用它把故事概念或剧本整理为可执行的多集制作方案，并管理从前期设计到视频生成、质检和交付的工作流。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated network destinations could expose the API key or cause unsafe downloads, and the scan evidence is incomplete.

Mitigation: Review the configured API endpoint and returned download URLs before use; provide ARK_API_KEY only for runs against trusted endpoints.

## Reference(s):

- [End-to-end orchestration](artifact/ai-short-drama-production/references/end-to-end-orchestration.md)
- [Production pipeline](artifact/ai-short-drama-production/references/production-pipeline.md)
- [Prompt consistency](artifact/ai-short-drama-production/references/prompt-consistency.md)
- [ClawHub release](https://clawhub.ai/frankchenfei/skills/ai-short-drama-production)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown production plans, CSV templates, JSON/JSONL task manifests, and executable commands or scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Production artifacts are scaled to the requested project scope.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
