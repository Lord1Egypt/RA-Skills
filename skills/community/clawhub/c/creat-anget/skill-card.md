## Description: <br>
Creates standalone OpenClaw agents with isolated workspaces, configuration, identity, memory, and optional Feishu bot bindings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[song5749](https://clawhub.ai/user/song5749) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create long-running, isolated OpenClaw agents for projects, customer support, HR, internal IT, or other dedicated workflows. It can also configure Feishu routing when separate bot identities are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change local OpenClaw configuration and create persistent agent state. <br>
Mitigation: Review the openclaw.json diff and generated workspace before restarting OpenClaw. <br>
Risk: The skill may copy the main agent's auth profiles or models into a new agent directory. <br>
Mitigation: Copy shared credentials only when intentional, and remove credentials that the new agent should not use. <br>
Risk: Feishu app secrets may be written into local configuration. <br>
Mitigation: Prefer environment variables or a protected secret store, and restrict permissions on configuration files containing Feishu secrets. <br>


## Reference(s): <br>
- [Standalone Agent Guide](references/standalone-agent-guide.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/song5749/creat-anget) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and Python helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or proposes local OpenClaw agent directories, workspace files, openclaw.json changes, and optional Feishu account configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
