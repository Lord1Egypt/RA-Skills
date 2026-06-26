## Description: <br>
Creates and configures multiple isolated Feishu bots with separate memory, workspace, model settings, personality files, and Feishu application credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lcz5221-svg](https://clawhub.ai/user/lcz5221-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to batch-create and manage multiple Feishu-connected OpenClaw agents with independent identities, workspaces, routing, credentials, and model configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow persists bot and gateway configuration changes, including Feishu credentials and routing settings. <br>
Mitigation: Back up ~/.openclaw/openclaw.json before use, run the setup only with trusted configuration files, and review generated account and route entries before restarting the gateway. <br>
Risk: Broad default access settings may allow unintended users to interact with bots. <br>
Mitigation: Tighten each bot with allowlists or mention requirements before production use, then verify gateway logs for blocked or unexpected senders. <br>
Risk: Configuration files contain app secrets, encryption keys, and verification tokens. <br>
Mitigation: Protect generated and input configuration files, avoid committing secrets, and store credentials using the deployment environment's approved secret-handling process. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lcz5221-svg/feishu-duoge002) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Setup script](artifact/scripts/setup_bots.py) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON configuration examples, shell commands, and a Python setup script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local OpenClaw configuration and per-agent workspace files when the setup script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, artifact _meta.json, and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
