## Description: <br>
Unofficial Bybit AI trading skill - trade on Bybit using natural language, covering spot, derivatives, earn, and more, with Bybit API credentials and explicit confirmation for real-money writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulyangby](https://clawhub.ai/user/paulyangby) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to let an AI assistant check Bybit market data, manage account information, and prepare or execute trading actions across supported Bybit products. It is intended for users who understand the financial risks of crypto trading and can provide scoped Bybit API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help perform real-money financial actions on a Bybit account. <br>
Mitigation: Start on testnet, use a dedicated limited-balance sub-account, and require explicit confirmation before any mainnet write operation. <br>
Risk: The skill requires sensitive Bybit API credentials. <br>
Mitigation: Store credentials in environment variables, grant only Read + Trade permissions, never enable withdrawals, and never paste secrets into a conversation. <br>
Risk: This is an unofficial community-maintained skill with no server-resolved source provenance for this version. <br>
Mitigation: Review the bundled files before installation and do not treat the package as official Bybit software unless the registry later shows a verified Bybit publisher or trusted source repository. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/paulyangby/bybit-trading-skill) <br>
- [Publisher Profile](https://clawhub.ai/user/paulyangby) <br>
- [Bybit](https://www.bybit.com) <br>
- [Bybit API Management](https://www.bybit.com/app/user/api-management) <br>
- [Bybit TradFi Integration Docs](https://bybit-exchange.github.io/docs/v5/tradfi-integration) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured confirmation cards, JSON examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Bybit API endpoints when credentials and user confirmation requirements are satisfied; simulated examples must be clearly labeled when live calls are unavailable.] <br>

## Skill Version(s): <br>
1.2.7 (source: server evidence, release metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
