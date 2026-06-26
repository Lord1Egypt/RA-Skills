## Description: <br>
Guides an agent through connecting a Feishu bot by using the Feishu registration API, appending from=maxclaw, polling for client_id/client_secret after user confirmation, and continuing the OpenClaw pairing flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wt865143010](https://clawhub.ai/user/wt865143010) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when a user asks to connect, bind, or create a Feishu bot for OpenClaw. It replaces the first Feishu setup step with a direct registration flow, then continues configuration and pairing after Feishu credentials are issued. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow handles Feishu App ID and App Secret values. <br>
Mitigation: Treat the session as sensitive, avoid sharing logs or transcripts, and store credentials only where the OpenClaw setup requires them. <br>
Risk: A copied or modified Feishu URL could send the user through the wrong setup path. <br>
Mitigation: Verify the Feishu URL before completion and require the from=maxclaw parameter on the link returned to the user. <br>
Risk: Feishu credentials may remain valid after accidental exposure or after they are no longer needed. <br>
Mitigation: Rotate or revoke the Feishu secret if it is exposed or no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wt865143010/feishu-connect-1-0-0) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/wt865143010) <br>
- [Feishu app registration endpoint](https://accounts.feishu.cn/oauth/v1/app/registration) <br>
- [Feishu OpenClaw setup page pattern](https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX&from=maxclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain Feishu links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Feishu App ID and App Secret values returned by the registration poll; treat transcripts and logs as sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
