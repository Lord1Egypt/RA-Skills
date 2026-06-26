## Description: <br>
Wire a Fieldy webhook transform into Moltbot hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrzilvis](https://clawhub.ai/user/mrzilvis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to connect Fieldy transcript webhooks to Moltbot Gateway so wake-word-triggered transcript text can start a Fieldy agent run. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fieldy transcript text is persisted locally under the workspace, including transcripts that do not contain the wake word. <br>
Mitigation: Review or edit src/fieldy-webhook.js before deployment to disable logging, restrict logging to wake-word matches, redact transcript text, or add retention limits. <br>
Risk: Webhook tokens may be exposed more easily when passed as query parameters. <br>
Mitigation: Use a strong webhook token and prefer the Authorization header when the webhook provider supports it. <br>
Risk: A valid webhook request can trigger a Fieldy agent run. <br>
Mitigation: Limit the target agent's authority and review the Moltbot webhook mapping before enabling the endpoint. <br>


## Reference(s): <br>
- [Moltbot Webhooks documentation](https://docs.molt.bot/automation/webhook.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a JavaScript webhook transform that logs transcript text locally and returns agent trigger payloads when wake words are detected.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
