## Description:

Ensure all contacts and companies have appropriate lifecycle stages by auditing missing or disallowed values, applying HubSpot lifecycle-stage corrections, and creating prevention workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

CRM administrators, RevOps teams, and developers use this skill to audit HubSpot lifecycle-stage coverage, correct records in missing or disallowed stages, and add prevention workflows for future records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable workflow can bulk change HubSpot contact and company lifecycle stages to Lead.

Mitigation: Run only the audit first, verify the target account and record counts, use a narrowly scoped token or sandbox, export record-level backups, and require an explicit apply step before changes.

Risk: Lifecycle-stage corrections can reduce CRM data quality if records are moved without account or company context.

Mitigation: Review the proposed mappings and apply context-aware stage assignment before running updates on a live HubSpot portal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/fix-lifecycle-stages)
- [HubSpot API endpoint](https://api.hubapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with Python scripts and CSV audit outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a HubSpot access token and may write before, execute, and after CSV audit files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
