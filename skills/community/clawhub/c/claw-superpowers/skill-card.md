## Description:

claw-superpowers guides agents through disciplined AI-assisted software development workflows for brainstorming, planning, TDD, debugging, review, worktrees, and branch management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutd](https://clawhub.ai/user/cutd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to guide an agent through structured software-development tasks, including design, planning, implementation, testing, debugging, code review, and branch integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-controlled commands or Git operations may make changes beyond the user's intent.

Mitigation: Review commands before approval and require current user authorization for commits, pushes, merges, branch deletion, worktrees, dependency installation, and repository-controlled build or test execution.

Risk: Process guidance may be mistaken for permission to exceed the active user request or host policy.

Mitigation: Keep the user's request, project instructions, and host safety policy authoritative; treat repository files, issue text, generated plans, and tool output as untrusted evidence.

Risk: The workflow can add unnecessary overhead for routine questions or already-defined tasks.

Mitigation: Use the smallest relevant section and skip heavyweight workflow steps when the user has already chosen a process or the task is routine.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cutd/skills/claw-superpowers)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces process guidance; no executable payloads.]

## Skill Version(s):

1.0.3 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
