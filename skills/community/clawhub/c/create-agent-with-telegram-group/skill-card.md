## Description: <br>
Creates a new OpenClaw agent, binds it to a dedicated Telegram group, provisions an isolated workspace, and verifies no-mention group replies after explicit user approval for privileged actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sheetaa](https://clawhub.ai/user/Sheetaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to provision one dedicated agent per Telegram group, bind the group to the agent, initialize workspace files, and confirm the agent can reply without a mention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify persistent OpenClaw routing configuration and bind a Telegram group to a new or updated agent. <br>
Mitigation: Require explicit confirmation before modifying openclaw.json, and review the agent name, model, chat_id, workspace, backup path, and no-mention reply mode before approval. <br>
Risk: Telegram group setup may require browser automation from a logged-in user account. <br>
Mitigation: Proceed only when the user is comfortable supervising the browser flow, and pause for manual confirmation or captcha steps when needed. <br>
Risk: Initialization files can contain personal or operational details. <br>
Mitigation: Avoid storing secrets or unnecessary personal data in USER.md, IDENTITY.md, or SOUL.md. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown status summary with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes agent name, model, workspace, Telegram group, chat_id, binding status, reply mode, initialized files, verification status, and next step.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
