## Description: <br>
Use when building or debugging an agent that integrates with the eSIMPal API to buy eSIMs for end-users, create orders, and deliver activation links, QR codes, or manual-install details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deniurchak](https://clawhub.ai/user/deniurchak) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to implement or test agents, bots, and assistants that guide eSIMPal order workflows, payments, activation, and delivery of eSIM installation details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through billable eSIM purchase, payment, or activation workflows. <br>
Mitigation: Require explicit action-specific user confirmation before order creation, payment, or activation, and refuse execution when confirmation is absent. <br>
Risk: An exposed eSIMPal API key could allow unauthorized order activity. <br>
Mitigation: Use sandbox or least-privilege keys where possible, keep ESIMPAL_API_KEY out of logs and stored files, and rotate keys if exposure is suspected. <br>
Risk: Retries with new idempotency keys could create duplicate billable actions. <br>
Mitigation: Reuse the same idempotency key only for retries of the same request and use a new key only for a new user-confirmed logical action. <br>
Risk: Activation actions may be irreversible or consume inventory. <br>
Mitigation: Ask the user to choose and confirm the activation path before calling new-profile or existing-profile activation endpoints. <br>


## Reference(s): <br>
- [eSIMPal API base URL](https://getesimpal.com/api) <br>
- [eSIMPal API example plans endpoint](https://getesimpal.com/api/v1/plans?country=TR&min_data_gb=1) <br>
- [ClawHub skill page](https://clawhub.ai/deniurchak/esimpal-api) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/deniurchak) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, API calls, markdown] <br>
**Output Format:** [Markdown guidance with code, command, configuration, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ESIMPAL_API_KEY at runtime and action-specific user confirmation before purchase, payment, or activation requests.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
