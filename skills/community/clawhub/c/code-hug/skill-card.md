## Description:

AI-driven software development workflow orchestrator that supports end-to-end project management, code analysis, business intelligence extraction, diagnostics, and workflow automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hickhe](https://clawhub.ai/user/hickhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use Code Hug to analyze multi-language software projects, extract business rules and PRD-style documentation, diagnose build or test failures, and coordinate staged implementation and validation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad repository analysis may expose private source code, business rules, audit trails, or generated analysis artifacts.

Mitigation: Run the skill first on a copy or narrow project path, review generated .code-hug/ contents, and add .code-hug/ to .gitignore when analysis artifacts should not be committed.

Risk: Auto-fix workflows can modify build configuration, dependencies, or source code in ways that require human review.

Mitigation: Keep auto_fix disabled unless changes are expected, use version control, review diffs before accepting changes, and retain rollback controls.

Risk: The security verdict is suspicious because scoping, consent, and data-handling details are limited for a workflow that can inspect production-adjacent repositories.

Mitigation: Review the skill before installing in private or production-adjacent repositories and use isolated, pinned dependency environments where possible.

## Reference(s):

- [Code Hug on ClawHub](https://clawhub.ai/hickhe/skills/code-hug)
- [Publisher profile: hickhe](https://clawhub.ai/user/hickhe)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON-style command arguments, configuration snippets, shell commands, and generated project artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update workspace analysis artifacts under .code-hug/ and may propose or attempt auto-fixes when enabled.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
