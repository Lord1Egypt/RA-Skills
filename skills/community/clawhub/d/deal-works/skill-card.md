## Description: <br>
AI agent infrastructure for deals, escrow, attestations, and autonomous agents. 39 tools across 9 engines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swgoettelman](https://clawhub.ai/user/swgoettelman) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this MCP server to let agents manage deal workflows, escrow, wallet operations, attestations, dispute workflows, marketplace listings, and autonomous agent deployment through the deal.works platform. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes high-impact transfers, cash-outs, escrow changes, and agent funding actions. <br>
Mitigation: Constrain DEAL_WORKS_API_KEY to minimum necessary permissions and require human approval for recipients, amounts, wallet addresses, and deal IDs before execution. <br>
Risk: The skill can deploy and control autonomous agents. <br>
Mitigation: Treat agent deployment, funding, start, stop, restart, and scale operations as human-approved actions with explicit budget and permission review. <br>
Risk: Dispute filing, vault sealing, and attestation actions can affect deal records and governance workflows. <br>
Mitigation: Verify evidence, deal IDs, dispute details, and vault contents before allowing an agent to submit or seal records. <br>


## Reference(s): <br>
- [ClawHub Listing](https://clawhub.ai/swgoettelman/deal-works) <br>
- [deal.works](https://deal.works) <br>
- [deal.works Documentation](https://docs.deal.works) <br>
- [deal.works API Reference](https://docs.deal.works/api) <br>
- [npm Package](https://www.npmjs.com/package/@swgoettelman/deal-works-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON tool and resource results with Markdown prompts and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node and DEAL_WORKS_API_KEY; exposes MCP tools, resources, and prompts over stdio.] <br>

## Skill Version(s): <br>
0.1.1 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
