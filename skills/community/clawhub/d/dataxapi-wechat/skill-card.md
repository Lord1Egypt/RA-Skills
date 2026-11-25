## Description:

This skill retrieves public WeChat Search posts, accounts, keyword suggestions, index history, and mini-program listings through DataXAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[data-x-api](https://clawhub.ai/user/data-x-api)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to help users find and summarize public WeChat Search content, Official Accounts, keyword suggestions, WeChat Index history, and mini-programs through DataXAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan notes an unpinned package installation method and partial reference coverage, so the benign verdict is not a guarantee that the package is safe.

Mitigation: Review and verify the package source and version before installing, and treat the scan result as incomplete.

Risk: Each data request is billed per call, and fetching additional pages creates additional charges.

Mitigation: Check the endpoint price before calling, set a maximum price, and fetch more pages only when needed.

## Reference(s):

- [DataXAPI WeChat Search API documentation](https://dataxapi.com/apis/wechat/)
- [DataXAPI WeChat pricing](https://dataxapi.com/pricing/wechat/)
- [DataXAPI agent setup guide](https://dataxapi.com/agents.md)
- [DataXAPI homepage](https://dataxapi.com)
- [ClawHub skill release](https://clawhub.ai/data-x-api/skills/dataxapi-wechat)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured API data and concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are public WeChat Search data; API calls are charged per endpoint call.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
