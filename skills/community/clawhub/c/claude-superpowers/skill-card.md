## Description:

Claude Superpowers activates a four-stage coding workflow that requires a confirmed plan, isolated branch or working copy, test-first implementation, and double review before presenting changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to impose a disciplined workflow on complex coding tasks: plan with user confirmation, isolate changes, write tests first, and review completed work before presentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can slow coding tasks because it requires plan confirmation, branch isolation, tests, and review before presentation.

Mitigation: Use it when stricter planning and verification are desired, and add the CLAUDE.md installation text only when persistent enforcement is intended.

Risk: The skill directs the agent to create branches and modify project files during coding tasks.

Mitigation: Review the confirmed plan, keep changes isolated until approval, and inspect the final changed file list before accepting the work.

## Reference(s):

- [Claude Superpowers homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/claude-superpowers.html)
- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/claude-superpowers)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with code blocks and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include branch names, test summaries, review checklists, and CLAUDE.md installation text.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
