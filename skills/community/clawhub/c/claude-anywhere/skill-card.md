## Description: <br>
Claude Anywhere connects Claude Code to Telegram, WeChat Work, and QQ so users can remotely read and write files, run commands, analyze images and files, resume sessions, and schedule tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yizhao1978](https://clawhub.ai/user/yizhao1978) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to operate Claude Code from messaging platforms for remote coding, file operations, command execution, image and file analysis, session resumption, and scheduled automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messaging users can drive Claude Code with broad local file and command authority. <br>
Mitigation: Install only where this remote control is intended, run as a dedicated unprivileged user or container, restrict the working directory, and limit bot membership. <br>
Risk: Tokens and session history can expose access or sensitive work context. <br>
Mitigation: Protect and rotate platform tokens, avoid sensitive hosts, and review /sessions exposure before enabling multi-user access. <br>
Risk: Scheduled /cron jobs can trigger unattended file and command actions. <br>
Mitigation: Disable or closely monitor /cron jobs unless unattended execution is acceptable for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yizhao1978/claude-anywhere) <br>
- [Claude Anywhere homepage](https://claudeanywhere.com/buy.html) <br>
- [QQ bot setup portal](https://q.qq.com/qqbot/openclaw/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Messaging replies with Markdown help text, code snippets, shell commands, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses can be split for platform reply limits; Pro mode enables image and file analysis, session resume, and scheduled task outputs.] <br>

## Skill Version(s): <br>
1.6.2 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
