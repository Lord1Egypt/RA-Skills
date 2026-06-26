## Description: <br>
Observability and metrics for AI agents - track calls, errors, latency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nantes](https://clawhub.ai/user/nantes) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to record AI agent calls, errors, latency, and resource usage, then inspect terminal summaries or export metrics for observability workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local metric files and exports may contain sensitive labels, error details, stack traces, prompts, tokens, or customer data. <br>
Mitigation: Avoid recording secrets or private data, and review agent_metrics.json and exported files before sharing or committing them. <br>
Risk: The artifact references a PowerShell wrapper that is not present in the supplied artifact files. <br>
Mitigation: Use the included Python CLI or separately obtain and review any wrapper before execution. <br>
Risk: The tool depends on psutil for resource metrics. <br>
Mitigation: Install psutil from a trusted package source and pin or review the dependency in managed environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nantes/agent-metrics-osiris) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples; runtime metrics can be displayed as terminal text or exported as JSON or CSV.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a local agent_metrics.json file when metrics are recorded.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
