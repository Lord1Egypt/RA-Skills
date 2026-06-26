## Description: <br>
Backfills contact-level industry from associated company records using a HubSpot workflow so teams can segment targeted campaigns by ICP vertical. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomgranot](https://clawhub.ai/user/tomgranot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operations and CRM teams use this skill to copy company industry values onto associated HubSpot contacts and audit the before-and-after enrichment state for segmentation and campaign targeting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk HubSpot updates may place industry values into the wrong contact property or fail when dropdown values do not match. <br>
Mitigation: Verify the authoritative contact Industry property, confirm dropdown values match the company property exactly, and use a compatible text field when exact dropdown matching is uncertain. <br>
Risk: The audit scripts use a HubSpot access token and can read CRM records while writing local CSV audit files. <br>
Mitigation: Use a least-privilege HubSpot token, protect the local audit files, and keep the export or audit trail for review and rollback planning. <br>
Risk: A misconfigured workflow can update many contact records before the issue is noticed. <br>
Mitigation: Review the workflow criteria before activation, spot-check enriched contacts, inspect workflow history for failures, and compare before and after audit counts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tomgranot/enrich-industry) <br>
- [HubSpot API endpoint used by audit scripts](https://api.hubapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with Python code blocks and workflow setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional before and after CSV audit outputs when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
