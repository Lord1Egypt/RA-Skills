## Description:

Delegate coding tasks to Cline CLI, an open-source autonomous coding agent that supports one-shot tasks, CI/CD automation, and parallel workstreams with Node.js 20+.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreasthinks](https://clawhub.ai/user/andreasthinks)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to delegate coding, review, testing, CI/CD, and Kanban-style parallel workstream tasks to Cline CLI while retaining human review of generated changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous coding and deploy workflows can make high-impact file, commit, or deployment changes.

Mitigation: Run the skill in an isolated repository, worktree, or container, and review diffs before committing or deploying.

Risk: Auto-approval flags such as `-y` can approve broad tasks without human checkpoints.

Mitigation: Avoid auto-approval for broad or sensitive tasks, use pinned package versions, and scope prompts to specific files or workflows.

Risk: Kanban network binding on `0.0.0.0` can expose the browser UI beyond localhost.

Mitigation: Keep Kanban bound to localhost unless strong access controls and network protections are in place.

Risk: Provider and deployment tokens used by Cline workflows can be over-privileged.

Mitigation: Use least-privilege tokens and keep provider or deployment credentials out of shared logs and prompts.

## Reference(s):

- [Cline CLI documentation](https://cline.bot/cli)
- [ClawHub skill page](https://clawhub.ai/andreasthinks/skills/cline-kanban)
- [Publisher profile](https://clawhub.ai/user/andreasthinks)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command patterns, configuration paths, workflow steps, and review guidance for autonomous coding-agent use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact/SKILL.md frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
