## Description:

Create foundational segmented lists for marketing and sales operations, including a master sendable list, ICP-based lists, persona lists, engagement lists, and behavioral lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomgranot](https://clawhub.ai/user/tomgranot)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operations and sales operations teams use this skill to create active HubSpot segmentation lists for campaign targeting, sales prioritization, and database health monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable script creates different HubSpot lists than the documentation promises.

Mitigation: Inspect the generated list definitions before execution and verify that the created lists match the intended segmentation plan.

Risk: The script-created 'All Marketing Contacts' list omits consent and deliverability filters needed for a compliant sendable audience.

Mitigation: Add and verify unsubscribe, hard bounce, email-known, and quarantine filters in HubSpot before treating the list as sendable.

Risk: The script uses a HubSpot access token to create lists.

Mitigation: Run it only with a token limited to the minimum list-management scopes required for the task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tomgranot/skills/build-smart-lists)
- [ClawHub Publisher Profile](https://clawhub.ai/user/tomgranot)
- [HubSpot API Base URL](https://api.hubapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with a Python execution script and CSV audit output when run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires HubSpot list-management permissions and a HubSpot access token; created lists should be reviewed in HubSpot before use.]

## Skill Version(s):

1.0.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
