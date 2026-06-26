## Description: <br>
Configure OpenClaw multi-agent routing for Feishu multi-account setups, including isolated agents and workspaces, Feishu account bindings, MEMORY bootstrap, memory embedding checks, and routing troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinywatermonster](https://clawhub.ai/user/tinywatermonster) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to create or repair Feishu multi-agent OpenClaw routing across multiple bot accounts while keeping each agent's workspace, persona, and memory setup isolated. It also guides troubleshooting for routing, pairing, Feishu permission, and memory embedding failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill configures Feishu app credentials and remote memory embedding credentials. <br>
Mitigation: Review each command before running it, avoid pasting app secrets or provider keys into chat or logs, and confirm the intended Feishu account IDs and agent IDs before changing persistent configuration. <br>
Risk: Persistent OpenClaw configuration changes can bind a Feishu account to the wrong agent or workspace. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before edits, validate the config, restart the gateway, probe channel status, and confirm routing with log evidence for each account. <br>
Risk: Remote memory embeddings may send workspace content to the configured provider. <br>
Mitigation: Only configure remote memory embeddings for workspace content that is acceptable to send to that provider, then verify the selected provider and embedding probe state per agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tinywatermonster/feishu-multiagent) <br>
- [OpenRouter OpenAI-compatible API endpoint](https://openrouter.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash, JSON, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes validation evidence expectations for config, gateway, channel, routing, and memory checks.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
