## Description:

BOT is a local-first framework for observable, composable agents with policy-guarded execution on ClawHub.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[agenticio](https://clawhub.ai/user/agenticio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use BOT to prototype local single-agent and multi-agent workflows with observable reasoning traces, capability-aware tool registration, policy-guarded local execution, and a local thought-tree monitor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Policy-guarded execution is not a security boundary and should not be relied on to block network, filesystem, subprocess, or other side effects from untrusted tools.

Mitigation: Install and run only in an isolated virtual environment, review registered tools before use, and use separate operating-system controls for untrusted execution.

Risk: The local web monitor can expose sensitive prompts, thoughts, or outputs if used with confidential data.

Mitigation: Run the monitor only when needed, keep it bound to local access, avoid secrets or sensitive prompts, and stop it after inspection.

Risk: Local memory storage is weak for untrusted input and may be affected by unsafe agent identifiers.

Mitigation: Validate or normalize agent identifiers before memory access and use a restricted memory directory for each test environment.

## Reference(s):

- [BOT on ClawHub](https://clawhub.ai/agenticio/skills/bot)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local execution guidance, example commands, agent configuration details, and implementation code.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
