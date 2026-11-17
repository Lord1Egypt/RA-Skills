## Description:

Choose and order food with learned preferences, price comparison, and variety protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to help an agent choose food, compare delivery options, apply preferences and restrictions, and place food orders after explicit confirmation. It also supports household/group ordering, local preference memory, price comparison, and post-order notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores dietary, allergy, household, budget, restaurant, and order-history notes locally.

Mitigation: Create ~/food-delivery with owner-only permissions, avoid storing unnecessary medical or religious detail, use aliases for household members, and delete stale notes.

Risk: The skill can use logged-in delivery apps and place paid food orders.

Mitigation: Require explicit user confirmation before checkout, review delivery address and total, and keep payment methods and credentials managed only inside the user's delivery apps.

Risk: Incorrect handling of allergies or firm dietary restrictions could lead to unsafe or unacceptable orders.

Mitigation: Treat critical restrictions as hard filters, add allergy notes to every relevant order, and verify restaurant accommodation before ordering.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/food-delivery)
- [Decision Framework](artifact/decisions.md)
- [Memory Setup](artifact/memory-template.md)
- [Ordering Workflow](artifact/ordering.md)
- [Common Traps](artifact/traps.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured ordering checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local notes under ~/food-delivery/ and may guide browser-based checkout only after explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
