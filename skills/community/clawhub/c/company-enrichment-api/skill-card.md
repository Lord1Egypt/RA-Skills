## Description:

Enrich a business website or Google Maps place ID into structured contact details, social profiles, and sourced owner information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and operations teams can enrich business leads from websites or Google Maps listings with published contact details and sourced owner information for CRM or spreadsheet workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enrichment calls use your API key with Scavio, and the skill also supports Google Maps search.

Mitigation: Review whether sending a business website or place ID to the external service is appropriate, and keep SCAVIO_API_KEY in an environment variable or secret store rather than source code.

## Reference(s):

- [Company Enrich documentation](https://scavio.dev/docs/company-enrich?utm_source=agent-skills&utm_medium=skill&utm_campaign=company-enrichment-api)
- [Company Enrich API endpoint](https://api.scavio.dev/api/v1/company/enrich)

## Skill Output:

**Output Type(s):** [JSON, Structured data]

**Output Format:** [Structured JSON with company contacts, social profiles, and sourced owner details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available fields depend on the source pages; owner information may be null, and owner email is included only when published on the site.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
