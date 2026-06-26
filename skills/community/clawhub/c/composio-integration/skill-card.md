## Description: <br>
Access and manage Gmail emails and Google Tasks through Composio's unified API, including tool discovery, email actions, and task automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Rita5fr](https://clawhub.ai/user/Rita5fr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to discover Composio tools and execute Gmail or Google Tasks operations from shell and Node.js workflows. It is suited to email search, draft or send actions, task creation, task updates, and connected-account automation when credentials and permissions are controlled by the operator. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports exposed live-looking credentials and personal account identifiers. <br>
Mitigation: Treat embedded keys and account IDs as compromised; remove them before use and configure fresh, scoped credentials controlled by the operator. <br>
Risk: The skill can execute sensitive Gmail and Google Tasks actions, including sending or deleting email and bulk-changing tasks. <br>
Mitigation: Restrict allowed tools and connected accounts, review parameters before execution, and require explicit confirmation for send, delete, or bulk-update actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Rita5fr/composio-integration) <br>
- [Publisher profile](https://clawhub.ai/user/Rita5fr) <br>
- [Composio REST API documentation](https://docs.composio.dev/rest-api/) <br>
- [Composio apps documentation](https://docs.composio.dev/apps) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, Configuration instructions, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash and JavaScript examples, plus JSON API responses from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires operator-provided Composio credentials and connected account identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
