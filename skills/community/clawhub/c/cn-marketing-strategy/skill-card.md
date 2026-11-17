## Description:

Chinese marketing strategy planner with API-powered benchmarks for creating data-driven plans across Xiaohongshu, Douyin, WeChat, Baidu, and ecommerce channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams and agents use this skill to plan China-focused digital campaigns, including audience analysis, channel strategy, content calendars, budget allocation, KPI frameworks, and benchmark-informed recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark lookups use an external Tencent SCF endpoint and may reveal IP address, request timing, and requested platform.

Mitigation: Avoid invoking benchmark lookups with sensitive campaign context, customer data, or confidential copy unless the publisher documents data handling clearly.

Risk: Marketing plans and benchmark-informed recommendations may be inaccurate or unsuitable for a specific campaign, budget, or regulatory context.

Mitigation: Review generated strategies, KPIs, compliance assumptions, and budget recommendations before using them in production campaigns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/cn-marketing-strategy)
- [Benchmark API base URL](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown strategy plans with tables, checklists, and optional inline shell commands for benchmark lookup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use an external Tencent SCF endpoint for benchmark lookups when the bundled script is invoked.]

## Skill Version(s):

2.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
