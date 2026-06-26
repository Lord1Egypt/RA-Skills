## Description: <br>
Gate spot trading and account operations skill for spot buy and sell actions, account value checks, order management, and conditional or trigger orders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaixianggeng](https://clawhub.ai/user/gaixianggeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent assist with Gate spot trading workflows, including balance checks, market and limit order drafting, trigger orders, amendments, cancellations, and fill verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate with write-capable Gate spot exchange credentials and may place, amend, or cancel real orders. <br>
Mitigation: Use a limited API key with no withdrawal permission and require clear confirmation for every order, trigger order, amendment, and cancellation. <br>
Risk: The skill delegates runtime rules to an unpinned remote file. <br>
Mitigation: Inspect or pin the remote runtime-rules file before deployment and verify the publisher and MCP server independently. <br>


## Reference(s): <br>
- [MCP execution specification](references/mcp.md) <br>
- [Trading scenarios](references/scenarios.md) <br>
- [ClawHub skill page](https://clawhub.ai/gaixianggeng/gaixianggeng-gate-exchange-spot-demo-20260402) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with order drafts, status summaries, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before write-capable trading actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
