## Description: <br>
Installs and configures the DefiLlama MCP server so agents can access DeFi analytics for TVL, prices, yields, protocol metrics, stablecoins, bridges, ETFs, hacks, raises, and related data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reynardoew](https://clawhub.ai/user/reynardoew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to add DefiLlama's remote MCP server to supported agents, authenticate with OAuth, and verify access to DeFi analytics tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan flags guidance that tells an agent to install additional workflow skills without user confirmation. <br>
Mitigation: Review the source and explicitly approve any workflow-skill installation command before running it. <br>
Risk: OAuth callback URLs can act like temporary secrets if copied through chat or other shared channels. <br>
Mitigation: Prefer a local browser-based OAuth flow; when a headless flow is required, treat callback URLs as temporary secrets and avoid sharing them through chat apps. <br>
Risk: The skill connects an agent to DefiLlama MCP through OAuth and a subscription-backed external service. <br>
Mitigation: Install only when the user intends to connect DefiLlama MCP and understands the account, subscription, and token-storage requirements. <br>


## Reference(s): <br>
- [DefiLlama MCP server endpoint](https://mcp.defillama.com/mcp) <br>
- [DefiLlama subscription page](https://defillama.com/subscribe) <br>
- [ClawHub release page](https://clawhub.ai/reynardoew/defillama-setup) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OAuth setup guidance and MCP connection verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
