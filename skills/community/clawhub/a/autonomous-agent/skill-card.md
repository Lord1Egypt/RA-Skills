## Description: <br>
Autonomous Agent Skills gives agents x402-paid MCP tools for stock prediction, backtesting, bank linking, score lookup, wallet setup, and Aptos/EVM payment handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephrp](https://clawhub.ai/user/Josephrp) <br>

### License/Terms of Use: <br>
GPL-2.0-only; Responsible AI License (RAIL) terms also stated <br>


## Use Case: <br>
External developers and agent operators use this skill to let an agent create or inspect wallets, fund and whitelist addresses, and call paid MCP tools for forecasts, backtests, bank linking, and reputation or borrower scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic x402 payment handling and wallet helpers can move funds if connected to funded wallets. <br>
Mitigation: Use a separate minimally funded wallet, prefer testnet or capped balances, and require human approval before any fund movement. <br>
Risk: Transfer, swap, and contract helpers expand the financial action surface beyond the main MCP payment workflow. <br>
Mitigation: Review or remove transfer, swap, and contract helpers when the deployment only needs MCP payments. <br>
Risk: The bundle includes unrelated Moltbook social automation instructions. <br>
Mitigation: Ignore or remove the bundled Moltbook skill unless autonomous social posting and messaging are explicitly intended. <br>
Risk: Bank linking and by-email score lookups can expose sensitive user or borrower information. <br>
Mitigation: Require explicit human approval before bank-linking, email score lookup, or sharing related results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Josephrp/autonomous-agent) <br>
- [Project homepage from ClawHub metadata](https://github.com/FinTechTonic/autonomous-agent) <br>
- [npm package](https://www.npmjs.com/package/cornerstone-autonomous-agent) <br>
- [Model Context Protocol](https://modelcontextprotocol.io) <br>
- [LangChain.js MCP documentation](https://js.langchain.com/docs/integrations/toolkits/mcp_toolbox) <br>
- [Hugging Face OpenAI-compatible inference documentation](https://huggingface.co/docs/api-inference/en/index) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and JSON-like tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or use local wallet files and may trigger paid MCP requests when configured.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
