## Description:

VS Code bridge pack for context push/pull and session linking between VS Code and OpenClaw Gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[romainsantoli-web](https://clawhub.ai/user/romainsantoli-web)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to synchronize selected VS Code context, file contents, diagnostics, and editor session state with OpenClaw Gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send selected VS Code context, file contents, diagnostics, and session metadata through OpenClaw Gateway.

Mitigation: Avoid syncing secrets, proprietary code, or regulated data unless that use is approved for the deployment environment.

Risk: Context synchronization can expose editor state beyond the local workspace.

Mitigation: Review the selected context before pushing it and keep the VS Code OpenClaw extension configured according to local policy.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline tool commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bridge-tool usage guidance for VS Code context sync and session status workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
