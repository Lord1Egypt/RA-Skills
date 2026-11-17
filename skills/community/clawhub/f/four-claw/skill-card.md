## Description:

Launch custom tokens on Solana (BAGS) or BNB Chain (FLAP) through the FourClaw API with configurable tax and revenue-sharing options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fourclawteam](https://clawhub.ai/user/fourclawteam)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to submit FourClaw token-launch requests and check launch status for Solana BAGS or BNB Chain FLAP tokens. It is intended for workflows where wallet, chain, token metadata, tax, and recipient settings can be reviewed before submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can submit live token-launch requests through an unauthenticated API flow.

Mitigation: Require manual confirmation before any POST and verify wallet ownership, chain, symbol, recipient splits, tax settings, and public profile fields.

Risk: Rate limits are tied to agentId values and can be weakened if identifiers are rotated.

Mitigation: Use stable agentId values per app or agent and do not rotate them to bypass rate limits.

Risk: Token metadata, social links, and gift-vault handles may publish user-provided information or direct funds to unintended recipients.

Mitigation: Review description, image URL, website, X/Twitter, Telegram, recipient, and xHandle fields before launch.

## Reference(s):

- [FourClawFun ClawHub skill page](https://clawhub.ai/fourclawteam/skills/four-claw)
- [FourClaw API documentation](https://fourclaw.fun/fourclaw/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown documentation with JSON examples and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes request parameters, response shapes, rate-limit guidance, and status-checking examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
