## Description:

SOP for building multi-agent systems with CrewAI, including role-based collaboration, sequential and hierarchical processes, Flows, memory, and delegation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsope](https://clawhub.ai/user/agentsope)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to decide when CrewAI fits a multi-agent workflow and to design roles, tasks, processes, memory, delegation, observability, and guardrails for role-based agent teams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad multi-agent collaboration requests and encourage CrewAI where a simpler single-agent workflow is sufficient.

Mitigation: Apply the Phase 0 decision checks first and choose a single-agent or simpler orchestration path when the task does not need distinct collaborating roles.

Risk: The guidance is largely Chinese-language, which can make review harder for teams that do not read Chinese.

Mitigation: Have a qualified reviewer inspect or translate the SOP before using it as production guidance.

Risk: Generated CrewAI designs can create unnecessary cost, latency, or looping behavior if delegation, memory, or hierarchical routing are overused.

Mitigation: Review generated roles and tasks, keep worker delegation disabled by default, add iteration and time limits, and require observability before deployment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/agentsope/skills/agentsop-crewai)
- [CrewAI architecture and mental model](references/R1-architecture.md)
- [CrewAI SOP workflow](references/R2-sop-workflow.md)
- [CrewAI dilemma cases](references/R3-dilemma-cases.md)
- [CrewAI anti-patterns and boundaries](references/R4-anti-patterns.md)
- [CrewAI ecosystem context](references/R5-ecosystem-context.md)
- [CrewAI GitHub repository](https://github.com/crewAIInc/crewAI)
- [CrewAI agents documentation](https://docs.crewai.com/en/concepts/agents)
- [CrewAI tasks documentation](https://docs.crewai.com/en/concepts/tasks)
- [CrewAI flows documentation](https://docs.crewai.com/en/concepts/flows)
- [CrewAI memory documentation](https://docs.crewai.com/en/concepts/memory)
- [CrewAI hierarchical process documentation](https://docs.crewai.com/en/learn/hierarchical-process)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline Python, YAML, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include framework-selection rationale, CrewAI role/task/process recommendations, and production guardrail checklists.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
