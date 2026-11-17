## Description:

具身智能领域前沿动态追踪与视频素材采集系统；覆盖顶会论文（ICRA/IROS/CoRL/CVPR/NeurIPS）、开源项目、实验室动态；优先采集有Demo视频的爆款工作；生成含发布时间/主页/代码/视频链接的结构化日报，支持视频号内容创作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessy-huang](https://clawhub.ai/user/jessy-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content researchers use this skill to track recent embodied AI papers, open-source projects, lab updates, and demo videos, then produce structured daily reports for research monitoring and video content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad shell execution access for a workflow that primarily needs public web research and reporting.

Mitigation: Run it in a sandbox without secrets or writable sensitive files, or prefer a version limited to web/search and read-only retrieval tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jessy-huang/skills/embodied-ai-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown daily report with links, ratings, and concise analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires source URLs for reported items, arXiv or conference details for papers, GitHub star counts for repositories, and demo-video availability when applicable.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
