## Description:

Use when users want to subscribe, pay, or manage Crypto Listing Alert notifications for exchange listing events and need Telegram, Discord, or email delivery with API-key login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xyz-ass](https://clawhub.ai/user/xyz-ass)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to manage Crypto Listing Alert subscriptions for Binance, OKX, Bybit, and Bitget listing notifications through Telegram, Discord, or email. It guides setup, payment order handling, subscription status checks, and cancellation through the bundled CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends reusable API keys, email or chat identifiers, and Telegram or Discord bot tokens to the listingalert.org backend.

Mitigation: Install only if the user trusts listingalert.org; use a dedicated bot token with minimal permissions for alert delivery.

Risk: Custom API URLs can redirect credentials and subscription data to an endpoint outside the normal service.

Mitigation: Avoid custom API URLs unless the user controls the endpoint, and do not use HTTP endpoints.

Risk: API keys or bot tokens may be exposed through command history, logs, or copied command examples.

Mitigation: Rotate any API key or bot token that may have been exposed, and avoid pasting long-lived credentials into shared logs.

## Reference(s):

- [Crypto Listing Alert service](https://listingalert.org)
- [ClawHub skill page](https://clawhub.ai/xyz-ass/skills/crypto-listing-alert)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-aware CLI result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses --json CLI output for structured command results; may include payment QR URLs returned by the service.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
