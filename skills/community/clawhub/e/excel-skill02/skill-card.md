## Description:

Create and manage Product Requirements Documents (PRDs) with user stories, acceptance criteria, and prioritized task tracking for feature implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao202404](https://clawhub.ai/user/zhao202404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and coding agents use this skill to create structured PRDs, define user stories with acceptance criteria, and track feature implementation progress through a PRD JSON file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an unattended coding-agent loop example that bypasses permission checks.

Mitigation: Remove dangerous permission-bypass flags, run agents in a restricted worktree or sandbox, set an iteration limit, keep credentials unavailable, and review diffs and commits before accepting changes.

## Reference(s):

- [7skill ClawHub Release](https://clawhub.ai/zhao202404/skills/excel-skill02)
- [Agent Usage Patterns](references/agent-usage.md)
- [Output Patterns and Templates](references/output-patterns.md)
- [Workflow Patterns for PRD Skills](references/workflows.md)
- [Ralph by snarktank](https://github.com/snarktank/ralph)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Amp Code](https://ampcode.com)
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance, shell commands]

**Output Format:** [Markdown guidance with JSON templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PRD structures and agent workflow guidance; does not itself execute implementation tasks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
