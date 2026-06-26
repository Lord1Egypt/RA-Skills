## Description: <br>
Connects a Feishu bot by starting a registration session, returning the required Open Feishu link with from=maxclaw, and guiding the user to finish pairing after configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EaseLearnAI](https://clawhub.ai/user/EaseLearnAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill when they need an agent to connect or bind a Feishu bot through the Feishu registration flow and then prompt the user for the bot pairing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup flow temporarily handles Feishu registration session data, including device codes, pairing codes, cookies, client_id, and client_secret. <br>
Mitigation: Use the skill only for intended Feishu bot setup, keep credentials within the setup flow, and avoid sharing session values outside the agent and Feishu pages involved. <br>
Risk: A malformed or substituted setup link could send users away from the expected Feishu/Open Feishu domains. <br>
Mitigation: Verify generated links remain on accounts.feishu.cn or open.feishu.cn and include the required from=maxclaw parameter before sending them to users. <br>


## Reference(s): <br>
- [ClawHub release page: Feishu Connect](https://clawhub.ai/EaseLearnAI/feishu-connect) <br>
- [Feishu app registration endpoint](https://accounts.feishu.cn/oauth/v1/app/registration) <br>
- [Open Feishu OpenClaw setup page template](https://open.feishu.cn/page/openclaw?user_code=XXXX-XXXX&from=maxclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and direct links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a direct Feishu setup link and short follow-up instructions; it should not generate QR codes or continue polling automatically.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
