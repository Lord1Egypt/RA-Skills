## Description: <br>
Captures learnings, errors, user corrections, and feature requests so agents can improve future project work and promote reusable knowledge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunyue1977](https://clawhub.ai/user/sunyue1977) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to record failures, corrections, feature requests, and reusable lessons in structured markdown logs. It supports reviewing and promoting high-value learnings into project or agent memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Durable learning logs may capture secrets, customer data, private URLs, raw prompts, or full command outputs. <br>
Mitigation: Require agents to summarize and redact sensitive content before writing .learnings entries, and keep .learnings out of version control unless each entry is intentionally shareable. <br>
Risk: Optional hooks can automatically remind or react during agent sessions, increasing the chance that broad task context is logged. <br>
Mitigation: Enable hooks only after reviewing their behavior and scoping logging rules for the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sunyue1977/feihong-self-improving-agent) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local learning, error, feature-request, and optional skill-template files when followed by an agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
