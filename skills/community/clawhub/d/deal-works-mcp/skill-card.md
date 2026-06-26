## Description: <br>
AI agent infrastructure for deals, escrow, attestations, and autonomous agents. 39 tools across 9 engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swgoettelman](https://clawhub.ai/user/swgoettelman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this MCP server to let agents create and manage deal workflows, escrow funding, attestations, disputes, marketplace listings, and autonomous agent deployments on deal.works. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent direct authority over funds, deals, marketplace posts, disputes, attestations, and remote agents. <br>
Mitigation: Use the least-privileged API key available, enforce budget limits outside the skill, and require explicit human confirmation before transfers, cashouts, escrow funding, deal actions, dispute votes, final seals, marketplace publishing, or agent deployment. <br>
Risk: Security evidence notes no clear confirmation guardrails for high-impact operations. <br>
Mitigation: Configure the hosting agent or MCP client to gate mutating tools with approval policies before deployment. <br>
Risk: The release depends on trust in deal.works and the published npm package scope. <br>
Mitigation: Install only when deal.works is trusted for the workflow and verify the npm package scope before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swgoettelman/deal-works-mcp) <br>
- [deal.works homepage](https://deal.works) <br>
- [deal.works documentation](https://docs.deal.works) <br>
- [npm package](https://www.npmjs.com/package/@swgoettelman/deal-works-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Configuration, Guidance] <br>
**Output Format:** [JSON text returned by MCP tools and resources, with plain-text prompt guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and DEAL_WORKS_API_KEY; high-impact tool calls can affect deals, funds, disputes, attestations, marketplace listings, and deployed agents.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
