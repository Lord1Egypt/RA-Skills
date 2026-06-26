## Description: <br>
飞牛论坛(club.fnnas.com)自动签到，支持手动或定时运行，并在需要时使用百度 OCR 处理验证码。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[OneTian1211](https://clawhub.ai/user/OneTian1211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation operators use this skill to configure credentials, install Node.js dependencies, run daily sign-in for club.fnnas.com, and optionally schedule it with OpenClaw cron. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a forum username and password plus Baidu OCR API credentials. <br>
Mitigation: Use dedicated credentials where possible, store them only in trusted ClawHub or local configuration, and rotate them when the skill is no longer used. <br>
Risk: CAPTCHA images may be sent to Baidu OCR, and OCR tokens are cached locally. <br>
Mitigation: Install only if this data flow is acceptable, keep token cache files out of shared folders and source control, and delete cached files when disabling the skill. <br>
Risk: Forum cookies are saved locally for session reuse. <br>
Mitigation: Keep the configured data directory private, exclude cache files from source control, and clear cookies if account access changes. <br>
Risk: A cron schedule can run the sign-in automatically. <br>
Mitigation: Review the OpenClaw cron schedule, timezone, and session before enabling unattended execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/OneTian1211/fnclub-signer) <br>
- [Publisher profile](https://clawhub.ai/user/OneTian1211) <br>
- [飞牛论坛](https://club.fnnas.com/) <br>
- [百度 AI 开放平台](https://ai.baidu.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON status output from the Node.js script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires forum credentials and Baidu OCR API keys; writes local cookie and OCR token cache files when used.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
