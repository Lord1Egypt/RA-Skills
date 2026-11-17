## Description:

Turn Amazon inventory data into a prioritized operating plan for stockout recovery, restocking, inventory pacing, or overstock clearance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techterrydev](https://clawhub.ai/user/techterrydev)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and operators use this skill to convert inventory, sales velocity, inbound timing, and margin constraints into a prioritized stockout recovery, replenishment, pacing, or overstock action plan. It supports planning and review, not automatic account changes or purchase commitments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat purchase, pricing, promotion, advertising, liquidation, disposal, tax, compliance, or account-change recommendations as approved actions.

Mitigation: Require human review and current official account or documentation verification before executing any operational change.

Risk: Inventory and sales inputs may include sensitive account, product, or business details.

Mitigation: Use redacted product labels and provide only the inventory and sales context needed for planning; avoid credentials, unnecessary account identifiers, and unredacted sensitive details.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/TechTerryDev/amazon-seller-skills/tree/main/skills/amazon-inventory-action-plan)
- [AMZ Helper project](https://amzhelper.com)
- [ClawHub skill page](https://clawhub.ai/techterrydev/skills/amazon-inventory-action-plan)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown inventory action plan with tables and review checkpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scenario-based planning output; account actions require human review before execution.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
