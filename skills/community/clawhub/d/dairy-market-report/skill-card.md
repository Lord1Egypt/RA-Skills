## Description:

Generates Chinese dairy market intelligence reports as magazine-style PDFs from monthly dairy industry PDFs, policy documents, structured market data, and GDT landed-cost calculations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robotbird](https://clawhub.ai/user/robotbird)

### License/Terms of Use:

MIT-0

## Use Case:

External users, market analysts, and dairy-industry teams use this skill to turn Chinese dairy market source documents into a structured monthly report covering prices, production, imports, exports, GDT results, landed-cost calculations, outlook, and policy or corporate events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted source documents or JSON data could affect report formatting or cause rendering failures.

Mitigation: Run the skill in a dedicated project folder, use pinned dependencies where possible, and review generated PDFs before distribution.

Risk: Market conclusions may be incomplete or misleading if the input PDFs or supporting data omit required figures.

Mitigation: Cross-check report values against the source documents and official data sources listed in the skill references; mark unavailable figures as data pending rather than filling gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robotbird/skills/dairy-market-report)
- [Publisher profile](https://clawhub.ai/user/robotbird)
- [Report template](artifact/references/report-template.md)
- [Report data schema](artifact/references/data-schema.md)
- [Data sources](artifact/references/data-sources.md)
- [GDT landed-cost formulas](artifact/references/gdt-formulas.md)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration]

**Output Format:** [Chinese-language PDF report, JSON report data, Markdown status text, and shell commands for extraction, calculation, and rendering.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single monthly report per period by default and expects source PDFs, DOCX files, or structured data to be reviewed for accuracy.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter lists 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
