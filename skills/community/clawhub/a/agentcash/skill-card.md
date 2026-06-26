## Description: <br>
Agentcash helps agents use wallet-authenticated, pay-per-call x402 and MPP APIs for service discovery, paid requests, and related provider workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maliot100x](https://clawhub.ai/user/maliot100x) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to discover payable service endpoints, check pricing and schemas, and run wallet-funded API calls for research, enrichment, media generation, communications, travel, jobs, and payment-provider workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through wallet-funded third-party API calls and purchases. <br>
Mitigation: Require explicit user confirmation before paid requests and check balance or pricing before expensive operations. <br>
Risk: The skill includes credential, registration, settlement, email, and phone workflows that can affect accounts or external parties. <br>
Mitigation: Require explicit confirmation before email or phone actions, service registration, payment settlement, adding new skills, or storing API keys. <br>
Risk: The authoritative scan summary flags broad paid-action authority and under-disclosed credential and payment-settlement workflows. <br>
Mitigation: Review carefully before installing and restrict use to agents that are allowed to make wallet-funded third-party API calls. <br>


## Reference(s): <br>
- [AgentCash homepage](https://agentcash.dev) <br>
- [ClawHub skill page](https://clawhub.ai/maliot100x/agentcash) <br>
- [Pump.fun Token Data Sources](references/pumpfun-data-sources.md) <br>
- [x402-Agent-Pay.com Reference](references/x402-agent-pay.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline bash, curl, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include paid API request instructions, wallet funding guidance, endpoint discovery steps, and credential handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
