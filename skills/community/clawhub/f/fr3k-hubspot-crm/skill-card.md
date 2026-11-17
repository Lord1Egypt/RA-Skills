## Description:

Full HubSpot CRM automation for contacts, deals, companies, activities, and pipeline reports via the HubSpot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr3kstyle](https://clawhub.ai/user/fr3kstyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to manage HubSpot contacts, deals, companies, associations, activities, and pipeline reports from an agent-directed command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands can change or delete live HubSpot CRM records using a bearer token without built-in confirmation safeguards.

Mitigation: Use a dedicated private app token with only required scopes and require explicit human confirmation before delete, update, association, or deal-stage commands.

Risk: Running the skill against a production HubSpot account may expose or modify customer and sales data.

Mitigation: Review the account target and token scope before installation, and test workflows in a non-production or least-privileged environment when possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fr3kstyle/skills/fr3k-hubspot-crm)
- [HubSpot API endpoint](https://api.hubapi.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a HubSpot Private App bearer token in HUBSPOT_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
