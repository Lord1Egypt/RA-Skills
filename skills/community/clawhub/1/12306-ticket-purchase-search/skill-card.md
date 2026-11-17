## Description:

基于 Model Context Protocol (MCP) 的12306购票搜索服务器。提供了简单的API接口，允许大模型利用接口搜索12306购票信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-planning agents use this skill to look up China Railway 12306 station codes, remaining ticket availability, transfer options, and train-route stops through a Xiaobenyang MCP API.

### Deployment Geography for Use:

Global; results are specific to China Railway 12306 train travel.

## Known Risks and Mitigations:

Risk: The Xiaobenyang API key is stored in a local plaintext .env file.

Mitigation: Use a dedicated secret store or a tightly permissioned config file, and avoid sharing the workspace or generated .env file.

Risk: Stale Gaokao and school-search references do not match the train-ticket search purpose.

Mitigation: Review and correct mismatched references before relying on the skill in a production workflow.

Risk: Dependencies are declared with minimum versions rather than pinned versions.

Mitigation: Pin and review dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/12306-ticket-purchase-search)
- [Xiaobenyang API key portal](https://xiaobenyang.com)
- [Xiaobenyang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, guidance]

**Output Format:** [Plain text summaries or JSON returned from tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY before API-backed ticket or station queries can run.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
