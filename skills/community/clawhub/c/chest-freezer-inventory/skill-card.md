## Description:

Tracks chest-freezer stock by layer and freeze date, recommends FIFO meals, flags quality aging, and summarizes inventory value and defrost needs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Households and bulk buyers use it to record frozen stock, find older items before shopping or meal planning, and plan retrieval and thawing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and update its JSON inventory file, and its activation triggers are broad.

Mitigation: Review the request before running inventory actions, use --store to select a dedicated file, and inspect changes afterward.

Risk: A quality-age verdict could be mistaken for a food-safety decision.

Mitigation: Use the age verdicts as quality guidance only and follow applicable food-safety guidance for handling and discard decisions.

## Reference(s):

- [Chest Freezer Inventory on ClawHub](https://clawhub.ai/voronindenis5/skills/chest-freezer-inventory)
- [Chest Freezer Inventory FIFO Model](artifact/references/freezer-fifo-model.md)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Plain-text inventory reports and a JSON inventory file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include a layer map, aging verdicts, FIFO meal and retrieval suggestions, and stock value summaries.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
