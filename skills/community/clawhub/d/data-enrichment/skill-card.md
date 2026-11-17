## Description:

Enrich company and contact lists with public data such as firmographics, technographics, social profiles, funding history, and employee count estimates, then clean, deduplicate, and score leads from raw CSV or JSON inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tktk-ai](https://clawhub.ai/user/tktk-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue, sales operations, and marketing teams use this skill to turn raw company names, domains, or contact lists into enriched, deduplicated, scored records for CRM import and lead prioritization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Contact enrichment can process personal data without a lawful basis or collect more fields than needed.

Mitigation: Use the skill only for legitimate business lead-enrichment workflows, confirm a lawful basis before processing contact data, and request only necessary fields.

Risk: Public-source enrichment can conflict with source terms or include sensitive personal data.

Mitigation: Respect source terms such as LinkedIn's and avoid collecting or storing sensitive personal data.

Risk: Enriched records may be incomplete, stale, or incorrect before CRM import.

Mitigation: Verify enriched records and confidence signals before importing or acting on the data.

## Reference(s):

- [Data Enrichment ClawHub Skill Page](https://clawhub.ai/tktk-ai/skills/data-enrichment)
- [Enrichment Field Definitions](references/field-definitions.md)
- [Default Lead Scoring Model](references/scoring-model.md)

## Skill Output:

**Output Type(s):** [text, markdown, CSV, JSON, guidance]

**Output Format:** [Markdown tables, CSV rows, JSON records, or CRM-compatible tabular exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lead scores, fit tags, source notes, and confidence fields; users should verify records before CRM import.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
