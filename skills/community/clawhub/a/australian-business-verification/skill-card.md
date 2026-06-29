## Description: <br>
Verifies Australian businesses against the official Australian Business Register using an ABN, ACN, or business/entity name and returns registration status, GST status, entity type, location, and trading names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arbazex](https://clawhub.ai/user/arbazex) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, finance teams, and compliance reviewers use this skill to validate Australian suppliers, customers, invoices, GST status, and onboarding records against ABR data. It supports due-diligence workflows but should be treated as one verification signal rather than a fraud, payment, or legal determination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live lookups send the configured ABR GUID and the queried ABN, ACN, or business name to abr.business.gov.au. <br>
Mitigation: Obtain the GUID directly from ABR, store it only as ABR_GUID, and keep it out of chat, logs, and version control. <br>
Risk: ABR registration and GST status can support due diligence but do not determine fraud risk, payment safety, or legal compliance by themselves. <br>
Mitigation: Use lookup results alongside invoice review, identity checks, contractual records, and appropriate legal or compliance review before acting. <br>
Risk: Name searches can return multiple similar businesses, making an incorrect entity match possible. <br>
Mitigation: Present close matches for user confirmation and run a follow-up ABN lookup before treating one result as verified. <br>


## Reference(s): <br>
- [Australian Business Register](https://abr.business.gov.au) <br>
- [ABR Web Services](https://abr.business.gov.au/Tools/WebServices) <br>
- [ABR API Reference](reference/api-reference.md) <br>
- [ABR Entity Types](reference/entity-types.md) <br>
- [Sample Responses](examples/sample-responses.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Plain-language Markdown summaries with optional shell commands and JSON lookup results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ABR_GUID environment variable for live ABR lookups; local ABN and ACN checksum validation can run without an API call.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
