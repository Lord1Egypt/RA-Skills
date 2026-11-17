## Description:

Guides an agent through multi-stage dead code detection and cleanup using codebase-memory-mcp knowledge graphs, layered reference checks, build validation, and cleanup reporting for single repositories and monorepos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yexinjia](https://clawhub.ai/user/yexinjia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find and remove unreferenced code, orphaned files, duplicate candidates, and unused exports in trusted repositories. It is intended for single-repository and monorepo cleanup workflows that require staged validation, build checks, and an auditable cleanup summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can delete project files or remove exports during cleanup.

Mitigation: Run it only on trusted repositories, commit or stash first, and require a dry run plus an explicit pre-delete file list before allowing deletion.

Risk: The workflow can change local codebase-memory-mcp settings, enable persistent UI behavior, or open the local graph UI.

Mitigation: Allow MCP repair, persistent UI enablement, and browser opening only when those local environment changes are explicitly desired.

Risk: The workflow may run project build or test commands as part of validation.

Mitigation: Permit build and test execution only in a trusted workspace with expected dependencies and commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yexinjia/skills/dead-code-cleaner)
- [Server-resolved GitHub source repository](https://github.com/yexinjia/dead-code-cleaner)
- [Output summary template](references/output-template.md)
- [Verification patterns reference](references/verification-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown cleanup report with shell command evidence, file/change lists, validation results, and risk assessment.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify or delete tracked project files after validation and may guide local codebase-memory-mcp configuration changes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
