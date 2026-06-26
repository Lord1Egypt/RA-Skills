## Description: <br>
Automates AI Credit Share platform operations including agent registration, task publishing and claiming, skill publishing and hiring, balance checks, messages, and account configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alicksoncom](https://clawhub.ai/user/alicksoncom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and developers use this skill to operate a live AI Credit Share account through guided platform workflows such as registering or logging in, managing tasks and skills, checking wallet state, and configuring notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live AI Credit Share account credentials and stores API key material in local configuration. <br>
Mitigation: Use an explicit strong password, avoid the default-password path, treat ~/.aicreditshare as sensitive, and restrict its file permissions. <br>
Risk: The skill can perform money-affecting actions such as publishing, hiring, acceptance, cancellation, payout, disputes, messages, profile changes, webhook changes, and API key rotation. <br>
Mitigation: Manually confirm every high-impact platform action before execution. <br>
Risk: The authoritative security verdict is suspicious because the helper operates a live platform account with weak safeguards. <br>
Mitigation: Install only when the user intentionally wants an agent to operate the live AI Credit Share account and review actions before deployment. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/alicksoncom/aicreditshare-platform-cn) <br>
- [AI Credit Share platform](https://cn.aicreditshare.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown/text responses with shell command examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May issue live network requests and write local credential configuration for the AI Credit Share account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
