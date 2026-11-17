## Description:

查询未来清晨的活动信息。当用户询问未来清晨的活动、近期活动、活动安排、某个活动详情时使用。支持列出所有活动和根据活动ID获取详情。默认输出JSON，用户要求时可输出Markdown格式。

This skill is ready for commercial/non-commercial use.

## Publisher:

[longbai](https://clawhub.ai/user/longbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about 未来清晨 events, list recent activities, and retrieve details for a specific activity by campaign ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The detail lookup uses an inline Node.js command with an activity ID placeholder, and a malicious or unvalidated ID could alter the executed code.

Mitigation: Validate campaign IDs as UUIDs and pass them as data to the request body rather than interpolating arbitrary user input into node -e source code.

Risk: The skill issues live network requests to an external event API and returns event details that may change over time.

Mitigation: Use it only for explicit 未来清晨 event queries, review results before relying on them, and re-run the lookup when current event status matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longbai/skills/futuremorning)
- [Cumen ListCampaignsOfClub API](https://api.cumen.fun/api/xx.cumen.v1.CumenService/ListCampaignsOfClub)
- [Cumen GetCampaign API](https://api.cumen.fun/api/xx.cumen.v1.CumenService/GetCampaign)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, API Calls, Guidance]

**Output Format:** [JSON by default, with optional Markdown tables or detail summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event times are converted from UTC to UTC+8; list results are not guaranteed to be sorted.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
