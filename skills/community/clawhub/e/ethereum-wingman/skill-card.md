## Description:

Ethereum Wingman guides agents through Scaffold-ETH 2 project creation, Solidity development, DeFi protocol patterns, security gotchas, and fork-mode testing against real protocol state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jp4g](https://clawhub.ai/user/jp4g)

### License/Terms of Use:

MIT

## Use Case:

Developers and coding agents use this skill to build, test, and review Ethereum dApps with Scaffold-ETH 2, Solidity, and common DeFi integrations. It is especially suited for workflows that need forked network state, smart contract safety checks, and practical Ethereum development guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to run mutable remote setup code, including project scaffolding through create-eth.

Mitigation: Review before installing, pin or manually verify create-eth before use, and run project generation in a clean workspace without wallet secrets or publishing tokens.

Risk: Cursor setup can persist this skill's AGENTS.md as .cursorrules in the current project.

Mitigation: Use the Cursor setup only in intended Ethereum workspaces and remove or replace the .cursorrules symlink when the project should no longer inherit this guidance.

Risk: The skill is specialized for Ethereum and Scaffold-ETH 2 workflows and may be inappropriate outside that scope.

Mitigation: Use it only for Ethereum or Scaffold-ETH 2 work and review generated smart contract guidance before applying it to production code.

## Reference(s):

- [Ethereum Wingman ClawHub Page](https://clawhub.ai/jp4g/skills/ethereum-wingman)
- [Automation, Incentives & Keepers](references/automation-and-incentives.md)
- [Critical Ethereum Development Gotchas](references/critical-gotchas.md)
- [Historical Hacks: Teachable Moments](references/historical-hacks.md)
- [SpeedRun Ethereum](https://speedrunethereum.com/)
- [Scaffold-ETH](https://scaffoldeth.io/)
- [Scaffold-ETH Documentation](https://docs.scaffoldeth.io/)
- [OpenZeppelin Documentation](https://docs.openzeppelin.com/)
- [Uniswap Documentation](https://docs.uniswap.org/)
- [Aave Documentation](https://docs.aave.com/)
- [Chainlink Documentation](https://docs.chain.link/)
- [Rekt Leaderboard](https://rekt.news/leaderboard/)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown responses with inline code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Scaffold-ETH setup commands, Solidity and TypeScript examples, configuration edits, and review checklists that require developer review before execution.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
