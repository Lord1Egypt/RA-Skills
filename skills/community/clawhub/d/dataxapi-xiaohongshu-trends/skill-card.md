## Description:

Get the hot topics Xiaohongshu (RedNote) suggests to creators right now, with their heat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to check current Xiaohongshu creator inspiration topics and their heat scores, then develop note ideas from those trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npm package is unpinned, creating a supply-chain risk.

Mitigation: Wait until the package is pinned to a reviewed version before installing or running it.

Risk: The scan is incomplete, and use involves sending credentials to an API destination.

Mitigation: Review the unresolved references and verify the DataXAPI destination and credentials are appropriate before use.

## Reference(s):

- [DataXAPI](https://dataxapi.com)
- [Xiaohongshu trends API documentation](https://dataxapi.com/apis/xiaohongshu/trends/list/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON trend data with topic names, heat scores, and paging details; concise text summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each page contains up to 20 topics; additional pages incur another per-call charge.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
