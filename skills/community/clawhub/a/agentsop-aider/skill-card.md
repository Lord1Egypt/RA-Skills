## Description:

Provides a terminal-based Aider SOP for git-native AI pair programming, covering repo scoping, edit-format choice, architect/editor mode, testing loops, and human-in-the-loop rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and coding agents use this skill to operate Aider in existing git repositories with disciplined file scoping, model/edit-format choices, testing loops, and rollback practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Following Aider workflows can modify code, create commits, and run user-selected commands.

Mitigation: Keep changes scoped, review diffs and commits before accepting them, and run tests or linters before relying on generated edits.

Risk: Unattended automation may apply edits or commands without enough human review.

Mitigation: Avoid unattended --yes workflows unless the surrounding automation and repository context are trusted.

## Reference(s):

- [ClawHub Agentsop Aider Skill Page](https://clawhub.ai/agentsope/skills/agentsop-aider)
- [Aider GitHub Repository](https://github.com/Aider-AI/aider)
- [R1: Aider Architecture & Mental Model](references/R1-architecture.md)
- [R2: Aider SOP Workflow](references/R2-sop-workflow.md)
- [R3: Dilemma Cases](references/R3-dilemma-cases.md)
- [R4: Anti-Patterns & Boundaries](references/R4-anti-patterns.md)
- [R5: Ecosystem Context](references/R5-ecosystem-context.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands, decision rules, and reference links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; it does not include executable installers or hidden actions.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
