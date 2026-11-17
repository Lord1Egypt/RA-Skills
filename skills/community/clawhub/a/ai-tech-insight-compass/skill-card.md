## Description:

AI科技资讯深度追踪与分析工作流。每日自动采集AI前沿动态、GitHub热门项目，生成3000-5000字技术深度文章并发布到公众号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and AI-focused content teams use this skill to collect current AI technology signals, validate trends with GitHub activity, summarize findings, and produce long-form technical articles for local archiving or optional publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes local file saving and external publication steps without clear confirmation gates.

Mitigation: Require explicit user confirmation before saving files or publishing content outside the workspace.

Risk: The artifact uses a /root output path for generated articles.

Mitigation: Change the output path to a user-controlled workspace or project directory before running the workflow.

Risk: The artifact includes a hard-coded HTTP publishing endpoint.

Mitigation: Remove the endpoint or replace it with a vetted, authenticated HTTPS publication target.

Risk: Generated technology articles may contain stale, incomplete, or misleading analysis from aggregated sources.

Mitigation: Review source material, claims, code examples, and publication copy before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-tech-insight-compass)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown technical article with optional code examples and publishing commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Targets 3000-5000 Chinese characters or words as described by the skill, with at least four code examples and at least five technical tags.]

## Skill Version(s):

1.0.0 (source: server release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
