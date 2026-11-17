## Description:

Handles HTTP 402 Payment Required responses for A402 buyer payments by parsing the Payment-Needed bill, invoking the alipay-bot CLI to initiate payment, retrying the protected request with payment proof, and sending a fulfillment acknowledgement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yun520-1](https://clawhub.ai/user/yun520-1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an HTTP request returns 402 Payment Required and an agent needs to guide the buyer-side Alipay/A402 payment flow. It supports wallet checks, payment submission, status querying, protected resource retry, and fulfillment acknowledgement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and executes an external npm package in a payment workflow.

Mitigation: Review the package source and integrity before installation, install only the pinned package version, and proceed only when the user trusts the package and merchants involved.

Risk: The retry flow may operate on untrusted or user-supplied resource URLs.

Mitigation: Enforce strict HTTPS URL validation and safe argument handling before running payment status or retry commands.

Risk: Problem feedback could include secrets, payment details, or unnecessary personal data.

Mitigation: Show the feedback payload to the user for confirmation and omit secrets or personal data that are not required for troubleshooting.

Risk: Payment links and QR code references are sensitive to exposure and may be user-bound.

Mitigation: Display payment links only through user-approved channels and avoid writing them to persistent logs or caches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/alipay-pay-for-402-service)
- [OpenClaw homepage](https://github.com/alipay/payment-skills)
- [alipay-bot npm package](https://www.npmjs.com/package/@alipay/agent-payment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and direct CLI output forwarding]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm and alipay-bot; payment links, QR MEDIA lines, and purchased resource responses are expected to be passed through without alteration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter: 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
