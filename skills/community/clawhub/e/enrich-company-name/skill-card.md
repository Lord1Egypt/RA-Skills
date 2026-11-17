## Description:

Populate missing contact company name fields from associated company records using a HubSpot workflow with optional API backfill for CRM segmentation, personalization, and ICP classification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

CRM operators, marketing operations teams, and developers use this skill to audit HubSpot contacts missing company names, copy associated company names into contact records, and verify enrichment results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable ongoing and bulk HubSpot CRM changes that may affect contact records at scale.

Mitigation: Use a least-privilege HubSpot token, test on a sandbox or small segment first, export affected contact and company fields before bulk changes, and define rollback or cleanup steps before enrolling the full backlog.

Risk: Audit scripts can retrieve contact PII fields while measuring enrichment coverage.

Mitigation: Remove unnecessary contact PII fields from the audit scripts and retain only the fields needed for before and after validation.

Risk: Duplicate or incorrect company associations can copy the wrong primary company name to a contact.

Mitigation: Confirm duplicate and auto-association settings before activation, then spot-check enriched contacts and workflow history after processing.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python audit scripts and HubSpot workflow configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce CSV audit files when the included before and after scripts are run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
