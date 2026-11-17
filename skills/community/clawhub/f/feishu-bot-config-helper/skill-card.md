## Description:

Helps configure Feishu bots by parsing bot setup details, matching an Agent profile, updating OpenClaw configuration, creating workspaces, restarting Gateway, and returning a setup report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebao360](https://clawhub.ai/user/jiebao360)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to set up Feishu bot Agents from chat-provided configuration details and generate local OpenClaw routing, workspace, and account settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide Feishu App Secrets during configuration, which can expose production credentials through chat or logs.

Mitigation: Use test credentials where possible, avoid pasting production secrets into retained chat or logs, and rotate any credential that may have been exposed.

Risk: The installer fetches mutable remote code and executes package installation steps.

Mitigation: Review the installer before running it and pin installation to a trusted commit or release.

Risk: Generated Feishu account settings may create broad access by default, including wildcard direct-message allowlists and open group policy.

Mitigation: Back up openclaw.json, review generated Agent permissions, replace wildcard allowFrom with explicit trusted users, and restrict broad skills such as all unless required.

Risk: The configurator restarts Gateway, which can interrupt active service.

Mitigation: Plan Gateway restart downtime and validate the generated configuration before restarting production services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiebao360/skills/feishu-bot-config-helper)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Feishu Open Platform](https://open.feishu.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code, shell commands, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce setup reports and local OpenClaw configuration changes when executed by the user or host environment.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
