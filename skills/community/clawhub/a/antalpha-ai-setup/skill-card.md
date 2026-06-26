## Description: <br>
Install and configure the Antalpha Skills MCP server. Provides 146+ Web3 tools for DEX swaps, smart money tracking, Polymarket prediction markets, Hyperliquid perpetuals, CEX trading, Bitcoin mining, and DeFi analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bevanding](https://clawhub.ai/user/bevanding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent operators use this skill to connect MCP-compatible agents to Antalpha's Web3 tools for swaps, wallet analytics, prediction markets, perpetuals, CEX trading, mining, and DeFi analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup grants an AI agent broad wallet and trading capabilities without enough documented safety and credential boundaries. <br>
Mitigation: Configure the MCP client to require explicit approval before every trade, swap, transfer, leverage change, order, or copy-trading action. <br>
Risk: Sensitive credentials or funded wallets could be exposed to high-impact remote actions. <br>
Mitigation: Use least-privilege or read-only credentials where available, avoid funded wallets until approval and revocation behavior is clear, and disable tools that are not needed. <br>
Risk: The skill depends on trust in a third-party remote MCP service. <br>
Mitigation: Install only if the operator trusts Antalpha and has reviewed the registration, authentication, support, and rate-limit process. <br>


## Reference(s): <br>
- [Antalpha Skills MCP Server](https://mcp-skills.ai.antalpha.com) <br>
- [Antalpha MCP Documentation](https://github.com/antalpha-com/antalpha-skills) <br>
- [Antalpha Website](https://www.antalpha.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/bevanding/antalpha-ai-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown setup guide with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Antalpha registration and credentials; connected MCP tools can expose wallet, trading, transfer, leverage, and market-analysis actions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
