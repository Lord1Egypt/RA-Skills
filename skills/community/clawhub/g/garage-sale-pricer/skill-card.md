## Description:

Use when preparing a garage/yard/tag sale — pricing items, building the inventory with printable price tags, planning change float, signage, timing, and routing leftovers to donation/consignment/curb. Encodes what garage-sale items actually sell for (furniture 10-15% of retail, clothes $1-5) with condition multipliers and day-2 half-off ladders, so sellers stop guessing and buyers stop lowballing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT-0

## Use Case:

Homeowners and other sellers can use this skill to prepare a garage, yard, moving, or estate sale. It helps price inventory, prepare tags, plan cash and sale-day logistics, and decide how to route unsold items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is benign but has medium confidence; one script received only partial static analysis.

Mitigation: Review the script before use, including how it reads and writes the local inventory file.

Risk: The pricing and sale-day guidance may not match local market conditions or sign and safety rules.

Mitigation: Check local rules and verify item-specific prices and safety recalls before following the recommendations.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/voronindenis5/skills/garage-sale-pricer)
- [Publisher profile](https://clawhub.ai/user/voronindenis5)
- [Price Bands](references/price-bands.md)
- [Sale-Day Playbook](references/sale-day-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, JSON]

**Output Format:** [Structured pricing and sale-planning guidance, printable price-tag text, and a local JSON inventory file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pricing estimates use USD and vary by category and item condition.]

## Skill Version(s):

1.0.0 (source: release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
