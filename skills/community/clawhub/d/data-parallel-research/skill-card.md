## Description:

Helps an agent split independent research subtopics across parallel agents and integrate their findings into a unified report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingginwan](https://clawhub.ai/user/mingginwan)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, developers, and research-oriented agents use this skill to decide when research topics are independent enough to delegate in parallel. It provides a task template and review steps for collecting, cross-checking, and merging parallel research outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may cause an agent to spawn multiple research agents, increasing tool use and review load.

Mitigation: Use it only when the research questions are clearly independent, and review each agent's output before integration.

Risk: Parallel research outputs can contain inconsistent facts, assumptions, or terminology.

Mitigation: Cross-check returned findings, investigate contradictions, and normalize terminology before using the final report.

Risk: The artifact instructions are currently Chinese-only, which may reduce usability for agents or reviewers that require English instructions.

Mitigation: Confirm the operating agent and reviewer can reliably interpret the Chinese workflow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mingginwan/skills/data-parallel-research)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown guidance with a reusable agent task template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May lead the host agent to launch multiple independent research agents when the task structure supports parallel work.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
