## Description:

Methodical end-to-end software delivery orchestrator for Codex CLI with dual project modes, dual execution modes, strict stage gates, progress tracking, manual and automated testing, continuous documentation updates, change-impact management, and a reusable AGENTS.md workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shalomobongo](https://clawhub.ai/user/shalomobongo)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to coordinate Codex CLI and other coding agents through spec-driven planning, gated implementation, validation evidence, documentation updates, and release handoff for greenfield or brownfield software projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delegate broad code-changing and command-running authority to external coding agents.

Mitigation: Use gated execution for unreviewed work, review generated prompts and commands before execution, and run tasks in a disposable branch or worktree.

Risk: Full-auto execution may make changes or run commands before a user has reviewed the task boundary.

Mitigation: Avoid --full-auto for unreviewed tasks and require explicit validation commands and manual review notes before marking gates as passed.

Risk: Validation commands may affect external services, destructive data paths, migrations, payments, or rollback flows.

Mitigation: Use staging or sandbox accounts for delete, payment, migration, and rollback tests, and keep validation commands explicit and reviewed.

Risk: The packaging helper can include unwanted sensitive or generated files if run on an unsafe directory.

Mitigation: Do not package directories containing secrets, symlinks, .env files, or generated archives.

## Reference(s):

- [Spec-Driven Development](references/spec-driven-development.md)
- [Planning Questionnaire](references/planning-questionnaire.md)
- [Modes](references/modes.md)
- [Gate Checklists](references/gate-checklists.md)
- [Testing Matrix](references/testing-matrix.md)
- [Manual Test Templates](references/manual-test-templates.md)
- [Coding-Agent Runbook](references/codex-runbook.md)
- [Gate Prompt Templates](references/gate-prompts.md)
- [Research Playbook](references/research-playbook.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, generated prompts, documentation artifacts, JSON gate state, and validation logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are project-scoped orchestration artifacts and command recommendations; validation evidence is recorded in project documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
