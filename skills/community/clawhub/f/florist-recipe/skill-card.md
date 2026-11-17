## Description:

Generate executable florist recipes (flower formula, stem counts, budget breakdown, substitutions, assembly steps, care) from a natural-language occasion, budget, and style request. This skill should be used when a user asks to design a bouquet or vase arrangement, wants to know how many stems to buy for a given budget, needs a shopping list for a flower market, needs to substitute an out-of-stock flower while keeping the design intent, or asks for step-by-step assembly and care instructions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junci003](https://clawhub.ai/user/junci003)

### License/Terms of Use:

MIT-0

## Use Case:

External flower shoppers and florists use this skill to turn an occasion, style, and budget into a practical bouquet or vase arrangement plan, including a shopping list, substitutions, assembly steps, and care guidance.

### Deployment Geography for Use:

Global; price references are based on first-tier Chinese city flower markets and should be localized.

## Known Risks and Mitigations:

Risk: Pet-safety advice in the flower reference may be inaccurate: the security guidance notes that carnations and ranunculus are listed as relatively safe there, while ASPCA identifies both as toxic to cats and dogs.

Mitigation: Verify each flower against a current veterinary or poison-control source before recommending an arrangement for a home with pets; avoid carnations and ranunculus when pet safety is uncertain.

Risk: Flower prices, seasonal availability, and vase-life estimates vary by location and conditions.

Mitigation: Present prices and vase life as reference ranges, state that local conditions govern, and confirm availability and pricing with the user's market.

## Reference(s):

- [Flower library](artifact/references/flower-library.md)
- [Arrangement constraints](artifact/references/constraints.md)
- [Recipe output schema](artifact/references/output-schema.md)
- [Image prompt guidance](artifact/references/image-prompt.md)
- [ClawHub release page](https://clawhub.ai/junci003/skills/florist-recipe)
- [ASPCA Carnation guidance](https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/carnation)
- [ASPCA Buttercup (Ranunculus) guidance](https://www.aspca.org/pet-care/aspca-poison-control/toxic-and-non-toxic-plants/buttercup)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Structured JSON recipe with a Markdown shopping list, assembly steps, care guidance, and a constrained image prompt.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Price, season, and vase-life figures are estimates; the skill instructs users to verify local market conditions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
