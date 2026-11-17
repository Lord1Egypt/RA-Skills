## Description:

通过 Clawec API 查询 Ozon 热搜词榜单（搜索指数、订购金额、转化、供需比等，支持类目与多维筛选）。在用户需要 Ozon 热搜词、关键词榜单、选词机会、类目搜索趋势调研时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[anyunzhong](https://clawhub.ai/user/anyunzhong)

### License/Terms of Use:

MIT-0

## Use Case:

External cross-border e-commerce sellers and operators use this skill to query Ozon hot keyword rankings, filter by category and metrics, and produce Chinese trend analysis and keyword-selection recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Ozon keyword research queries and the ClawEC API key to www.clawec.com.

Mitigation: Use the CLAWEC_API_KEY environment variable, avoid hardcoding secrets, and install only when that external API use is acceptable.

Risk: Keyword recommendations may be misleading if API errors, sparse results, or pagination are not checked.

Mitigation: Check top-level status, data.success, error messages, filters, page metadata, and total result counts before presenting conclusions.

## Reference(s):

- [Response schema](references/response-schema.md)
- [ClawEC API base](https://www.clawec.com/api)
- [Ozon hot-ranking endpoint](https://www.clawec.com/api/aigc/ec/ozon/data/keyword/hot-ranking)
- [ClawHub skill page](https://clawhub.ai/anyunzhong/skills/clawec-ozon-keyword-hot-ranking)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown report with optional bash/curl snippets and API JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWEC_API_KEY and sends Ozon keyword research queries to www.clawec.com; pageSize is capped at 15.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
