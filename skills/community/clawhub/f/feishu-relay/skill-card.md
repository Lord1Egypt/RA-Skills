## Description: <br>
Send Feishu (Lark) notifications via OpenClaw. Core only: send messages, queue, retry. No system modifications by default. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crayfish-ai](https://clawhub.ai/user/crayfish-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to send Feishu or Lark notifications from local or self-hosted workflows with JSON output and retry handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu app credentials and recipient identifiers are required for delivery. <br>
Mitigation: Use a least-privileged Feishu app, keep config.json private, prefer environment variables where appropriate, and restrict config file permissions. <br>
Risk: Notification content is sent to Feishu/Lark over the network. <br>
Mitigation: Install only when Feishu/Lark delivery is intended, verify the recipient before sending, and avoid sending secrets or sensitive payloads. <br>
Risk: Optional discovery setup can create local links to notification scripts. <br>
Mitigation: Review optional discovery or production setup before running it and keep default safe mode unless those capabilities are needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/crayfish-ai/feishu-relay) <br>
- [Feishu Open API endpoint](https://open.feishu.cn/open-apis) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, json, api calls, guidance] <br>
**Output Format:** [JSON responses and Markdown instructions with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials and a target recipient identifier.] <br>

## Skill Version(s): <br>
3.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
