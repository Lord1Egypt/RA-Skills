## Description:

Use when building or debugging an agent (e.g. Telegram/WhatsApp bot, AI assistant) that integrates with the eSIMPal API to buy eSIMs for end-users, create orders, and deliver activation links, QR codes, or manual-install details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deniurchak](https://clawhub.ai/user/deniurchak)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build or debug bots and assistants that call the eSIMPal API to list plans, create orders, guide payment, activate eSIM packages, and deliver QR codes, activation links, or manual installation details to end users.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable base URL could expose the eSIMPal bearer key to an untrusted endpoint.

Mitigation: Use only the fixed eSIMPal API endpoint or a strictly allowlisted non-production endpoint with separate test credentials; do not forward Authorization headers across cross-origin redirects.

Risk: Order creation, payment, or activation can cause billable or irreversible user-facing actions.

Mitigation: Require explicit, action-specific user confirmation for order creation, payment, and activation endpoints; refuse execution when confirmation is absent.

Risk: API keys could be exposed through logs, transcripts, files, or overly broad credentials.

Mitigation: Load ESIMPAL_API_KEY from the runtime environment, avoid printing or persisting it, use least-privilege scopes, and rotate keys if exposure is suspected.

Risk: Hidden retries or incorrect idempotency keys could create duplicate orders or payment sessions.

Mitigation: Reuse the same idempotency key only for retrying the same request, use a new key only for a new confirmed action, and avoid hidden retries for billable operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deniurchak/skills/esimpal-api)
- [eSIMPal API Base URL](https://getesimpal.com/api)

## Skill Output:

**Output Type(s):** [guidance, code, configuration, API calls]

**Output Format:** [Markdown with API endpoint examples, JSON snippets, and integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ESIMPAL_API_KEY at runtime; billable and activation actions require explicit, action-specific user confirmation.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
