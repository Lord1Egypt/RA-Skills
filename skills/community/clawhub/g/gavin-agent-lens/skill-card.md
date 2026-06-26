## Description: <br>
Track AI agent API calls, analyze token usage, and optimize costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lrg913427-dot](https://clawhub.ai/user/lrg913427-dot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use Agent Lens to monitor LLM API calls, token usage, latency, errors, and estimated costs across agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to install an external GitHub package that was not included in the scanned artifact. <br>
Mitigation: Review or pin the package before installation and install it in a virtual environment. <br>
Risk: The local SQLite trace database can contain usage, model, cost, timing, and error information. <br>
Mitigation: Treat the database as potentially sensitive and use the documented cleanup command when retention is no longer needed. <br>


## Reference(s): <br>
- [Agent Lens on ClawHub](https://clawhub.ai/lrg913427-dot/gavin-agent-lens) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include local CLI commands, Python integration snippets, and cost-analysis workflows.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
