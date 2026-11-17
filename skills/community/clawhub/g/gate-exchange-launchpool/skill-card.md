## Description:

Gate LaunchPool staking and airdrop skill for browsing LaunchPool projects, staking or redeeming assets, and checking pledge or reward records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External Gate users and agent operators use this skill to browse LaunchPool opportunities, manage staking or redemption requests, and review LaunchPool participation and airdrop history through the Gate MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles authenticated staking and redemption actions.

Mitigation: Use a Gate API key with permissions you are comfortable granting and verify each stake or redeem preview before confirming.

Risk: The skill relies on mutable remote runtime rules.

Mitigation: Review before installing and prefer a release where shared runtime rules are bundled or pinned to an immutable commit.

## Reference(s):

- [Gate LaunchPool MCP Specification](references/mcp.md)
- [Gate LaunchPool Projects - Browse & Filter](references/launch-projects.md)
- [Gate LaunchPool Stake & Redeem - Participate and Withdraw](references/stake-redeem.md)
- [Gate LaunchPool Records - Pledge History & Reward History](references/records.md)
- [Gate Exchange LaunchPool Scenario Index](references/scenarios.md)
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)
- [Gate API key management](https://www.gate.io/myaccount/profile/api-key/manage)
- [Gate publisher website](https://www.gate.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown tables, action previews, confirmations, and concise status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stake and redeem actions require explicit user confirmation before execution.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
