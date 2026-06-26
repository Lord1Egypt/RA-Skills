## Description: <br>
Gate LaunchPool staking and airdrop skill for browsing LaunchPool projects, staking or redeeming assets, and checking participation or reward records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Gate users use this skill to browse LaunchPool opportunities, stake or redeem assets after confirmation, and review pledge or airdrop reward history through Gate MCP tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use authenticated Gate access to stake or redeem funds. <br>
Mitigation: Use least-privilege API access, never paste API secrets into chat, and proceed only after the project, pool, coin, amount, and risk notes match the user's intent. <br>
Risk: The security summary flags mutable external runtime rules and under-scoped financial disclosures. <br>
Mitigation: Review the linked Gate MCP source and runtime-rules repository before installation, and keep stake or redeem flows behind explicit immediate confirmation. <br>


## Reference(s): <br>
- [LaunchPool project workflows](references/launch-projects.md) <br>
- [LaunchPool MCP specification](references/mcp.md) <br>
- [LaunchPool records workflows](references/records.md) <br>
- [Stake and redeem workflows](references/stake-redeem.md) <br>
- [Scenario index](references/scenarios.md) <br>
- [Gate API key management](https://www.gate.io/myaccount/profile/api-key/manage) <br>
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md) <br>
- [Gate website](https://www.gate.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown responses with tables, action previews, confirmation prompts, and result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated Gate MCP access for account-specific records and stake or redeem actions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
