## Description:

AutoCraft guides AI-assisted software project planning, task execution, verification, and quality checks for structured product delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin-chen2025](https://clawhub.ai/user/robin-chen2025)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, developers, and engineering leads use AutoCraft to plan software projects, convert plans into task tickets, coordinate AI agent execution, and verify deliverables against design and quality criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs mutable external code.

Mitigation: Review install.sh and the external AutoCraft repository before installation, pin the repository to a reviewed commit, and run the system in a container or disposable development VM.

Risk: The skill exposes persistent local services with limited containment.

Mitigation: Bind services to 127.0.0.1 unless remote access is intentional, monitor the started processes, and stop nohup processes after use.

Risk: Task inputs and sub-agent behavior can affect project outputs.

Mitigation: Treat task inputs as untrusted and keep prior user, repository, and policy constraints in force when AutoCraft sub-agents generate or verify work.

## Reference(s):

- [AutoCraft ClawHub skill page](https://clawhub.ai/robin-chen2025/skills/autocraft)
- [AutoCraft task creator reference](references/task-creator/SKILL.md)
- [AutoCraft agent guide](references/ac-agent-guide/SKILL.md)
- [Architecture check reference](scripts/architecture-check/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, API payloads, validation reports, and code or configuration templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, npm, and git according to artifact metadata.]

## Skill Version(s):

2.1.0 (source: server release evidence; artifact SKILL.md v2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
