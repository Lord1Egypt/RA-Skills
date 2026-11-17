## Description:

Codex Autopilot helps agents orchestrate multi-model coding sessions in tmux, route frontend and backend tasks, manage task queues, monitor progress, and trigger testing and auto-fix workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwyvern](https://clawhub.ai/user/imwyvern)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to operate multiple AI coding sessions across projects, dispatch queued tasks to Codex or Gemini, monitor idle or stuck sessions, and connect testing and review loops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent autonomous coding workflows can approve or execute high-impact actions without enough user control.

Mitigation: Disable automatic permanent approvals and yolo/full-auto modes, review task and PRD command checks, and keep human review in the loop for high-impact actions.

Risk: Configured repositories and notification channels may expose sensitive project actions or tokens.

Mitigation: Protect Telegram and Discord tokens, scope repository access narrowly, and run the skill under a low-privilege account or disposable project-scoped sandbox.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imwyvern/skills/codex-autopilot)
- [README](README.md)
- [Test Agent Design](docs/test-agent-design.md)
- [Branch Isolation Design](docs/branch-isolation-design.md)
- [Discord Routing Plan](docs/discord-routing-plan.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Code]

**Output Format:** [Markdown guidance with shell commands, YAML configuration examples, and code-oriented workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May operate through persistent tmux sessions, local scripts, task queues, and notification channels configured by the user.]

## Skill Version(s):

0.7.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
