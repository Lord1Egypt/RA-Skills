## Description: <br>
Rent and operate a no-KYC cloud VPS over MCP - pick a plan, deploy, get root SSH. Pay with crypto (USDC/USDT) or card. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[poiuyhje](https://clawhub.ai/user/poiuyhje) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use Eqvps to connect an agent to EQVPS's MCP service, check account state, fund a prepaid balance, choose VPS plans, deploy servers, retrieve SSH access details, and manage server lifecycle tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects the agent to a remote paid VPS service where funding an account, paying invoices, or ordering servers can spend money. <br>
Mitigation: Show prices, require explicit user confirmation before each paid action, and do not proceed until the user confirms funding or purchase intent. <br>
Risk: The workflow can expose EQVPS API tokens and root SSH credentials. <br>
Mitigation: Treat API tokens and root credentials as private secrets and avoid logging, reposting, or sharing them outside the user-facing handoff. <br>
Risk: The service is described as no-KYC VPS hosting, which may not fit every organization's procurement, compliance, or abuse-prevention requirements. <br>
Mitigation: Install and use the skill only when the organization accepts EQVPS as a paid no-KYC hosting provider. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/poiuyhje/eqvps) <br>
- [EQVPS homepage](https://eqvps.com) <br>
- [EQVPS MCP endpoint](https://mcp.eqvps.com/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration snippets and MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before paid actions; API tokens and root credentials must be treated as secrets.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
