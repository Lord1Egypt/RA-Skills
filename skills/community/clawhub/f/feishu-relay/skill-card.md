## Description:

Send Feishu (Lark) notifications via OpenClaw, including message delivery, structured JSON output, and retry behavior without default system modifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crayfish-ai](https://clawhub.ai/user/crayfish-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send Feishu or Lark notifications from local, shared-hosting, or self-hosted workflows. It is best suited for agent status updates, operational alerts, and scripted notification delivery where Feishu credentials and recipient IDs are already available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Message content is sent to Feishu/Lark through the Feishu Open API.

Mitigation: Use the skill only for content appropriate to send to Feishu and confirm the configured recipient before sending alerts or operational messages.

Risk: Feishu app credentials can be exposed if environment variables or config.json are mishandled.

Mitigation: Keep FEISHU_APP_SECRET private, restrict config.json permissions, and avoid logging or sharing credential-bearing configuration.

Risk: The opt-in discovery script can link executable notify scripts from other OpenClaw workspaces or skills.

Mitigation: Do not run scripts/install-discovery.sh unless every scanned workspace and skill has been reviewed and trusted.

## Reference(s):

- [Feishu Open APIs](https://open.feishu.cn/open-apis)
- [ClawHub Skill Page](https://clawhub.ai/crayfish-ai/skills/feishu-relay)
- [README](artifact/README.md)
- [Skill Metadata](artifact/skill.json)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Configuration]

**Output Format:** [CLI output with optional structured JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends message content to Feishu through open.feishu.cn and requires Feishu app credentials plus a recipient identifier.]

## Skill Version(s):

3.2.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
