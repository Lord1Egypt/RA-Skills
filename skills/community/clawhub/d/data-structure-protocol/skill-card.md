## Description:

Data Structure Protocol (DSP) helps agents build and navigate graph-based structural memory for codebases, storing entities, dependencies, public API entries, and reasons for connections in a .dsp directory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k-kolomeitsev](https://clawhub.ai/user/k-kolomeitsev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use DSP to initialize, update, inspect, and maintain a codebase dependency graph during code changes. The skill guides agents through CLI-backed workflows for creating entities, recording imports and exports, navigating impact, and keeping .dsp structural memory current.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled CLI can delete arbitrary directories if destructive commands receive absolute or traversal-style UIDs.

Mitigation: Install only for trusted projects and prompts, avoid destructive commands such as remove-entity on unreviewed input, and review or back up repository state before use until UID validation and .dsp path confinement are enforced.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k-kolomeitsev/skills/data-structure-protocol)
- [DSP Bootstrap Procedure](references/bootstrap.md)
- [DSP Operations Reference](references/operations.md)
- [DSP Storage Format](references/storage-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code-oriented references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository-local DSP graph maintenance guidance and CLI command suggestions for agent workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
