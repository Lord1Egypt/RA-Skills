## Description:

Anti-Pattern Czar detects and helps fix TypeScript error-handling anti-patterns, including silent failures, empty catches, promise swallowing, and unlogged errors, with scan, review, auto, resume, and report modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to scan TypeScript projects for error-handling anti-patterns, review findings by severity and critical path, and apply approved fixes with session state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs the external antipattern-czar package through Bun, and the release security summary flags that package as unpinned.

Mitigation: Pin and review an exact package version before use, and run scans in a controlled repository context.

Risk: Broad trigger phrases could start scans or edit-oriented workflows unintentionally.

Mitigation: Invoke the skill explicitly by name and grant write access only when a fix workflow is intended.

Risk: Automated fixes can modify TypeScript error-handling behavior, especially outside critical paths.

Mitigation: Use review mode for critical-path findings, require explicit confirmation for auto mode, and inspect resulting diffs before merging.

## Reference(s):

- [Anti-Pattern Czar on ClawHub](https://clawhub.ai/glucksberg/skills/anti-pattern-czar)
- [Anti-Pattern Patterns Reference](references/patterns.md)
- [Workflow Details](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and text reports with shell commands, JSON state, and TypeScript fix snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes .anti-pattern-state.json for session state when scanning or fixing.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
