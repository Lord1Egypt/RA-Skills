## Description:

Auto Model Router automatically selects a model for OpenClaw agents based on task complexity and task category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmchenggh](https://clawhub.ai/user/hmchenggh)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to route tasks across configured model plans, task categories, fallback rules, and optional sub-agent dispatch without manually choosing a model for each request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic model switching may route prompts or files to different model providers with limited user control or disclosure.

Mitigation: Review the selected plan and provider configuration before use, restrict providers that may receive sensitive data, and avoid sensitive inputs until external lookup behavior is clarified.

Risk: Task-specific sub-agent dispatch may change which agent or model handles an interrupted task.

Mitigation: Review or disable sub-agent settings for sensitive workflows and require explicit confirmation before dispatching side tasks.

Risk: The published security guidance recommends a pinned or verified installer command.

Mitigation: Prefer pinned installation, verify release hashes when available, and install only from the server-resolved skill page or trusted tooling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hmchenggh/skills/auto-model-router-glm)
- [Publisher profile](https://clawhub.ai/user/hmchenggh)
- [Project homepage](https://github.com/HMCHENGGH/auto-model-router)
- [README](artifact/README.md)
- [Task routing rules](artifact/task-rules.json)
- [Plan C GLM configuration](artifact/config/plan-c.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes work across task categories, model plans, fallbacks, and optional sub-agent dispatch.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
