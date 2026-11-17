## Description:

Leads AI software projects through strict research, design, planning, and implementation phases to produce secure, maintainable, and high-quality code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sidrtraktor](https://clawhub.ai/user/sidrtraktor)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to make an AI coding agent gather factual codebase context, design an architecture, plan implementation steps, and execute work through human review gates and quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill treats sub-agent coordination and commits after completed phases as part of its normal workflow.

Mitigation: Before using the skill, decide whether the agent must ask separately before spawning sub-agents or creating commits.

Risk: The skill blocks progress until human review gates, builds, tests, linting, security checks, and architecture checks are satisfied.

Mitigation: Use it when the project can support staged reviews and make the required approval path clear before implementation begins.

Risk: The workflow forbids architecture guessing when the stack, patterns, or project standards are missing.

Mitigation: Provide the technology stack and architectural standards with the initial task, or expect the agent to pause for clarification.

## Reference(s):

- [AI Tech Lead on ClawHub](https://clawhub.ai/sidrtraktor/skills/ai-tech-lead)
- [Publisher profile](https://clawhub.ai/user/sidrtraktor)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with code, command, configuration, and review guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill emphasizes staged research, design, planning, implementation coordination, human approval gates, and quality checks.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
