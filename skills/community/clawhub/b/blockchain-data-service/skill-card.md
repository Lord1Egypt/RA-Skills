## Description:

Vitruveo MCP Server 是一个为 Vitruveo 网络提供只读区块链服务的模型上下文协议服务器，适用于AI代理访问区块链数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent users use this skill to query read-only Vitruveo and EVM blockchain data such as blocks, balances, transactions, contract reads, token metadata, and NFT ownership through an API-backed tool set.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a XiaoBenYang API key and the scan notes that it may be saved as plaintext in a local .env file.

Mitigation: Prefer environment-variable or secret-manager configuration and avoid committing or sharing local .env files.

Risk: The scan reports that the backend identity does not cleanly match the skill's Vitruveo-only description.

Mitigation: Review the publisher's backend documentation or wait for publisher clarification before relying on this as a strictly Vitruveo-scoped service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alinklab/skills/blockchain-data-service)
- [XiaoBenYang API key provider](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, JSON, guidance]

**Output Format:** [Markdown summaries of API-returned JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key for API-backed blockchain lookups.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
