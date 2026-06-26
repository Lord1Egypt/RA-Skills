## Description: <br>
Gate Flash Swap Skill helps an agent preview, execute, and verify Gate flash swaps across one-to-one, one-to-many, and many-to-one cryptocurrency conversions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to manage Gate flash swap workflows, including quote previews, swap execution after confirmation or explicit one-click requests, supported-pair checks, and order status review. <br>

### Deployment Geography for Use: <br>
Global, subject to Gate regional availability and compliance restrictions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to execute real cryptocurrency trades through Gate flash swap write tools. <br>
Mitigation: Use a narrowly scoped Gate authorization, review quote previews and amounts before execution, and reserve one-click or direct swap wording for cases where immediate execution is intended. <br>
Risk: Requests such as convert all or sweep balances may inspect holdings and convert full eligible balances. <br>
Mitigation: Confirm the asset list, full-balance intent, and previewed amounts before creating orders; avoid broad sweep wording when only a partial conversion is desired. <br>
Risk: The skill depends on an external runtime-rules document whose behavior can change outside this reviewed package. <br>
Mitigation: Review the linked runtime rules before installation and before high-value use, and re-check them when the skill or Gate MCP setup changes. <br>


## Reference(s): <br>
- [MCP Execution Specification](references/mcp.md) <br>
- [Flash Swap Scenarios](references/scenarios.md) <br>
- [Gate Runtime Rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>
- [Gate MCP Setup](https://github.com/gateio/gate-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown summaries and tables with MCP tool call guidance and results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke authenticated Gate MCP read and write tools; swap outputs include quotes, confirmation prompts, order IDs, status, and error details.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence; artifact frontmatter: 2026.3.23-1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
