## Description:

Reads bid or procurement evaluation rules, extracts pricing-score formulas, and helps agents produce user-confirmed JSON configurations for a local bid pricing calculator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Bid teams, procurement consultants, and evaluators use this skill to parse pricing-score rules from tender materials, confirm the interpretation, and generate calculator-ready JSON for scenario testing. It is intended for pricing-score analysis only, not full bid evaluation or guaranteed award decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported calculator configurations or CSV exports may mislead or attack users handling sensitive bid data.

Mitigation: Use only self-generated or trusted JSON, avoid opening exported CSVs with active spreadsheet features enabled, and prefer a fixed version that renders with textContent and safely encodes CSV fields.

Risk: Pricing recommendations may be wrong if tender text, screenshots, or OCR are misread.

Mitigation: Require user confirmation of the parsed formula before generating configuration JSON, and manually verify pricing formulas against the original tender document before making bid decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/bid-pricing-strategy-sandbox)
- [Formula knowledge base](artifact/formula-kb.md)
- [Demo output](artifact/demo-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with JSON configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured parsing summaries, calculator-ready JSON configurations, usage notes, and bid-pricing cautions; the bundled calculator can export CSV locally.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter and manifest report 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
