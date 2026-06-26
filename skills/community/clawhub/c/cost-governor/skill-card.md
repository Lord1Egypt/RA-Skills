## Description: <br>
Tracks LLM API costs in real time, enforces budget limits with circuit breakers, and supports optional autonomous agent payments through the x402 protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AtlasPA](https://clawhub.ai/user/AtlasPA) <br>

### License/Terms of Use: <br>
MIT License <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor LLM provider spending, set budget limits, receive alerts, and pause activity when configured limits are exceeded. Operators may also use its x402 payment flow for optional Pro features when they have reviewed wallet funding and approval controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages agents to spend from funded wallets for Pro features. <br>
Mitigation: Use a separate low-balance wallet and require explicit human approval for each payment or renewal. <br>
Risk: Autonomous payment behavior may run without enough spending limits or operator review. <br>
Mitigation: Configure strict budget limits, confirm how to disable hooks and circuit breakers, and review the package/source code before running setup. <br>
Risk: Payment verification is described as trusting reported transaction hashes in the artifact documentation. <br>
Mitigation: Do not rely on the payment flow for high-value or unattended purchases until on-chain verification and approval controls are reviewed. <br>


## Reference(s): <br>
- [Cost Governor on ClawHub](https://clawhub.ai/AtlasPA/cost-governor) <br>
- [Project GitHub link from artifact documentation](https://github.com/AtlasPA/openclaw-cost-governor) <br>
- [x402 Protocol](https://www.x402.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, HTTP examples, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for cost tracking, local dashboard use, budget configuration, circuit-breaker reset, and optional payment setup.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
