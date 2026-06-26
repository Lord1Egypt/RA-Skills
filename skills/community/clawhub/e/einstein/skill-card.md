## Description: <br>
Blockchain analytics and DeFi intelligence via Einstein's x402 micropayment services for on-chain market analysis, token research, whale tracking, smart money tracking, rug pull scanning, launchpad monitoring, portfolio analysis, MEV detection, cross-chain arbitrage, and Polymarket data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChuXo](https://clawhub.ai/user/ChuXo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run paid blockchain analytics queries through Einstein x402 services, including market, wallet, token security, launchpad, DeFi, NFT, and prediction-market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a crypto private key and can sign real USDC payments. <br>
Mitigation: Use a dedicated, low-balance Base USDC wallet and prefer the EINSTEIN_X402_PRIVATE_KEY environment variable over config.json. <br>
Risk: Automated confirmation can allow paid queries without an interactive payment review. <br>
Mitigation: Avoid --yes, EINSTEIN_AUTO_CONFIRM, or global auto-confirm in agent workflows unless spending limits and query scope are controlled. <br>
Risk: The free epstein-search command sends search terms to DugganUSA rather than the Einstein x402 service. <br>
Mitigation: Do not submit sensitive search terms to epstein-search unless that third-party routing is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ChuXo/einstein) <br>
- [Einstein Homepage](https://emc2ai.io) <br>
- [Einstein x402 Services Catalog](references/services-catalog.md) <br>
- [Einstein x402 Payment Guide](references/payment-guide.md) <br>
- [Einstein x402 Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and service-response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Paid queries may return structured data or AI-generated analysis; use requires Node.js, curl, and an Einstein x402 private key for USDC payments on Base.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
