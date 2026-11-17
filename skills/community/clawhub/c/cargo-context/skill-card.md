## Description:

Reads and updates a company's go-to-market knowledge base in Cargo and queries its knowledge graph.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Revenue teams and their agents use this skill to read and maintain company context such as ICPs, personas, positioning, plays, proof points, objections, competitors, and buying signals. It also helps inspect the context repository and its knowledge graph.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Context writes, edits, and command-driven changes can be pushed to the workspace repository immediately.

Mitigation: Confirm the active workspace and review the intended changes before writing or running commands that modify files.

Risk: Call-derived context may include sensitive customer details or quotations.

Mitigation: Review and redact sensitive details before saving call-derived content.

Risk: The security assessment covers the bundled instructions, not the external Cargo CLI implementation or missing sibling guidance.

Mitigation: Use a reviewed, pinned CLI release and workspace-scoped credentials.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cargo-ai/skills/cargo-context)
- [Project homepage (metadata)](https://github.com/getcargohq/cargo-skills)
- [Canonical context repository example](https://github.com/getcargohq/cargo-workspaces)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown]

**Output Format:** [Markdown guidance and Cargo CLI commands; context entries use typed Markdown or MDX.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cargo CLI responses are JSON; context write and edit operations push changes to the workspace repository.]

## Skill Version(s):

1.4.3 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
