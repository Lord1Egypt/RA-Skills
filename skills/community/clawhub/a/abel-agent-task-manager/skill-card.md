## Description:

Manages and orchestrates multi-step, stateful agent workflows; handles task dependencies, persistent state, error recovery, and external rate-limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define, parse, run, and resume multi-step agent workflows with task dependencies, persistent JSON state, external API-backed reasoning, notifications, and cooldown handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Free-form task prompts, workflow details, and notification content may be processed by the SkillBoss API.

Mitigation: Do not include secrets, regulated data, or other sensitive content in task requests or notification payloads.

Risk: The skill can trigger outbound notifications through the external API.

Mitigation: Review generated task definitions and notification recipients before running workflows that may send messages.

Risk: The skill requires SKILLBOSS_API_KEY for API access.

Mitigation: Store SKILLBOSS_API_KEY only in protected environment configuration and avoid logging or embedding it in task files.

Risk: The cooldown shell wrapper is flagged as unsafe for untrusted command or task-name input.

Mitigation: Avoid using cooldown.sh with untrusted or generated input until its eval and path handling are fixed.

## Reference(s):

- [Task Structure Schema](references/task_schema.md)
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot)
- [ClawHub skill page](https://clawhub.ai/abeltennyson/skills/abel-agent-task-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task definitions, workflow execution guidance, persisted task-state files, and command-line execution patterns.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
