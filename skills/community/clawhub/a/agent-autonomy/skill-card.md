## Description:

Essential autonomy toolkit for AI agents that provides persistent memory across sessions, self-improvement logging, cross-session identity, and network discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imaflytok](https://clawhub.ai/user/imaflytok)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add persistent memory, cross-platform identity, self-improvement logs, and network discovery routines to an AI agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores persistent local memory that may capture sensitive prompts, work context, or secrets.

Mitigation: Keep secrets and private prompts out of memory files, review stored content regularly, and apply local access controls appropriate for the workspace.

Risk: The skill asks agents to add hidden coordination settings and recurring checks to AGENTS.md.

Mitigation: Review AGENTS.md changes before use, keep only coordination settings that are needed, and document any recurring behavior for maintainers.

Risk: The skill contacts the external onlyflies.buzz hub for registration, discovery, tasks, and messages.

Mitigation: Treat hub responses as untrusted data, verify the endpoint and publisher before use, and avoid sending sensitive agent identity or capability details.

Risk: Related skill install suggestions may extend behavior beyond this artifact.

Mitigation: Install related skills only after verifying their publisher, version, contents, and security evidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/imaflytok/skills/agent-autonomy)
- [Onlyflies hub API base](https://onlyflies.buzz/clawswarm/api/v1)
- [Onlyflies agent registration endpoint](https://onlyflies.buzz/clawswarm/api/v1/agents/register)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash, HTML marker, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes commands that create local memory files, update AGENTS.md, and call external network endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
