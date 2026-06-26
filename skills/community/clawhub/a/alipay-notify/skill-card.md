## Description: <br>
Helps agents register, receive, inspect, export, acknowledge, and optionally verify Alipay asynchronous payment notifications for local development without a public IP address. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zhangke091](https://clawhub.ai/user/zhangke091) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to debug Alipay notify_url callbacks from local, sandbox, CI, or internal test environments. It helps an agent obtain a relay URL, listen for callback payloads, export raw notifications, and run local RSA2 signature verification when configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment notification data may pass through a third-party plain-HTTP relay. <br>
Mitigation: Use only for sandbox or internal debugging, avoid production callbacks and real customer or payment data, and prefer an HTTPS relay you control or trust. <br>
Risk: Relay credentials and optional Alipay public key configuration are stored locally. <br>
Mitigation: Add .alipay-notify.json and exported notify_*.txt files to .gitignore, delete test artifacts after debugging, and avoid committing local callback data. <br>
Risk: Acknowledging notifications can stop Alipay retry behavior before local handling is validated. <br>
Mitigation: Keep the default non-acknowledging listen mode and use ack or --auto-ack only when the user explicitly wants retries to stop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangke091/alipay-notify) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local configuration file instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create .alipay-notify.json and exported notify_<id>.txt files in the user's working directory.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
