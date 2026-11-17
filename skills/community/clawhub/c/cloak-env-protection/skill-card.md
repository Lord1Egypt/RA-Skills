## Description:

Protect .env secrets from AI agents by keeping real credentials encrypted in a vault while agents see structurally valid sandbox values on disk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danieltamas](https://clawhub.ai/user/danieltamas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to recognize Cloak-protected projects, avoid direct access to real secrets, and use Cloak commands for safe .env handling when real environment values are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote installer commands may execute unverified scripts directly in a shell.

Mitigation: Review the Cloak project and installer source first; prefer a signed, versioned package or a download, verify, inspect, then run workflow.

Risk: Commands that reveal, edit, set, or run processes with real secrets can expose sensitive credentials if used without user direction.

Mitigation: Keep Cloak actions user-directed and rely on Cloak authentication prompts instead of attempting manual vault access or secret injection.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should preserve secret-handling boundaries and avoid revealing or reconstructing real secret values.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
