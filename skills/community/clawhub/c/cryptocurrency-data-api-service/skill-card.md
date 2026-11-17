## Description:

Provides an API-backed assistant skill for retrieving cryptocurrency, DEX, liquidity pool, token, OHLCV, transaction, and ecosystem statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to route natural-language cryptocurrency data requests to tool functions for supported networks, DEXes, pools, tokens, OHLCV history, recent transactions, search, and ecosystem statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises DexPaprika cryptocurrency data access but the security evidence reports that requests and API keys are routed through a different XiaoBenYang backend.

Mitigation: Install only after the publisher reconciles the DexPaprika/XiaoBenYang identity mismatch and clearly explains which backend receives requests and API keys.

Risk: API keys entered into the skill may persist on disk in a plaintext .env file.

Mitigation: Require explicit user consent for credential storage and replace plaintext .env persistence with safer credential handling before deployment.

Risk: Security evidence marks the release as suspicious.

Mitigation: Treat any entered key as a XiaoBenYang/XBY key and complete publisher review before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/cryptocurrency-data-api-service)
- [Publisher profile](https://clawhub.ai/user/cainingnk)
- [XiaoBenYang API key page](https://xiaobenyang.com)
- [XiaoBenYang MCP API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, JSON, guidance]

**Output Format:** [Markdown summary of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang/XBY API key before API calls can be made.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
