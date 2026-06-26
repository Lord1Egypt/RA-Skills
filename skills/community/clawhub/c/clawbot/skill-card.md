## Description: <br>
Credit line service for AI agents to access x402 services without upfront payment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goddieian47-boop](https://clawhub.ai/user/goddieian47-boop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to register agents for ClawCredit, check credit status, and route x402 service payments through an issued credit line after user consent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration requests broad agent data access for credit evaluation, including transcripts, prompts, and workspace context. <br>
Mitigation: Install and register only after explicit user consent and only when the user is comfortable sharing that agent context with ClawCredit and the external SDK. <br>
Risk: The skill stores a payment token for later API calls. <br>
Mitigation: Protect the saved credential file, avoid copying or logging tokens, and revoke or rotate the token if exposure is suspected. <br>
Risk: Recurring heartbeat or cron-style checks may continue after setup. <br>
Mitigation: Set payment budgets and stop monitoring jobs when ClawCredit pre-qualification or payment use is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goddieian47-boop/clawbot) <br>
- [X402 partner services registry](https://www.claw.credit/X402_PARTNER_SERVICES_REGISTRY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps, API-call patterns, credential handling guidance, consent requirements, and payment-risk cautions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
