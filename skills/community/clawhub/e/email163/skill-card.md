## Description: <br>
基于Go的163邮箱SMTP发送工具，支持HTML格式邮件、多收件人、命令行发送和发送日志记录。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x760591483](https://clawhub.ai/user/x760591483) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators can use this skill to compile and run a 163 SMTP email sender for scripted notifications, HTML messages, and multi-recipient mail workflows. It requires a 163 email address and authorization code supplied through environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles SMTP credentials through environment variables. <br>
Mitigation: Use a dedicated 163 SMTP authorization code, keep credentials out of shared shell profiles and logs, and rotate the authorization code if it may have been exposed. <br>
Risk: Send logs can include recipient addresses, subjects, message content, and send results. <br>
Mitigation: Review logging settings before use, store logs in a private location, and avoid sending confidential content unless logs are protected or redacted. <br>
Risk: The SMTP connection code disables TLS certificate verification. <br>
Mitigation: Review and update the TLS configuration before relying on this skill for sensitive or production email workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/x760591483/email163) <br>
- [Publisher profile](https://clawhub.ai/user/x760591483) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text, Files, Guidance] <br>
**Output Format:** [Markdown usage guidance, command-line flags, SMTP email output, status text, and dated log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EMAIL163_ADDRESS and EMAIL163_PASSWORD environment variables; sends through smtp.163.com and records send attempts to date-based log files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
