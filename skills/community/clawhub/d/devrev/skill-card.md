## Description:

Interact with DevRev to create/update issues and tickets, and search/query works and parts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nimit2801](https://clawhub.ai/user/nimit2801)

### License/Terms of Use:


## Use Case:

Developers and support engineers use this skill to let an agent manage DevRev issues, tickets, works, and parts through the DevRev REST API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, or delete live DevRev records when supplied with a PAT.

Mitigation: Use a least-privilege PAT and require explicit approval before create, update, or delete operations.

Risk: Pasting DevRev tokens into chat can expose credentials.

Mitigation: Store the token in the DEVREV_TOKEN environment variable and avoid sharing it in conversation.

Risk: An agent could modify the wrong DevRev record if the target is ambiguous.

Mitigation: Show the target record ID before any write operation and ask the user to confirm it.

## Reference(s):

- [DevRev API Reference](references/api.md)
- [DevRev API](https://api.devrev.ai)
- [DevRev token settings](https://app.devrev.ai/settings/tokens)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a DEVREV_TOKEN environment variable for authenticated DevRev API operations.]

## Skill Version(s):

1.0.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
