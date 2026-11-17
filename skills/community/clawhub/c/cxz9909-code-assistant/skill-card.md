## Description:

A Spanish-language programming assistant that analyzes source code, finds bugs, suggests optimizations, supports refactoring, and generates documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxz9909](https://clawhub.ai/user/cxz9909)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review source files or directories, identify common code quality and security patterns, measure complexity, and generate documentation drafts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future refactor, auto-fix, or self-repair behavior could modify code if implemented by the host agent or a later version.

Mitigation: Review proposed code changes before applying them, and run normal tests and scans before deployment.

Risk: Static pattern findings and generated documentation can be incomplete or misleading.

Mitigation: Treat outputs as review aids and confirm findings against the source code, project tests, and security review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxz9909/skills/cxz9909-code-assistant)
- [ClawHub publisher profile](https://clawhub.ai/user/cxz9909)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and may include analysis summaries, bug findings, optimization suggestions, documentation drafts, test suggestions, and commands for the host agent to run.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
