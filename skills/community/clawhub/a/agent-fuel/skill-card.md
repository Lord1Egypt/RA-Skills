## Description:

Autonomous agent wallet management with MoonPay auto top-up, x402 payments, and OpenWallet Standard. Agents never run out of gas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zedit42](https://clawhub.ai/user/zedit42)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to monitor wallet balances, trigger MoonPay top-ups, and handle x402 payments while applying spending limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic wallet top-ups and x402 payments can spend real funds if limits or approval controls are too broad.

Mitigation: Use a dedicated wallet with limited funds, disable autonomous top-up and x402 auto-pay until allowlists are configured, and require human approval above low thresholds.

Risk: Shell-based notification configuration can execute unintended commands.

Mitigation: Avoid the notifyCmd execution path unless it is fixed, reviewed, and restricted to a trusted command.

Risk: Dependency or CLI behavior changes can alter payment behavior.

Mitigation: Pin the MoonPay CLI version, review upgrades, and run the skill from a restricted account with scoped config, log, and state files.

## Reference(s):

- [Agent Fuel ClawHub Listing](https://clawhub.ai/zedit42/skills/agent-fuel)
- [MoonPay CLI](https://agents.moonpay.com)
- [x402 Protocol](https://x402.org)
- [OpenWallet Standard](https://github.com/nickatmpb/open-wallet-standard)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON configuration, and code-oriented guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces wallet automation instructions and command examples; execution should remain subject to human-approved spending limits.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
