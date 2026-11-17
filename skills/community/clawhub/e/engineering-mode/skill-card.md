## Description:

Engineering Mode guides coding agents through a six-stage workflow for understanding, decomposing, isolating, executing, verifying, and recovering from code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzxiaoqiang520](https://clawhub.ai/user/zzzxiaoqiang520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to structure code-writing, refactoring, and recovery work into explicit stages with local verification gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recovery guidance can discard unrelated work through reset, checkout, or branch deletion commands.

Mitigation: Require explicit user confirmation before destructive Git operations and verify the exact branch or checkpoint target before running them.

Risk: Wildcard branch cleanup and unpinned lint or test invocations can affect more than the intended worktree or toolchain.

Mitigation: Use exact branch names for cleanup and prefer locally pinned project validation commands.

## Reference(s):

- [Engineering Mode Skill Page](https://clawhub.ai/zzzxiaoqiang520/skills/engineering-mode)
- [Commit Discipline](references/commit-discipline.md)
- [Error Recovery](references/error-recovery.md)
- [Pre-Edit Checklist](references/pre-edit-checklist.md)
- [Validate Strategies](references/validate-strategies.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and staged checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to read files, edit code, run validation commands, and report recovery outcomes.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
