## Description:

Assists with electronic component selection, second-source comparisons, and evidence-backed substitution and supply-chain risk reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hegions](https://clawhub.ai/user/hegions)

### License/Terms of Use:

MIT-0

## Use Case:

Hardware engineers, electronics distributors, and sourcing teams use this skill to compare candidate parts against datasheets, assess pin-to-pin and package compatibility, and flag lifecycle or sourcing risks before BOM review. Final qualification and substitution approval remain with the responsible engineer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive BOM, inventory, pricing, or transaction details could be disclosed in outward-facing reports.

Mitigation: Access internal records only with authorization and omit customer names, supplier names, internal prices, stock counts, and transaction details from shared output.

Risk: A proposed substitute could fail in the actual circuit or mechanical assembly.

Mitigation: Verify claims against current manufacturer documentation, flag missing evidence, and require responsible-engineer review and relevant testing before substitution.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hegions/skills/electronic-part-selection-advisor)
- [Selection rules](references/selection-rules.md)
- [Data sources](references/data-sources.md)
- [Semiconductor pin-to-pin judgment](references/pin-to-pin-judgment.md)
- [Connector pin-to-pin judgment](references/connector-pin-to-pin-judgment.md)
- [Power pin-to-pin judgment](references/power-pin-to-pin-judgment.md)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown reports and comparison tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source citations, uncertainty labels, and substitution caveats]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
