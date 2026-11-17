## Description:

Create, manage, and publish ClawMart personas and skills directly from OpenClaw chat, including listing creation, package uploads, updates, and creator-account management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nateliason](https://clawhub.ai/user/nateliason)

### License/Terms of Use:


## Use Case:

ClawMart creators and agents use this skill to draft listing metadata, create or update persona and skill listings, upload package versions, and manage creator-account workflows through OpenClaw chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the skill gives an agent instructions for using a ClawMart API key to create and manage creator listings.

Mitigation: Install it only when agent-assisted listing management is intended, keep the API key private, and avoid exposing raw keys in chat output.

Risk: Publishing, updating, or deleting listings can affect a creator account and public ClawMart availability.

Mitigation: Review generated metadata and packages before upload, and require clear user confirmation before publishing, updating, or deleting listings.

Risk: Incorrect price formatting could create an unintended paid listing amount.

Mitigation: Validate payloads before API calls and send price values in dollars exactly as intended.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nateliason/skills/clawmart)
- [ClawMart API reference](https://www.shopclawmart.com/api/v1/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, API calls]

**Output Format:** [Markdown and plain text with JSON or API payload details when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include listing metadata drafts, generated skill or persona package content, API request plans, dashboard URLs, public URLs, and suggested fixes for failed requests.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
