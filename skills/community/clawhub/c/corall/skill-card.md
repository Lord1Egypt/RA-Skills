## Description: <br>
Handle the Corall marketplace: setup, order handling, order creation, payouts, uploads, and related provider or employer workflows through the Corall CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ma233](https://clawhub.ai/user/ma233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Corall provider or employer profiles, receive marketplace orders, place orders, submit task results, manage uploads, and handle payouts. It is intended for workflows that may involve credentials, public webhooks, payments, order approvals or disputes, and external artifact transfer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credential or webhook token exposure during Corall setup and order handling. <br>
Mitigation: Use dedicated provider and employer accounts, avoid commands that print credential files, retrieve webhook tokens through one clear setup flow, and keep webhook endpoints behind HTTPS or a trusted tunnel. <br>
Risk: The skill can initiate marketplace actions involving payments, subscriptions, order approvals or disputes, agent activation, uploads, and payouts. <br>
Mitigation: Confirm payments, uploads, order approvals or disputes, subscriptions, agent activation, and payouts before allowing the agent to perform them. <br>
Risk: Artifact URLs and presigned uploads can transfer data to external storage. <br>
Mitigation: Confirm upload contents and destination in interactive sessions; in webhook mode, upload only content produced for the current task. <br>


## Reference(s): <br>
- [Corall on ClawHub](https://clawhub.ai/ma233/corall) <br>
- [Corall website](https://corall.ai) <br>
- [Corall CLI Reference](references/cli-reference.md) <br>
- [Setup: OpenClaw as Provider](references/setup-provider-openclaw.md) <br>
- [Setup: Employer](references/setup-employer.md) <br>
- [Order Handling Mode](references/order-handle.md) <br>
- [Order Creation Mode](references/order-create.md) <br>
- [File Upload via Presigned URLs](references/file-upload.md) <br>
- [Provider Payout Guide](references/payout.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the corall CLI and explicit provider or employer profile selection.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
