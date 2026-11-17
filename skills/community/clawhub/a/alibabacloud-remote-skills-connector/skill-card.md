## Description: <br>
Connects an agent to Alibaba Cloud AgentHub-hosted remote skills for hosted skill discovery, credential preparation, A2A task communication, and task continuation without operating cloud resources locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to route Alibaba Cloud resource inspection, diagnosis, auditing, creation, deployment, configuration, update, scaling, restart, repair, restore, and deletion requests to matching Alibaba Cloud AgentHub-hosted remote agents. It also supports capability onboarding, credential preparation, task continuation, and connector troubleshooting while keeping user-facing interactions in Simplified Chinese. <br>

### Deployment Geography for Use: <br>
China (Alibaba Cloud China site only) <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an Alibaba Cloud hosted remote agent handle cloud tasks using the user's selected Alibaba credentials. <br>
Mitigation: Install only for intended Alibaba Cloud remote-agent workflows, prefer OAuth or an existing aliyun CLI profile, review approval pages carefully, and avoid putting secrets in task messages. <br>
Risk: Credential, network, and local state handling are sensitive even though the scanner verdict is clean. <br>
Mitigation: Use the documented credential sources and strict HTTPS workflow, keep credentials out of prompts and task messages, and rely on the connector's managed input and task-state boundaries. <br>


## Reference(s): <br>
- [Security Boundaries](references/security-boundaries.md) <br>
- [A2A Runtime Reference](references/a2a-proxy.md) <br>
- [Hosted Skill Catalog](references/hosted-skill-catalog.md) <br>
- [File State-Machine Contract](references/file-state-machine.md) <br>
- [RAM Authorization Behavior](references/ram-policies.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-remote-skills-connector) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with inline shell commands and JSON status snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [User-facing responses are in Simplified Chinese; cloud-resource actions are delegated to selected Alibaba Cloud remote agents.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
