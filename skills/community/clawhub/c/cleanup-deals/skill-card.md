## Description:

Standardizes HubSpot deal pipelines, removes test deals, addresses missing amounts or close dates, and coordinates Salesforce-synced deal handling when applicable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Sales operations teams and CRM administrators use this skill to audit HubSpot deal quality, clean test or stale deals, standardize pipeline stages, and verify reporting accuracy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad deletion or pipeline changes can remove, misclassify, or distort production HubSpot deal records.

Mitigation: Use read-only access for the initial audit, export affected records and pipeline settings, require administrator approval for exact record and pipeline IDs, and prefer archive or quarantine over permanent deletion.

Risk: Changes to Salesforce-synced HubSpot deals can sync back to Salesforce and cause data loss.

Mitigation: Exclude records with Salesforce opportunity identifiers unless HubSpot and Salesforce administrators approve the change, and include Salesforce recycle-bin checks in rollback planning.

## Reference(s):

- [Cleanup Deals on ClawHub](https://clawhub.ai/tomgranot/skills/cleanup-deals)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python code snippets and numbered cleanup steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit, cleanup, verification, rollback, and Salesforce-sync coordination guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
