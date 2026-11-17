## Description:

Entry point for the Elytro wallet skill and curated DeFi sub-skills that help agents operate Elytro ERC-4337 smart accounts with 2FA, spending limits, social recovery, transaction simulation, and user approval workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[walkjoi](https://clawhub.ai/user/walkjoi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external wallet operators use this skill pack to set up and manage Elytro smart accounts, run wallet queries, simulate and send transactions, coordinate DeFi planner output, and execute manually approved payroll or paid-request workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that the wallet skill can automatically replace and activate its own instructions from an unpinned remote branch before wallet operations.

Mitigation: Use a pinned and reviewed skill release, prevent automatic skill-file or CLI updates unless explicitly approved, and scan any updated instructions before wallet operations.

Risk: Wallet workflows can move funds, change security settings, submit OTPs, initiate recovery actions, revoke delegations, and make paid requests.

Mitigation: Require explicit human approval for each sensitive action and verify every transaction, delegation, recovery action, paid request, OTP, and payroll command before execution.

Risk: DeFi planner outputs may include incorrect calldata, unknown contracts, mismatched chains, or unsafe paymaster and UserOperation details.

Mitigation: Validate addresses, chain IDs, calldata, values, and UserOperation JSON; simulate before sending; reject unknown contracts or unreviewed paymasters without human approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/walkjoi/skills/elytro-wallet-cli-skill)
- [Elytro homepage](https://elytro.com)
- [Elytro command reference](elytro/references/commands.md)
- [Uniswap AI upstream](https://github.com/Uniswap/uniswap-ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown guidance with inline shell commands and structured wallet result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user approval before money movement, security changes, OTP submission, recovery writes, delegation revocation, updates, and paid requests.]

## Skill Version(s):

0.2.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
