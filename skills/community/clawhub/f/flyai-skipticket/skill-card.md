## Description:

Artifact contents describe a guide for creating or updating agent skills with bundled workflow guidance and helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jixinda](https://clawhub.ai/user/jixinda)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this release to plan, initialize, validate, and package agent skills with concise guidance and reusable helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local helper scripts may write or package files outside the intended skill directory because of filesystem scoping issues.

Mitigation: Use clean, trusted skill directories, avoid packaging untrusted folders or symlinks, keep output paths outside the source skill tree, and review packages before deployment.

## Reference(s):

- [Workflow Patterns](artifact/references/workflows.md)
- [Output Patterns](artifact/references/output-patterns.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with optional code, shell commands, and generated files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create skill directories and .skill packages when helper scripts are invoked]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
