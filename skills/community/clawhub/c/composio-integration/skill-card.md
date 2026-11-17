## Description:

Access and manage Gmail emails and Google Tasks through Composio's unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rita5fr](https://clawhub.ai/user/rita5fr)

### License/Terms of Use:


## Use Case:

Developers and automation users can use this skill to list Composio tools and run Gmail or Google Tasks actions such as searching email, sending messages, and creating tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports an exposed plaintext Composio API key.

Mitigation: Revoke and rotate the key before installation or use, then provide credentials through a secure environment variable or secrets store.

Risk: The skill can invoke broad Gmail and Google Tasks actions, including sending, deleting, or modifying user data.

Mitigation: Require explicit confirmation and narrow allowlists for sensitive actions before executing them.

Risk: Artifact documentation includes personal account identifiers and connected account IDs.

Mitigation: Remove personal identifiers from published documentation and require users to supply their own connected account IDs.

## Reference(s):

- [Composio REST API Documentation](https://docs.composio.dev/rest-api/)
- [Composio Apps Directory](https://docs.composio.dev/apps)
- [ClawHub Skill Page](https://clawhub.ai/rita5fr/skills/composio-integration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent instructions and command examples for invoking Composio-backed tools; tool execution results depend on Composio API responses.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
