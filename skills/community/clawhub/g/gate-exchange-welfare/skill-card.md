## Description: <br>
Gate welfare center and new-user task skill that helps users check welfare rewards, new-user tasks, and benefit-claiming guidance using real Gate MCP data only. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and support agents use this skill to answer Gate welfare, rewards, and new-user task questions. It checks account eligibility first, then either returns real beginner task information or directs users to the Gate rewards hub, login, support, or the appropriate related skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vague rewards or task requests could trigger account-specific welfare checks unnecessarily. <br>
Mitigation: Confirm the user means Gate welfare or new-user tasks before account-specific lookup when the request is ambiguous. <br>
Risk: The skill requires a local Gate MCP setup with API credentials. <br>
Mitigation: Install only in trusted Gate MCP environments and use a dedicated least-privilege API key limited to Welfare:Read. <br>
Risk: Reward names, amounts, task status, or eligibility could be misleading if fabricated or not sourced from live task data. <br>
Mitigation: Use only real MCP-returned task fields, preserve identity-gate sequencing, and direct users to the official Gate website or app as the final authority. <br>


## Reference(s): <br>
- [Gate Welfare Runtime Rules](artifact/references/gate-runtime-rules.md) <br>
- [Gate Welfare MCP Specification](artifact/references/mcp.md) <br>
- [Proper MCP Data Usage Examples](artifact/references/mcp-data-usage.md) <br>
- [Gate Exchange Welfare Scenarios](artifact/references/scenarios.md) <br>
- [Gate Skills Homepage](https://github.com/gate/gate-skills) <br>
- [Gate Rewards Hub](https://www.gate.com/rewards_hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown task lists and short guidance messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Gate MCP read-only welfare identity and beginner task data; does not claim rewards or make account changes.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
