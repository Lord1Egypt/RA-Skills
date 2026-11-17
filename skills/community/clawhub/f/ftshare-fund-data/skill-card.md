## Description:

基金数据技能集（market.ft.tech）。覆盖基金基本信息、净值历史、累计收益率、基金概览列表、支持基金标的列表。用户询问基金详情、基金净值、基金收益、基金列表时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shawn92](https://clawhub.ai/user/shawn92)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up A-share fund basic information, NAV history, cumulative return time series, fund overviews, and supported fund symbols from market.ft.tech. It is suited for answering fund detail, return, NAV, and fund list questions when a fund code or resolvable fund name is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs bundled Python scripts and sends fund codes, pagination values, and selected return periods to market.ft.tech.

Mitigation: Install only in environments where that execution and outbound access to market.ft.tech are permitted.

Risk: Users with strict governance requirements may need tighter execution and network controls.

Mitigation: Apply a permission policy that limits execution to run.py and network access to market.ft.tech.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shawn92/skills/ftshare-fund-data)
- [market.ft.tech API base URL](https://market.ft.tech)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands]

**Output Format:** [JSON data from bundled Python handlers, typically summarized by the agent as Markdown tables or bullet points.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fund codes, page values, page sizes, and return-period selectors as query inputs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
