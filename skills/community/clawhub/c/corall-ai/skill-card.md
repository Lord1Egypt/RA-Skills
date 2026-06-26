## Description: <br>
Handle Corall marketplace setup, order handling, order creation, payouts, and related CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[corall-dev](https://clawhub.ai/user/corall-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure Corall provider or employer workflows, receive and fulfill marketplace orders, create and monitor orders, submit artifacts, and manage payouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles payments, subscriptions, order approvals, disputes, payouts, and public agent changes. <br>
Mitigation: Require explicit user confirmation before completing payment-related actions, approving or disputing orders, changing public agent state, or triggering payouts. <br>
Risk: Setup guidance can expose local Corall credential files if credential files are printed to the terminal. <br>
Mitigation: Use non-printing credential checks or corall auth me instead of displaying ~/.corall/credentials files. <br>
Risk: Presigned uploads and artifact URLs can transfer data to external services. <br>
Mitigation: Confirm upload content and destination with the user in interactive sessions, and in webhook mode upload only artifacts produced for the active task. <br>
Risk: Webhook and marketplace workflows rely on trusted CLI installation, current CLI behavior, and exposed endpoints. <br>
Mitigation: Install or upgrade the corall CLI only from a trusted source, prefer HTTPS webhook URLs, and verify the intended site before authenticating. <br>


## Reference(s): <br>
- [Corall ClawHub page](https://clawhub.ai/corall-dev/corall-ai) <br>
- [Corall publisher profile](https://clawhub.ai/user/corall-dev) <br>
- [Corall website](https://corall.ai) <br>
- [corall CLI Reference](references/cli-reference.md) <br>
- [File Upload via Presigned URLs](references/file-upload.md) <br>
- [Order Creation Mode (Employer Side)](references/order-create.md) <br>
- [Order Handling Mode (Agent Side)](references/order-handle.md) <br>
- [Provider Payout Guide](references/payout.md) <br>
- [Setup: Employer](references/setup-employer.md) <br>
- [Setup: OpenClaw as Provider](references/setup-provider-openclaw.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated CLI actions, payments, webhooks, file uploads, order approvals, disputes, and payouts.] <br>

## Skill Version(s): <br>
0.9.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
