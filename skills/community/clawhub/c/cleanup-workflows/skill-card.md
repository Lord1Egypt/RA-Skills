## Description:

Audit and remove inactive, test, or deprecated workflows from HubSpot. Identifies workflows that have never enrolled contacts, workflows turned off for 90+ days, and test workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

HubSpot administrators and operations teams use this skill to audit workflow inventory, identify inactive or test automations, and plan cautious cleanup with owner notification and rollback documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: HubSpot workflows may be deleted permanently and cannot be restored.

Mitigation: Turn workflows off first, wait one week, document owners and deletion reasons, and capture screenshots or workflow logic before deleting.

Risk: Overbroad HubSpot credentials could expose or change more automation data than needed.

Mitigation: Use a HubSpot token scoped only to needed workflow read or manage permissions and run cleanup only with owner approval.

Risk: Deleting a workflow without checking dependencies can disrupt downstream automations or property updates.

Mitigation: Check workflow enrollment triggers, dependent property updates, and referenced documentation before deletion.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomgranot/skills/cleanup-workflows)
- [HubSpot Workflows API Endpoint](https://api.hubapi.com/automation/v4/flows)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration]

**Output Format:** [Markdown with inline Python code and step-by-step operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a scoped HubSpot API token and owner approval before deletion.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
