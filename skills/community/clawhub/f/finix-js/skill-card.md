## Description:

Finix.js integration for accepting card and ACH bank payments on the web.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jbryant](https://clawhub.ai/user/jbryant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add Finix-hosted card and ACH payment collection to web checkout flows and connect browser tokenization with server-side Finix API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Finix credentials or sandbox credential examples may be copied into browser code, logs, shell history, CI output, or command lines.

Mitigation: Use sandbox examples only for local testing, keep live credentials server-side, and store production secrets in a secret manager or protected configuration.

Risk: Payment-flow examples can affect live card or ACH processing if copied directly into production without merchant-specific review.

Mitigation: Test with sandbox Application and Merchant IDs first, then review environment, amount, credential, and fraud-session handling before switching to live Finix endpoints.

## Reference(s):

- [Finix homepage](https://finix.com)
- [Finix.js tokenization guide](https://docs.finix.com/guides/online-payments/payment-tokenization/tokenization-forms)
- [Create an Identity](https://docs.finix.com/api/identities/createidentity)
- [Create a Payment Instrument](https://docs.finix.com/api/payment-instruments/createpaymentinstrument)
- [Create a Transfer](https://docs.finix.com/api/transfers/createtransfer)
- [Create an Authorization](https://docs.finix.com/api/authorizations/createauthorization)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces integration guidance rather than executable skill code; examples require merchant-specific Finix identifiers and server-side credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
