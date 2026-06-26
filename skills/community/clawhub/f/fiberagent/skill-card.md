## Description: <br>
FiberAgent helps OpenClaw agents search merchants for products, compare crypto cashback rates, calculate effective prices, and return tracked affiliate links for rewards on Monad. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openclawlaurent](https://clawhub.ai/user/openclawlaurent) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External agents and developers use FiberAgent to answer shopping, deal-finding, cashback, and product-comparison requests while routing purchases through crypto reward links. The skill is intended for agent-commerce workflows that need merchant search, cashback estimates, wallet registration, and earnings statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tracked affiliate links and wallet rewards can tie shopping activity to an agent wallet. <br>
Mitigation: Use a dedicated wallet when privacy matters and disclose to end users that purchases through returned links may be attributed for crypto rewards. <br>
Risk: Wallet registration could prompt users to share sensitive wallet material. <br>
Mitigation: Provide only public wallet addresses to the skill and never provide seed phrases or private keys. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openclawlaurent/fiberagent) <br>
- [FiberAgent Website](https://fiberagent.shop) <br>
- [FiberAgent API Docs](https://fiberagent.shop/api/docs) <br>
- [FiberAgent OpenAPI Spec](https://fiberagent.shop/server/openapi.json) <br>
- [FiberAgent Agent Card](https://fiberagent.shop/.well-known/agent-card.json) <br>
- [FiberAgent MCP Server](https://fiberagent.shop/api/mcp) <br>
- [FiberAgent ERC-8004 Profile](https://www.8004scan.io/agents/monad/135) <br>
- [FiberAgent Live Demo](https://fiberagent.shop/compare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, API calls, configuration, guidance] <br>
**Output Format:** [Markdown or structured tool results containing product listings, prices, cashback amounts, merchant details, affiliate URLs, registration responses, and agent statistics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tracked affiliate links and wallet-related crypto reward information.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
