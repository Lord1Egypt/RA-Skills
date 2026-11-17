## Description:

This skill guides agents that answer questions about AgentScope, build AgentScope Python applications, inspect AgentScope APIs, and use AgentScope examples and reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wxf8126275](https://clawhub.ai/user/wxf8126275)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to get AgentScope guidance, locate relevant framework examples, inspect APIs, and draft code or configuration for agent applications. It is also useful for agents helping with multi-agent orchestration, deployment patterns, and framework-specific troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes runnable shell and Python examples that may execute code on a user's machine.

Mitigation: Review proposed commands before execution and run examples in a sandbox or minimal environment, especially on machines with secrets.

Risk: The skill recommends cloning or updating the AgentScope repository from a mutable branch.

Mitigation: Prefer pinned AgentScope versions or reviewed commit hashes instead of relying on the latest main branch.

Risk: Some example dependencies may become stale over time.

Mitigation: Review and update example dependencies before running A2UI client examples or broader framework demos.

## Reference(s):

- [AgentScope Skill Page](https://clawhub.ai/wxf8126275/skills/agentscope-skill)
- [AgentScope Documentation](https://agentscope.ai/docs/)
- [AgentScope Repository](https://github.com/agentscope-ai/agentscope)
- [Deployment Guide](references/deployment_guide.md)
- [Multi-Agent Orchestration](references/multi_agent_orchestration.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AgentScope Python examples, repository navigation guidance, API inspection commands, and implementation plans.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
