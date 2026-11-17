## Description:

Diagram as contract for agreed-upon AI development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonlinear](https://clawhub.ai/user/nonlinear)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to view Mermaid-based contract diagrams, track agreed implementation phases, and work with Markdown contract files through a local viewer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unauthenticated local server can expose read/write behavior for Markdown files.

Mitigation: Run the server only on loopback, narrowly allowlist file paths, and avoid exposing the port to other hosts.

Risk: Automatic file rewriting can alter private or important Markdown files.

Mitigation: Use disposable or version-controlled files, remove write access where possible, and require explicit confirmation before writes.

Risk: Rendered Markdown or diagram content may be unsafe when input is not trusted.

Mitigation: Sanitize Markdown before rendering and use the viewer only with trusted contract files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nonlinear/skills/contract-diagram)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with Mermaid diagrams and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch a local hot-reload viewer and update diagram metadata in Markdown files.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
