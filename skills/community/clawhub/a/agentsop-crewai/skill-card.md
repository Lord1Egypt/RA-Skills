## Description: <br>
SOP for building multi-agent systems with CrewAI, including role-based collaboration, sequential and hierarchical processes, Flows, memory, and delegation for clear agent-team pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsope](https://clawhub.ai/user/agentsope) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to decide when CrewAI is appropriate and to design role-based multi-agent workflows with explicit tasks, process selection, memory posture, observability, and delegation limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can over-activate on vague teamwork or collaboration requests where a single agent or simpler tool flow would be enough. <br>
Mitigation: Confirm that the task truly needs multiple specialized agents before applying the CrewAI workflow. <br>
Risk: CrewAI hierarchical delegation and default manager patterns can add routing uncertainty, token growth, and retry loops. <br>
Mitigation: Prefer sequential processes or explicit Flows unless dynamic manager routing is clearly required, and keep worker delegation off by default. <br>
Risk: Production CrewAI workflows can be difficult to debug without trace data and runtime limits. <br>
Mitigation: Use observability, iteration caps, rate limits, and outer timeouts before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/agentsope/agentsop-crewai) <br>
- [CrewAI Architecture and Mental Model](references/R1-architecture.md) <br>
- [CrewAI SOP Workflow](references/R2-sop-workflow.md) <br>
- [CrewAI Dilemma Cases](references/R3-dilemma-cases.md) <br>
- [CrewAI Anti-Patterns and Boundaries](references/R4-anti-patterns.md) <br>
- [CrewAI Ecosystem Context](references/R5-ecosystem-context.md) <br>
- [CrewAI Agents Documentation](https://docs.crewai.com/en/concepts/agents) <br>
- [CrewAI Tasks Documentation](https://docs.crewai.com/en/concepts/tasks) <br>
- [CrewAI Flows Documentation](https://docs.crewai.com/en/concepts/flows) <br>
- [CrewAI Memory Documentation](https://docs.crewai.com/en/concepts/memory) <br>
- [CrewAI Hierarchical Process Documentation](https://docs.crewai.com/en/learn/hierarchical-process) <br>
- [CrewAI GitHub Repository](https://github.com/crewAIInc/crewAI) <br>
- [CrewAI Manager Agent Discussion](https://github.com/crewAIInc/crewAI/discussions/1220) <br>
- [CrewAI Delegation Loop Issue](https://github.com/crewAIInc/crewAI/issues/330) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline Python and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces decision guidance, CrewAI design patterns, and example agent/task/crew configuration snippets.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
