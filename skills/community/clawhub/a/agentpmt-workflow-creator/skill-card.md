## Description:

AgentPMT Workflow Creator helps agents build and manage multi-step AI workflows that orchestrate tools, prompts, loops, branches, and human notifications into reusable DAG pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to create, validate, update, publish, remix, and manage AgentPMT workflow skills for multi-step business processes. It is intended for agents that need AgentPMT-specific workflow schema, action names, and invocation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup examples include unpinned npx commands.

Mitigation: Prefer OpenClaw or ClawHub installation paths, or verify and pin the installer and source revision before use.

Risk: Workflow update, publish, delete, and restore actions can change or remove workflow drafts or published snapshots.

Mitigation: Require explicit user approval before these actions and confirm the current draft revision and latest saved workflow state.

Risk: Workflow nodes may call external marketplace tools and handle credentials or payment-related setup.

Mitigation: Keep inputs scoped to the task and avoid placing account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/agentpmt-workflow-creator)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/agentpmt-workflow-creator)
- [Generated action schema](artifact/schema.md)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [What is AgentPMT](https://clawhub.ai/agentpmt/what-is-agentpmt)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with JSON action payloads and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to guide AgentPMT-hosted remote tool calls and workflow draft management.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
