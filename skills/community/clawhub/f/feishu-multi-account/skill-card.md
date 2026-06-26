## Description: <br>
Supports configuring independent Feishu bot accounts for multiple OpenClaw sub-agents so messages route to the account-bound agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhili007](https://clawhub.ai/user/zhili007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure multiple Feishu bot accounts, bind each account to the intended sub-agent, and troubleshoot message routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu AppSecret values may be exposed if copied into source control, logs, or screenshots while following the configuration guide. <br>
Mitigation: Back up openclaw.json, keep AppSecret values out of source control, logs, and screenshots, and rotate any secret that may have been exposed. <br>
Risk: Incorrect account-to-agent bindings can route Feishu messages to the wrong OpenClaw sub-agent. <br>
Mitigation: Verify each Feishu account is bound to the intended agent, ensure bindings are top-level configuration entries, restart the gateway, and confirm routing in logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhili007/feishu-multi-account) <br>
- [Skill guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes OpenClaw openclaw.json account, binding, agent, restart, and log-check guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
