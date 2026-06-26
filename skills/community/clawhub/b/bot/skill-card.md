## Description: <br>
Bot is a local-first framework for observable, composable agents with policy-guarded execution on ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenticio](https://clawhub.ai/user/agenticio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run local-first single-agent and multi-agent workflows with observable reasoning, capability-aware tools, and policy-guarded local execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The memory helper can access files outside the advertised memory folder. <br>
Mitigation: Do not pass untrusted role or agent IDs to memory helpers until path validation is added. <br>
Risk: The policy executor provides local policy checks but is not OS-level sandboxing. <br>
Mitigation: Register only trusted local callables and do not treat policy checks as a sandbox boundary. <br>
Risk: The optional local monitor can expose prompt and run data on its local web view. <br>
Mitigation: Use the monitor only with non-sensitive prompts and keep it bound to 127.0.0.1. <br>
Risk: Dependency installation executes package installation in the active Python environment. <br>
Mitigation: Install only inside a virtual environment before running examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agenticio/bot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and Python examples; example runs can produce local JSON and HTML monitor output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Core demos run locally; the optional monitor binds to 127.0.0.1 when started.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
