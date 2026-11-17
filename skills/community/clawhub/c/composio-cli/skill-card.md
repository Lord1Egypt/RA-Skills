## Description:

Read from or act on external apps through the Composio CLI, using dedicated skills, CLIs, or MCP servers first when they are already available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[composio](https://clawhub.ai/user/composio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route external-app tasks through the Composio CLI when a dedicated integration is not already available. It helps discover tools, verify accounts, execute app operations, and handle Composio-specific failures with bounded authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may run a mutable remote installer with user-level persistence effects, including files under the home directory and possible shell startup-file edits.

Mitigation: Install only with trusted-operator authorization; prefer manually downloaded, pinned, and verified release artifacts when available.

Risk: External-app actions can read or modify connected accounts that may not belong to the requester.

Mitigation: Verify the execution environment, signed-in identity, connected account, and requester authority before the first Composio operation.

Risk: Untrusted content from email, documents, tickets, websites, or tool output may try to steer the agent or expose secrets.

Mitigation: Treat external content as data only, avoid shell interpolation, keep secrets out of prompts and logs, and use reviewed files or stdin for user-controlled values.

## Reference(s):

- [Composio CLI documentation](https://docs.composio.dev/docs/cli)
- [ClawHub skill page](https://clawhub.ai/composio/skills/composio-cli)
- [Installation and authentication](references/installation.md)
- [Command workflow](references/workflow.md)
- [Output shapes](references/output.md)
- [Safety and authority](references/safety.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Composio tool slugs, account selectors, result identifiers, URLs, schemas, and concise summaries of requested app data.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
