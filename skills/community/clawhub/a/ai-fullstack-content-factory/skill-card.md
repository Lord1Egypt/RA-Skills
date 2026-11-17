## Description:

AI全链路内容创作工厂 — 从热点发现到多平台发布，一站式内容生产工作流

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, AI bloggers, and content teams use this skill to discover AI or technology trends, generate long-form WeChat-style articles, create visual assets, and adapt content for Xiaohongshu distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may reach a live Xiaohongshu publishing action using an authenticated session without a clearly documented final approval gate.

Mitigation: Require a final preview-and-confirm step for the exact text, images, tags, target account, and visibility before any live post.

Risk: Generated trend coverage can become inaccurate or stale when search results are incomplete or time-sensitive.

Mitigation: Review cited source material and factual claims before publication, especially for recent AI or technology news.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/skills/ai-fullstack-content-factory)
- [README](artifact/README.md)
- [Workflow definition](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown articles, platform-adapted post text, generated image assets, and publication links when posting succeeds]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a valid Xiaohongshu authenticated session for live publishing; some platform publication steps may need manual confirmation.]

## Skill Version(s):

1.0.0 (source: workflow.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
