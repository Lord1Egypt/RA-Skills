## Description:

For agents that take tasks from a Vercel Board - use when a board task needs something your team cannot do. Asks ScBee for up to three verified outside agents that fit, replies in the task's thread with them and their install commands, and holds the task for a person's approval. Also checks a public repo named in a task before your team depends on it. Never installs or runs anything by itself. Not for agents outside a Vercel Board; use find-agent instead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmakt99](https://clawhub.ai/user/hmakt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents working in a team's Vercel Board use this skill to find up to three matching outside agents when their team cannot handle a task, then share suggestions in the task thread for a person's approval. It can also summarize checks of public repositories named in a task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because a local path-like reference could not be resolved, leaving some evidence incomplete.

Mitigation: Resolve and review the referenced material and assess the skill before installation.

## Reference(s):

- [Vercel Board handoff guide](https://scbee.vercel.app/with/vercel-board)
- [ScBee](https://scbee.vercel.app)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Task-thread reply text with suggested agents, install commands, and repository review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggests up to three agents and pauses for a person's approval before any agent is used.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
