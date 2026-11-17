## Description:

A Mobile Elevating Work Platform workflow skill for equipment selection, preliminary engineering calculations, product intelligence, bid search, and bid-response drafting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangpf6698](https://clawhub.ai/user/yangpf6698)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineering or commercial teams use this skill to compare MEWP options, run preliminary stability, wind-load, motor, hydraulic, and cylinder calculations, gather product data, and prepare bid-response materials. Outputs are intended as engineering and business support, not as formal certification or qualified design approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preliminary calculations or equipment recommendations could be mistaken for safety certification or final engineering approval.

Mitigation: Verify manufacturer data, current standards, site conditions, and all safety-critical decisions with qualified professionals before use.

Risk: Recurring bid-monitoring automation could create repeated external searches or notifications without clear user intent.

Mitigation: Require explicit confirmation before enabling any recurring bid-monitoring automation.

Risk: Product specifications, pricing, ownership, and standards references can become outdated.

Mitigation: Cite source documents and retrieval dates, mark unverified values clearly, and re-check current manufacturer, standards, and official procurement sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangpf6698/skills/aerialwork)
- [Selection decision matrix](references/selection.md)
- [Standards and regulations reference](references/standards.md)
- [Product intelligence method](references/product-intel.md)
- [Bidding and bid-response guide](references/bidding.md)
- [Bid response template](assets/bid_response_template.csv)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with tables and inline shell commands; local calculation commands return plain-text formulas and results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses metric units and asks for missing site, load, height, platform, and bid inputs before producing recommendations or calculations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
