## Description:

Automatically analyzes complex tasks, classifies them by type and priority, creates sub-agent task plans, tracks progress, and reviews deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sixtysixsone](https://clawhub.ai/user/sixtysixsone)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent decide when a request needs sub-agent delegation and produce structured plans for research, development, documentation, batch, or search tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic sub-agent planning can delegate broad or destructive tasks with limited user oversight.

Mitigation: Use only where automatic delegation is acceptable and require manual confirmation for deletion, bulk changes, or other high-impact actions.

Risk: The scheduler records raw task text and progress in persistent memory files.

Mitigation: Do not include secrets or sensitive prompts in task text; use it only in workspaces where this persistence is acceptable.

Risk: Security review flagged the release as suspicious because data safeguards and user controls are limited.

Mitigation: Review the skill before installation and prefer a pinned or organization-approved ClawHub installer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sixtysixsone/skills/auto-complex-task-planner)
- [README.md](artifact/README.md)
- [README_CN.md](artifact/README_CN.md)
- [SKILL.md](artifact/SKILL.md)
- [scheduler.py](artifact/scheduler.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and JSON-like task records with optional shell configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist raw task details in local JSON and daily memory files when the scheduler runs.]

## Skill Version(s):

2.0.0 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
