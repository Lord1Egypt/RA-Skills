## Description:

Give AI conversations a verifiable receipt by hashing messages into a tamper-evident chain, anchoring the digest through Fidacy, and providing a public verification link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fidacy](https://clawhub.ai/user/fidacy)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operators of customer-facing agents use this skill to create receipts for conversations involving refunds, claims, quotes, orders, scheduling, or other commitments that may later need verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external @fidacy/session npm SDK may change behavior or dependencies across releases.

Mitigation: Pin @fidacy/session to a reviewed version and install from a lockfile with npm ci.

Risk: Anchoring and gate calls may transmit operational data or metadata that matters for sensitive conversations.

Mitigation: Review what the SDK sends during anchoring and gate calls before using the skill with sensitive conversations.

Risk: The Fidacy gate becomes part of the business approval path for commitments such as refunds, claims, or quotes.

Mitigation: Use deny-by-default handling for non-approve verdicts and scope API keys narrowly for the required approval workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fidacy/skills/fidacy-conversation-receipts)
- [Fidacy receipt verification](https://fidacy.com/verify)
- [Fidacy API key signup](https://app.fidacy.com/signup)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline JavaScript and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to install and configure @fidacy/session, add receipt chaining, gate commitments, anchor sessions, and return verification links.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
