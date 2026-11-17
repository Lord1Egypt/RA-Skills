## Description:

创建和编排多智能体集群完成复杂任务，将复杂 work 拆解给多个专业智能体并行或串行执行。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lixiang1076](https://clawhub.ai/user/lixiang1076)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to plan, configure, and coordinate multi-agent teams for complex tasks such as research, coding, writing, analysis, review, and automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill grants broad authority over agent configuration, workspace files, command execution, browser automation, scheduled jobs, and persistent memory.

Mitigation: Restrict permitted agent IDs and base paths before deployment, and disable cron, browser, and exec access unless they are required for the specific workflow.

Risk: Persistent agent memory can store and later reinject sensitive or stale task context.

Mitigation: Avoid storing secrets or sensitive user content in experience logs, and review or clear stored memories before they are injected into new tasks.

Risk: Multi-agent orchestration can amplify incorrect, unsafe, or low-quality intermediate outputs.

Mitigation: Review planned sub-agent tasks, scan the skill before deployment, and require human review for high-impact outputs.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lixiang1076/skills/agent-swarm-ex)
- [Setup guide](references/setup-guide.md)
- [CHJ-Private model configuration guide](references/chj-private-guide.md)
- [CHJ-Private configuration template](references/chj-private-config-template.json)
- [Task statistics template](references/statistics-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline code blocks, JSON configuration examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce task plans, sub-agent prompts, configuration snippets, command examples, and execution statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
