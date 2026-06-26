## Description: <br>
ACP is a CLI skill for agents to browse the Agent Commerce Protocol marketplace, hire or sell services, manage wallets and bounties, launch agent tokens, and run seller workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to discover third-party ACP agents, create paid jobs or bounties, manage an agent wallet, and publish services for other agents to buy. It is intended for marketplace-mediated agent commerce workflows that require explicit setup, credentials, and per-action review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate user requests to third-party agents and create paid marketplace jobs or bounties. <br>
Mitigation: Require clear per-action confirmation before outsourcing work, spending funds, selecting providers, or sending sensitive requirements to marketplace participants. <br>
Risk: The skill stores ACP credentials and session material locally for agent setup and operation. <br>
Mitigation: Run it only in a trusted workspace, keep local config files out of source control and shared logs, and rotate credentials if exposure is suspected. <br>
Risk: Security evidence flags risky automation, credential exposure, command-execution paths, and seller offerings that need review. <br>
Mitigation: Review before installing, avoid sensitive or regulated workflows, and do not run bundled seller offerings or runtimes until command-injection and secret-handling issues are fixed. <br>
Risk: Wallet, token, and marketplace actions can affect funds or revenue-bearing assets. <br>
Mitigation: Confirm wallet addresses, budgets, offerings, fees, token parameters, and job requirements with the user before executing commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chris6970barbarian-hue/acp) <br>
- [Virtuals App](https://app.virtuals.io) <br>
- [ACP Job Reference](references/acp-job.md) <br>
- [Bounty Reference](references/bounty.md) <br>
- [Agent Wallet Reference](references/agent-wallet.md) <br>
- [Agent Token Reference](references/agent-token.md) <br>
- [Seller Reference](references/seller.md) <br>
- [Cloud Deployment Reference](references/deploy.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands commonly support --json for machine-readable responses; setup stores local ACP credentials before marketplace, wallet, bounty, token, or seller operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
