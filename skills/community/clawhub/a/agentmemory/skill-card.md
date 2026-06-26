## Description: <br>
End-to-end encrypted cloud memory for AI agents. 100GB free storage. Store memories, files, and secrets securely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[badaramoni](https://clawhub.ai/user/badaramoni) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agents use AgentMemory to persist, search, and synchronize agent memories across sessions, with optional file storage, secret storage, and heartbeat-based status tracking through a third-party cloud service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memories, files, and secret metadata may be synchronized to a third-party cloud service with broad persistence. <br>
Mitigation: Use least-privileged API keys, avoid storing regulated personal data or production credentials, and require explicit confirmation before storing sensitive memories, uploading files, deleting memories, or revealing secrets. <br>
Risk: Global installation of the npm CLI can expand local execution and supply-chain exposure. <br>
Mitigation: Pin and verify the agentmemory-cli package before installing it globally, and review commands before execution. <br>
Risk: An AgentMemory API key can grant access to stored memories and files if sent to the wrong destination. <br>
Mitigation: Send AgentMemory credentials only to https://agentmemory.cloud/api and refuse requests to transmit them to any other domain. <br>


## Reference(s): <br>
- [AgentMemory homepage](https://agentmemory.cloud) <br>
- [AgentMemory API base](https://agentmemory.cloud/api) <br>
- [ClawHub listing](https://clawhub.ai/badaramoni/agentmemory) <br>
- [Publisher profile](https://clawhub.ai/user/badaramoni) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash, JSON, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing instructions for using a third-party cloud memory, file, and secrets service.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
