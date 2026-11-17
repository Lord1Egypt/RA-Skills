## Description:

Pay for anything with USDC using virtual cards for online checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawallex-tech](https://clawhub.ai/user/clawallex-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to set up Clawallex access, check USDC wallet and card state, create virtual cards for one-time or subscription payments, and guide checkout flows without exposing card secrets in chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate payment-card creation and uses high-value Clawallex credentials.

Mitigation: Use a dedicated, low-limit Clawallex API key, check wallet balance before payment, and confirm amount and description with the user before creating a card.

Risk: Secrets can be exposed through chat transcripts or command-line history.

Mitigation: Avoid entering API keys or secrets directly into chat or shell history, and rotate keys if they may have been logged.

Risk: Production credentials could be sent to an unsafe endpoint if a custom or HTTP base URL is used.

Mitigation: Do not use custom or HTTP base URLs with production credentials.

Risk: Stored credentials and card-sensitive data require careful local handling.

Mitigation: Keep ~/.clawallex credential files protected or remove them when no longer needed, and never display PAN or CVV values to the user.

## Reference(s):

- [Clawallex Skill on ClawHub](https://clawhub.ai/clawallex-tech/skills/clawallex)
- [Clawallex Dashboard Settings](https://app.clawallex.com/dashboard/settings)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON command results with concise Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require Python 3.9+ and a configured Clawallex account or signup flow; payment actions should be confirmed before execution.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
