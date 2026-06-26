## Description: <br>
Teach OpenClaw how to work in Feishu (Lark) group chats: recognize who is talking, behave properly in groups vs DMs, respect multi-user privacy, and format messages for the platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4ier](https://clawhub.ai/user/4ier) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators connecting OpenClaw to Feishu use this skill to make an agent a competent group-chat and DM participant. It provides sender-identification setup, Feishu contact-sync guidance, group etiquette, privacy expectations, and platform formatting rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sync script can bulk-copy Feishu organization contacts into persistent agent context. <br>
Mitigation: Run it only with authorization for Feishu contact-read access, keep USER.md private, and avoid committing or sharing the generated contacts table. <br>
Risk: Scheduled contact sync can repeatedly refresh sensitive employee identifiers without further review. <br>
Mitigation: Review any cron setup before enabling it and prefer narrower on-demand lookup or limited contact export when that is sufficient. <br>
Risk: The sync script reads Feishu app credentials from the OpenClaw configuration at runtime. <br>
Mitigation: Protect the OpenClaw configuration file and grant the Feishu app only the permissions needed for the intended contact lookup. <br>


## Reference(s): <br>
- [Feishu tenant access token API endpoint](https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal) <br>
- [Feishu contact user lookup API endpoint](https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, and a Python helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update USER.md with a Feishu contacts table when the bundled sync script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
