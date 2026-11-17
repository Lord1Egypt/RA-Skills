## Description:

Compare public Patreon membership tiers and Substack subscription plans through Crawlora, preserving published benefits, pricing, billing terms, and offer availability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, analysts, and prospective subscribers compare public Patreon and Substack offers against content interests, benefits, budget, currency, and billing preferences without subscribing or changing accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Crawlora API key is required for public Patreon and Substack lookups.

Mitigation: Set the key knowingly and limit lookups to the intended creator or publication scope.

Risk: Published benefits and prices may be mistaken for verified entitlements, delivery quality, or a personalized checkout total.

Mitigation: Label offers as public published data, preserve currency and billing terms, and flag unknown or disabled plans rather than assuming purchase availability.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/creator-membership-comparison)
- [Supported Crawlora endpoints](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands]

**Output Format:** [Markdown comparison matrices and prose with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes offer identity, published benefits, billing and currency basis, availability, evidence gaps, and fit tradeoffs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
