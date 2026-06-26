## Description: <br>
T54 provides guidance for using ClawCredit to register agents for credit, monitor qualification, and make x402 service payments through a credit line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rizaldii09](https://clawhub.ai/user/Rizaldii09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure ClawCredit SDK flows for x402 service access, credit qualification, repayments, and credential handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports broad private agent data collection and recurring uploads for credit evaluation. <br>
Mitigation: Install only in a dedicated low-sensitivity workspace, review what the SDK uploads and retains, and avoid exposing secrets in prompts or transcripts. <br>
Risk: The skill enables payment authority for x402 service calls through a credit line. <br>
Mitigation: Set explicit spend limits and approval rules before paid calls, and verify repayment status before continued use. <br>
Risk: The artifact describes heartbeat or cron-based monitoring behavior. <br>
Mitigation: Disable or closely monitor scheduled entries and keep the saved API token private. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Rizaldii09/firstt) <br>
- [X402 partner services registry](https://www.claw.credit/X402_PARTNER_SERVICES_REGISTRY.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes operational guidance for consent, credential storage, payment preflight checks, monitoring, and repayments.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
