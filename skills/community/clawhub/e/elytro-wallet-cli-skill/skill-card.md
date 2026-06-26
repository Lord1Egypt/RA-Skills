## Description: <br>
The Elytro skill pack gives agents instructions for using the Elytro ERC-4337 smart-account CLI, routing DeFi intents, executing Uniswap-planned transactions, and running approved payroll workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[walkjoi](https://clawhub.ai/user/walkjoi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and wallet operators use this skill pack to let agents manage Elytro smart accounts, gather DeFi planner outputs, simulate transactions, request approval, and execute approved wallet, recovery, paid request, or payroll actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic update instructions may replace local wallet guidance before use. <br>
Mitigation: Disable or ignore automatic SKILL.md and CLI update behavior unless updates are pinned, fetched from a trusted source, and reviewed before use. <br>
Risk: The skill can guide transactions, approvals, paid requests, recovery changes, OTP submission, and payroll payouts. <br>
Mitigation: Require simulation output and explicit human confirmation before any send, paid request, security change, recovery action, OTP submission, or payroll payout. <br>


## Reference(s): <br>
- [Elytro command reference and consent list](elytro/references/commands.md) <br>
- [Elytro homepage](https://elytro.com) <br>
- [Uniswap AI](https://github.com/Uniswap/uniswap-ai) <br>
- [Elytro Recovery App](https://recovery.elytro.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and command-result response templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes safety gates for simulation, approval, OTP, recovery, paid request, and payroll workflows.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata; artifact package.json reports 2.0.0 and elytro/SKILL.md reports 0.7.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
