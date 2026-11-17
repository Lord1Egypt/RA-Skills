## Description:

Codemod helps agents search, run, and author repeatable codemods for migrations, upgrades, updates, deprecations, API changes, and large mechanical refactors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohebifar](https://clawhub.ai/user/mohebifar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate codebase migrations, upgrades, refactors, codemod discovery, codemod authoring, and AST or tree-sitter inspection through Codemod CLI workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct agents to run broad, unpinned Codemod CLI commands that may fetch executable code at runtime.

Mitigation: Review the skill before installing it in sensitive repositories, use a trusted locally installed or pinned Codemod CLI, run codemods in a constrained workspace, inspect dry-run output, and avoid exposing unnecessary credentials.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, code edits, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run Codemod CLI commands, inspect dry-run results, and produce codemod package files when authoring is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
