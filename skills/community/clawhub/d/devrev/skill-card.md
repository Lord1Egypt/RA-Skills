## Description: <br>
Interact with DevRev to create/update issues and tickets, and search/query works and parts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nimit2801](https://clawhub.ai/user/nimit2801) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and support engineers use this skill to manage DevRev issues, tickets, and parts through DevRev REST API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a DevRev token to create, update, or delete live DevRev records. <br>
Mitigation: Use a dedicated least-privilege DevRev token and require explicit confirmation before any create, update, or delete operation. <br>
Risk: Incorrect object IDs or fields could modify the wrong issue, ticket, part, or user assignment. <br>
Mitigation: Verify DON IDs, display IDs, target fields, and proposed payloads before executing write commands. <br>
Risk: A DevRev token shared in chat or logs could expose workspace data. <br>
Mitigation: Provide the token through DEVREV_TOKEN, avoid pasting it into chat, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [DevRev skill page](https://clawhub.ai/nimit2801/devrev) <br>
- [DevRev API Reference](references/api.md) <br>
- [DevRev token settings](https://app.devrev.ai/settings/tokens) <br>
- [DevRev API base URL](https://api.devrev.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a DevRev PAT provided through DEVREV_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
