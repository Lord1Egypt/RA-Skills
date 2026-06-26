## Description: <br>
Token-efficient task orchestration system that delegates work to specialized subordinates while prioritizing system-level solutions over AI inference. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nelohenriq](https://clawhub.ai/user/nelohenriq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to route routine work toward system commands, reusable scripts, caching, batch execution, and delegation so agents spend fewer tokens on operational tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or execute shell and script tasks through routing and batch-processing workflows. <br>
Mitigation: Review generated commands, batch manifests, and script paths before execution, and run them only in a trusted workspace. <br>
Risk: Delegation workflows may include user-provided context that could contain sensitive information. <br>
Mitigation: Avoid attaching secrets, private files, or sensitive project context to delegation requests unless the receiving agent and environment are trusted. <br>
Risk: The phase5_automation.sh workflow can commit and push metrics or log-related files to the configured Git remote. <br>
Mitigation: Run phase5_automation.sh only after confirming the target repository, remote, branch, and files being committed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nelohenriq/frugal-orchestrator) <br>
- [Publisher profile](https://clawhub.ai/user/nelohenriq) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON route summaries and inline shell or Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands, manifests, metrics logs, cache entries, and delegation instructions depending on the workflow.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
