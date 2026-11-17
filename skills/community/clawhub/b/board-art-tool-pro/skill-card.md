## Description:

画板艺术工具专业版 helps agents manage team canvas workflows for batch artwork publishing, multi-frame animation, scheduled releases, canvas zone permissions, and artwork analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and team workspace operators use this skill to automate board-art publishing workflows, configure canvas governance, schedule animation releases, and review artwork performance metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad read, write, and execution authority for team canvas publishing and governance.

Mitigation: Run it only in the board-art workflow, scope credentials to the minimum board and role permissions, and require explicit confirmation before publish, modify, delete, or permission changes.

Risk: Broad trigger language could cause the skill to be invoked for unrelated analytics or automation work.

Mitigation: Limit activation to board-art batch publishing, animation, analytics, and governance tasks; use another skill for general analytics or automation.

Risk: Canvas service tokens and scheduling keys may grant access to team boards or release workflows.

Mitigation: Provide credentials through environment variables, avoid hardcoding secrets, and rotate or revoke tokens after use in shared environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/board-art-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples, shell command examples, configuration snippets, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe publish results, conflict reports, board-governance configuration, animation frame settings, and analytics summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
