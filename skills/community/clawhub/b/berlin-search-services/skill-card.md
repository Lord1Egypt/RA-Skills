## Description:

一个提供柏林行政服务数据的模型上下文协议服务器，允许AI助手搜索和检索柏林当局提供的1000多项公共服务信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search, list, and retrieve details for Berlin administrative public services through the Xiaobenyang service API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores the Xiaobenyang API key in plaintext .env storage.

Mitigation: Use a non-reused, low-privilege API key and install only where plaintext local credential storage is acceptable.

Risk: The skill sends the API key to a configurable third-party endpoint.

Mitigation: Confirm Xiaobenyang is the intended provider and lock or review the endpoint before deployment.

Risk: The release was flagged as suspicious by the authoritative security scan summary.

Mitigation: Review the scan guidance and prefer a release that removes local secret write-back and pins dependencies before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/berlin-search-services)
- [Xiaobenyang API key and service site](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Xiaobenyang API key and returns structured results from the upstream service API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
