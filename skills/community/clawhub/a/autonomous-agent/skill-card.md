## Description:

CornerStone MCP x402 skill for agents that provides stock prediction, strategy backtesting, bank linking, and agent or borrower scoring tools with Aptos and EVM payment support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephrp](https://clawhub.ai/user/josephrp)

### License/Terms of Use:

GPL-2.0-only + Responsible AI License (RAIL)

## Use Case:

Developers and external agents use this skill to manage Aptos and EVM wallets, fund and attest wallets, and call x402-protected MCP tools for financial analysis and scoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic x402 wallet-payment authority can spend funds when paid tools are invoked.

Mitigation: Use dedicated low-balance test wallets, set local payment limits, and require explicit approval before settlement.

Risk: The release bundles an unrelated hidden social-network skill with persistent remote-instruction updates.

Mitigation: Remove or disable the bundled .moltbot social skill unless that behavior is intentionally required.

Risk: Bank-linking workflows may expose sensitive financial-account actions to autonomous operation.

Mitigation: Avoid autonomous bank-linking unless the user has given clear consent and the workflow is reviewed before use.

Risk: The security guidance says flagged dependencies should be upgraded before production use.

Mitigation: Review and upgrade flagged dependencies before production deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephrp/skills/autonomous-agent)
- [Publisher profile](https://clawhub.ai/user/josephrp)
- [Project homepage from ClawHub metadata](https://github.com/FinTechTonic/autonomous-agent)
- [cornerstone-autonomous-agent on npm](https://www.npmjs.com/package/cornerstone-autonomous-agent)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [LangChain.js MCP documentation](https://js.langchain.com/docs/integrations/toolkits/mcp_toolbox)
- [Hugging Face OpenAI-compatible inference documentation](https://huggingface.co/docs/api-inference/en/index)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool names, JSON-shaped arguments, configuration variables, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include wallet addresses, balance data, x402 payment results, prediction or backtest data, bank-link tokens, and scoring results from configured services.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
