## Description: <br>
Design, build, and deploy AI agents with architecture patterns, framework selection, memory systems, and production safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, builders, and operators use this skill to design agent systems, choose frameworks, implement memory and tool patterns, define behavior for teams, and review agent security before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact includes an unsafe debugging suggestion to expose chain-of-thought for visibility. <br>
Mitigation: Use structured traces, tool logs, rubric scores, and short summaries instead. <br>
Risk: Agent implementations based on these examples may perform external messages, payments, deletes, deployments, or broad file and account access without sufficient oversight. <br>
Mitigation: Require human approval for external messages, payments, deletes, deployments, and broad file or account access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/agents) <br>
- [Architecture patterns and memory](artifact/architecture.md) <br>
- [Framework comparison](artifact/frameworks.md) <br>
- [Use cases by role](artifact/use-cases.md) <br>
- [Implementation patterns and code](artifact/implementation.md) <br>
- [Security boundaries and risks](artifact/security.md) <br>
- [Evaluation and debugging](artifact/evaluation.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with tables, checklists, and code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; does not declare tools, MCP servers, credentials, or executable workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
