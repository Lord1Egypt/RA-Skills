## Description:

Use BEFORE any payment or money-moving tool call. Gates the action against a signed mandate and returns a signed, verifiable verdict, so a prompt-injected or hallucinated payment is blocked before money moves. Non-custodial. A free account-owned API key activates the firewall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fidacy](https://clawhub.ai/user/fidacy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill before payment or other money-moving actions to check them against an active mandate and obtain signed allow/deny verdicts and audit evidence. It also provides setup guidance for Fidacy, whose payment protection requires an account-owned API key and executor-side grant validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mandatory gating may block unrelated tasks until the Fidacy account is activated.

Mitigation: Scope mandatory gating to explicitly selected payment tools and ensure missing activation cannot block unrelated work.

Risk: Without an account-owned API key, consequential payment decisions are denied; protection also depends on the executor validating grants.

Mitigation: Configure the key before use and require the payment executor to validate and enforce each signed grant before settlement.

Risk: Assessment or hosted operation may send action data to Fidacy.

Mitigation: Confirm what action data reaches Fidacy and review the external package version before enabling assessment or hosted operation.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/fidacy/skills/fidacy-payment-firewall)
- [Fidacy Public JWKS](https://api.fidacy.com/.well-known/jwks.json)
- [Fidacy Account Activation](https://app.fidacy.com/signup)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Markdown setup and workflow instructions with shell commands, JSON configuration examples, and structured tool verdicts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Payment protection requires an account-owned API key and executor-side grant validation.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
