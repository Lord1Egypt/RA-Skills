## Description:

Manage Asana via the Asana REST API. Use when you need to list workspaces, projects, tasks, search tasks, comment, update, complete, or create tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k0nkupa](https://clawhub.ai/user/k0nkupa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent manage Asana workspaces, projects, and tasks through a Node.js CLI backed by the Asana REST API, including listing, search, comments, updates, completion, and task creation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asana credentials may be exposed through saved local files or command-line use.

Mitigation: Prefer environment variables or a secret manager, avoid passing secrets on the command line, and restrict permissions on ~/.openclaw/asana.

Risk: The skill can modify live Asana tasks, comments, and completion state.

Mitigation: Use a low-privilege Asana token or test workspace when possible, and review mutating commands before execution.

## Reference(s):

- [Asana Developer Documentation](https://developers.asana.com/docs)
- [Asana endpoints quick reference](artifact/references/asana-endpoints.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON API responses, terminal text, and Markdown setup guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and Asana authentication; commands can read and modify live Asana data.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
