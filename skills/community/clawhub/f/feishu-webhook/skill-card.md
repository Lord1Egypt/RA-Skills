## Description: <br>
Send Markdown-formatted rich text messages to Feishu channels or DMs through a webhook with heredoc input support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[talentestors](https://clawhub.ai/user/talentestors) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to send Markdown-formatted notifications, alerts, and reports to Feishu channels or DMs from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages are sent to the configured Feishu destination, so sensitive or private content can be exposed if the webhook points to the wrong channel or DM. <br>
Mitigation: Verify the webhook destination before use and only send secrets, personal data, or private reports when they are intended for that Feishu destination. <br>
Risk: Webhook URLs and signing secrets can grant posting access if they are stored or shared carelessly. <br>
Mitigation: Keep FEISHU_WEBHOOK_URL and FEISHU_WEBHOOK_SECRET out of source control and provide them through protected environment configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/talentestors/feishu-webhook) <br>
- [Project homepage](https://github.com/talentestors/feishu-webhook) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown content sent through stdin with short terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FEISHU_WEBHOOK_URL and optionally FEISHU_WEBHOOK_SECRET in the environment.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
