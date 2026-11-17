## Description:

Coupon query assistant that helps users find coupons, discounts, red packets, and product offers from a third-party coupon aggregation service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geraldalexanderrw](https://clawhub.ai/user/geraldalexanderrw)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to retrieve current platform coupons, food delivery red packets, and product-category offers. The skill is intended for coupon lookup and savings guidance, with results supplied by an external coupon aggregation service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a third-party coupon service and displays externally supplied coupon links.

Mitigation: Install only when the publisher is trusted, and validate returned links before users act on them.

Risk: The skill can run a local update path in response to upgrade-related chat input.

Mitigation: Avoid using the chat-triggered upgrade path; prefer a release that removes runtime self-updates.

Risk: The package includes shared service credentials.

Mitigation: Prefer a version that does not ship shared credentials and uses publisher- or user-managed credentials instead.

Risk: Cache data is handled in a shared temporary location.

Mitigation: Store cache data in a protected per-user location with appropriate permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geraldalexanderrw/skills/getcoupon)
- [ClawHub publisher profile](https://clawhub.ai/user/geraldalexanderrw)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text coupon summaries, platform lists, category matches, and externally supplied links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-sensitive discounts, app-opening instructions, fallback coupon text, and update guidance.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
