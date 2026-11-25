## Description:

编排 WorkBuddy 派发、只读验收与候选交接；不代替业务执行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lisong2003-lgtm](https://clawhub.ai/user/lisong2003-lgtm)

### License/Terms of Use:

MIT

## Use Case:

For people coordinating work between Codex and WorkBuddy, it supports dispatching research and document tasks, requesting read-only independent checks, and handing off isolated code or skill candidates for final review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security report flags directions to implement or repair business code as potentially exceeding the stated coordination and read-only verification role.

Mitigation: Review the skill's instructions and tool scope before use; keep verification read-only, isolate candidate work, and have Codex check deliverables.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lisong2003-lgtm/skills/codex-workbuddy-control)
- [Architecture and workflow](references/architecture.md)
- [Setup](references/setup.md)
- [Commands](references/commands.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task, receipt, and verification templates with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task details and storage locations are supplied by the user.]

## Skill Version(s):

0.1.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
