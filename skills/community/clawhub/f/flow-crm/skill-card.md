## Description: <br>
Interact with FlowDeck CRM API (clients, deals, proposals, receivables, expenses, contacts). Use for all CRM operations via the FlowDeck REST API through Supabase Edge Functions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araujodgdev](https://clawhub.ai/user/araujodgdev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers with a FlowDeck workspace use this skill to manage CRM, project, finance, and contact records through the FlowDeck REST API. It supports listing, retrieving, creating, updating, and deleting FlowDeck resources when supplied with an appropriately scoped API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, or delete business records including receivables, expenses, clients, projects, tasks, and comments. <br>
Mitigation: Require explicit user confirmation before any create, update, delete, or payment-related action. <br>
Risk: The client creation workflow asks for sensitive business and personal identifiers such as CPF/CNPJ and finance contact details. <br>
Mitigation: Collect only fields that are truly needed for the user's task and avoid storing or sharing unnecessary sensitive data. <br>
Risk: Use with an overly broad or inappropriate API key could expose or modify FlowDeck workspace data. <br>
Mitigation: Use only with a FlowDeck workspace where the API key is appropriately scoped and revoke keys that are invalid, overbroad, or no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/araujodgdev/flow-crm) <br>
- [Publisher profile](https://clawhub.ai/user/araujodgdev) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FLOWDECK_API_KEY or an API key argument; API responses are printed as formatted JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
