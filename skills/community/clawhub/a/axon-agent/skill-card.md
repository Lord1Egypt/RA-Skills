## Description: <br>
Register, monitor, and maintain AI Agents on the Axon blockchain, including registration, status checks, heartbeat daemon setup, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[6tizer](https://clawhub.ai/user/6tizer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to register an EVM wallet as an Axon on-chain Agent, check agent status, run the heartbeat daemon, and troubleshoot registration or heartbeat failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a private key file to submit Axon registration transactions and operate a heartbeat daemon. <br>
Mitigation: Use a dedicated low-balance wallet, keep the private key outside shared repositories with restrictive file permissions, and run the dry run before submitting a transaction. <br>
Risk: Registration and daemon setup depend on the intended Axon chain, RPC endpoint, registry contract, and external daemon source. <br>
Mitigation: Verify the chain ID, RPC endpoint, registry address, and daemon source before giving the daemon access to a wallet key. <br>
Risk: The watchdog cron can restart the daemon repeatedly after deployment. <br>
Mitigation: Confirm the daemon command and log paths before enabling cron, and document how to stop the daemon and remove the watchdog entry. <br>


## Reference(s): <br>
- [Axon official repository](https://github.com/axon-chain/axon) <br>
- [Axon SDK Known Issues & Gotchas](references/known-issues.md) <br>
- [Axon Agent on ClawHub](https://clawhub.ai/6tizer/axon-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that read a private key file, submit on-chain transactions, build an external daemon, and configure cron.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
