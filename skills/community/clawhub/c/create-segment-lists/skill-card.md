## Description:

Create business segment lists in HubSpot for customers, partners, competitors, employees, ICP tiers, and industries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operations and CRM teams use this skill to plan, create, verify, and maintain HubSpot segment lists for targeting, suppression, reporting, and workflow enrollment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create and manage HubSpot marketing segment lists, which may affect targeting, suppression, reporting, workflows, or campaigns.

Mitigation: Use a HubSpot token with only the minimum list-management permissions needed, review proposed list names and criteria before execution, and check list dependencies before deleting or replacing lists.

Risk: Incorrect segment criteria can put contacts into misleading or conflicting lists.

Mitigation: Verify member counts, check for mutually exclusive segment conflicts, and confirm visibility with the appropriate teams after list creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tomgranot/skills/create-segment-lists)
- [Publisher profile](https://clawhub.ai/user/tomgranot)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, API Calls]

**Output Format:** [Markdown with inline Python code blocks and checklist-style verification guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces HubSpot list planning criteria, API usage examples, verification steps, rollback guidance, and maintenance tips.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
