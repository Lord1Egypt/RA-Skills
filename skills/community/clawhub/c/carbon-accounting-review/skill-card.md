## Description:

Review GHG inventories, carbon disclosures and PCF methods; trace evidence, flag double counting and state assurance limits. 碳盤查／碳揭露審閱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[simon5530](https://clawhub.ai/user/simon5530)

### License/Terms of Use:

MIT-0

## Use Case:

Sustainability teams, consultants and analysts use the skill to review authorized GHG inventory and disclosure evidence, identify calculation and evidence gaps, and prepare an actionable report. Product teams and developers can use it to screen product-footprint and carbon-software methods, with findings left for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One scanner reported an error, so the available scan evidence is incomplete despite the benign verdict.

Mitigation: Review the scanner limitation and inspect relevant package files before relying on the scan result.

Risk: The host or model provider may process supplied carbon data remotely.

Mitigation: Use only authorized, appropriately de-identified material and check the host provider’s privacy and retention terms before sharing confidential data.

Risk: A model may misread tables, invent standards clauses or miscalculate consequential figures; this workflow is not assurance or certification.

Mitigation: Verify important calculations and source claims independently, and have a qualified human review consequential conclusions.

## Reference(s):

- [GHG Protocol Corporate Standard](https://ghgprotocol.org/corporate-standard)
- [GHG Protocol Scope 2 Guidance](https://ghgprotocol.org/scope-2-guidance)
- [GHG Protocol Scope 3 Standard](https://ghgprotocol.org/corporate-value-chain-scope-3-standard)
- [GHG Protocol Product Standard](https://ghgprotocol.org/product-standard)
- [Authority and evidence guide](artifact/references/sources.md)
- [PCF and carbon-software method review](artifact/references/method-review.md)
- [Public-disclosure review](artifact/references/public-disclosures.md)
- [Review report template](artifact/templates/review-report.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report with evidence locators, finding statuses, calculations, limitations and prioritized actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scope-bounded findings; missing or unreadable evidence remains not assessable. Human review is required for consequential conclusions.]

## Skill Version(s):

1.0.0 (source: changelog, released 2026-11-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
