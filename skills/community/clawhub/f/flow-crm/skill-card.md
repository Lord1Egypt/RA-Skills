## Description:

Interact with FlowDeck CRM API (clients, deals, proposals, receivables, expenses, contacts). Use for all CRM operations via the FlowDeck REST API through Supabase Edge Functions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[araujodgdev](https://clawhub.ai/user/araujodgdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and CRM operators use this skill to list, retrieve, create, update, and delete FlowDeck CRM records such as clients, deals, proposals, receivables, expenses, and contacts through the FlowDeck REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or delete real CRM and project data when used with a powerful FlowDeck API key.

Mitigation: Use a least-privilege API key and require explicit user confirmation before update or delete actions.

Risk: Changing FLOWDECK_BASE_URL could send credentials or requests to an unintended API endpoint.

Mitigation: Keep FLOWDECK_BASE_URL pinned to the legitimate FlowDeck endpoint before running commands.

Risk: The security summary notes that the skill exposes broader actions than its CRM description clearly communicates.

Mitigation: Review the supported resources and actions before installing, especially project-management resources and destructive operations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/araujodgdev/skills/flow-crm)
- [FlowDeck API gateway endpoint](https://mycivgjuujlnyoycuwrz.supabase.co/functions/v1/api-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, Python 3.10 or newer, and a FlowDeck API key supplied by FLOWDECK_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
