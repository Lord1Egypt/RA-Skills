## Description:

Register and operate an AI Agent on the Axon blockchain, including registration, on-chain status checks, heartbeat daemon setup, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[6tizer](https://clawhub.ai/user/6tizer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to register an EVM wallet as an Axon Agent, check balance and agent status, deploy heartbeat maintenance, and troubleshoot registration or daemon failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read wallet private keys from local files.

Mitigation: Use a dedicated low-funds wallet, prefer address-only status checks when possible, store the private-key file with restrictive permissions, and limit server access.

Risk: Real registration sends an irreversible on-chain transaction with AXON stake and burn economics.

Mitigation: Run the dry-run path first, verify the official Axon repository, RPC endpoint, chain ID, and dependency versions, and proceed only after accepting the permanent burn and stake lockup.

Risk: The daemon and watchdog introduce persistent background behavior through long-running processes and cron.

Mitigation: Review daemon and cron commands before installation, monitor logs after startup, and remove the cron entry or stop the daemon when heartbeat maintenance is no longer intended.

Risk: Axon precompile and SDK behavior is documented as inconsistent, which can affect status checks or registration simulation.

Mitigation: Use the included known-issues guide, verify chain ID 9001, and treat failed simulations or precompile reads as conditions requiring manual review before sending a real transaction.

## Reference(s):

- [Axon official repository](https://github.com/axon-chain/axon)
- [Axon SDK Known Issues & Gotchas](references/known-issues.md)
- [Axon Agent on ClawHub](https://clawhub.ai/6tizer/skills/axon-agent)
- [6tizer publisher profile](https://clawhub.ai/user/6tizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and Python/Bash script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead to on-chain transactions and persistent daemon or cron configuration.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
