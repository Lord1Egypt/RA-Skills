## Description:

End-to-end encrypted cloud memory for AI agents. 100GB free storage. Store memories, files, and secrets securely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[badaramoni](https://clawhub.ai/user/badaramoni)

### License/Terms of Use:


## Use Case:

External developers and agent users use AgentMemory to store, search, synchronize, and retrieve agent memories, files, heartbeat state, and secrets through a cloud service and CLI/API workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send selected memories, files, metadata, heartbeat status, and secret data to agentmemory.cloud.

Mitigation: Use the skill only with explicit authorization for the data being synchronized, and avoid storing sensitive personal or work data unless that transfer is approved.

Risk: The artifact documents mutable installation paths such as curl-based skill installation and global npm installation.

Mitigation: Prefer pinned and locally reviewed installation artifacts before enabling the skill or CLI in an agent environment.

Risk: The skill supports storing and retrieving secrets, including third-party API keys and credentials.

Mitigation: Do not store third-party API keys or production credentials unless policy permits it, and restrict AgentMemory API keys to requests sent only to https://agentmemory.cloud/api.

## Reference(s):

- [AgentMemory ClawHub Listing](https://clawhub.ai/badaramoni/skills/agentmemory)
- [AgentMemory Homepage](https://agentmemory.cloud)
- [AgentMemory API Base](https://agentmemory.cloud/api)
- [AgentMemory Documentation](https://agentmemory.cloud/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to call a third-party cloud API and optionally install a CLI.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
