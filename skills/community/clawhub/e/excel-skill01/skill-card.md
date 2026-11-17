## Description:

Create and manage Product Requirements Documents (PRDs) with structured user stories, acceptance criteria, and task prioritization for feature development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhao202404](https://clawhub.ai/user/zhao202404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product managers, and agent operators use this skill to create PRDs that break features into ordered user stories with verifiable acceptance criteria. The references also describe ways coding agents can consume PRDs during implementation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags unattended agent-loop guidance that disables permission checks and can repeatedly modify code without review.

Mitigation: Use bounded, reviewed agent runs with normal permission prompts, avoid the documented dangerous permission-skipping loop on untrusted repositories or PRDs, and inspect diffs before commits.

## Reference(s):

- [Agent Usage Patterns](artifact/references/agent-usage.md)
- [Output Patterns and Templates](artifact/references/output-patterns.md)
- [Workflow Patterns for PRD Skills](artifact/references/workflows.md)
- [Ralph by snarktank](https://github.com/snarktank/ralph)
- [Claude Code](https://github.com/anthropics/claude-code)
- [Amp Code](https://ampcode.com)
- [Tips for AI Coding with Ralph Wiggum](https://www.aihero.dev/tips-for-ai-coding-with-ralph-wiggum)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces PRD structures, acceptance-criteria examples, progress-tracking guidance, and agent workflow prompts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
