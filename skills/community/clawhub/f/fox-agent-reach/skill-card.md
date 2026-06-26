## Description: <br>
Fox Agent Reach gives an AI agent command guidance for searching, reading, and interacting with web, social, video, code, RSS, and article platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinthqod](https://clawhub.ai/user/qinthqod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when an assistant needs to search or read supported platforms, inspect shared URLs, run diagnostics, or configure platform channels. It also provides command patterns for posting, commenting, and platform-specific setup when the user explicitly asks for those actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may require sensitive account cookies for some platforms. <br>
Mitigation: Use limited-scope or disposable accounts where possible and store cookies only in locations intended for persistent agent-reach data. <br>
Risk: The skill includes commands for posting, commenting, and publishing to supported platforms. <br>
Mitigation: Require an explicit preview and user confirmation before any public write action. <br>
Risk: The skill describes a WeChat article workflow that bypasses anti-bot controls. <br>
Mitigation: Use that workflow only when permission and a compliant access path are clear; otherwise avoid it. <br>


## Reference(s): <br>
- [Agent Reach homepage](https://github.com/Panniantong/Agent-Reach) <br>
- [Agent Reach install guide](https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline bash and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes platform-specific command examples and operational cautions for cookies, proxies, and temporary files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
