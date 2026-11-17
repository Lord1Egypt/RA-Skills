## Description:

Agent Create Config guides an OpenClaw user through collecting requirements, generating configuration files, registering a persistent agent, binding Feishu channels, restarting services, and validating delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moistenxx](https://clawhub.ai/user/moistenxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to coordinate the creation and launch of new OpenClaw agents, including workspace files, agent registration, Feishu binding, gateway restart, validation, and delivery confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide creation of persistent OpenClaw agents and workspace files.

Mitigation: Use it only in an intended OpenClaw environment and confirm each filesystem write, agent registration, and gateway restart before applying changes.

Risk: Feishu bot tokens, app IDs, app secrets, and account bindings may be exposed if entered directly into shell commands or logs.

Mitigation: Use a secret manager or masked prompt where possible, and avoid shell history or logging that records credentials.

Risk: Generated agents may rely on mutable BOOTSTRAP.md and memory files.

Mitigation: Review bootstrap and memory files as untrusted content before allowing a generated agent to act on them.

Risk: Administrator-level bindings can grant broad access.

Mitigation: Assign only the minimum account privileges needed for the target agent and avoid administrator bindings unless they are required.

## Reference(s):

- [Merged Process Reference](references/MERGED_PROCESS.md)
- [ClawHub Skill Page](https://clawhub.ai/moistenxx/skills/agent-create-config)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces OpenClaw agent setup guidance and checklists; it does not itself verify external service credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
