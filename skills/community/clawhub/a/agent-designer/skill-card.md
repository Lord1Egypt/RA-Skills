## Description: <br>
Agent Designer is a toolkit for designing, generating tool schemas for, and evaluating multi-agent systems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Agent Designer to plan multi-agent architectures, generate tool schemas, and evaluate execution logs before implementation or optimization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated architectures may assign agents broad tool access or unsafe permissions. <br>
Mitigation: Review each design before implementation, narrow each agent's tools to the minimum required, and add approvals for code execution, file writes, API calls, notifications, and scheduling. <br>
Risk: Execution logs can include confidential or sensitive operational data. <br>
Mitigation: Avoid feeding confidential logs unless generated output files are stored, retained, and reviewed under appropriate data-handling controls. <br>
Risk: Generated plans and evaluations can be incomplete or misleading for a specific production environment. <br>
Mitigation: Validate generated architectures, schemas, and recommendations against real requirements, security boundaries, and operational constraints before deployment. <br>


## Reference(s): <br>
- [Agent Architecture Patterns Catalog](references/agent_architecture_patterns.md) <br>
- [Multi-Agent System Evaluation Methodology](references/evaluation_methodology.md) <br>
- [Tool Design Best Practices for Multi-Agent Systems](references/tool_design_best_practices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON outputs, Mermaid diagrams, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates architecture, schema, evaluation, recommendation, and roadmap files from JSON inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
