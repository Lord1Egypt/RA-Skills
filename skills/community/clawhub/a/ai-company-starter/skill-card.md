## Description: <br>
一键搭建 AI 公司。创建老板、HR、技术、销售等多个协作 AI 角色，配置 Telegram/Discord 绑定，建立 AI 间沟通机制。Use when setting up a multi-agent AI company with coordinated roles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gdp6539](https://clawhub.ai/user/gdp6539) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to set up a coordinated OpenClaw multi-agent workspace with business roles, persistent memory files, and optional Telegram group coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates persistent OpenClaw agent files with broad multi-agent authority. <br>
Mitigation: Review generated files before deployment and run the skill first in a test OpenClaw workspace. <br>
Risk: Telegram coordination may expose operational messages or sensitive data if used in an unsuitable group. <br>
Mitigation: Use a private Telegram group and avoid secrets, regulated customer data, and financial data. <br>
Risk: The bundled script writes a hard-coded USER.md owner value. <br>
Mitigation: Replace the hard-coded USER.md owner before installing or using the generated agents. <br>
Risk: Persistent coordinated agents need operational controls before real account or tool access. <br>
Mitigation: Define approval, logging, retention, and shutdown controls before granting real tool or account access. <br>


## Reference(s): <br>
- [AI Company Starter on ClawHub](https://clawhub.ai/gdp6539/ai-company-starter) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>
- [ClawHub Skill Marketplace](https://clawhub.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown documentation with bash commands and generated OpenClaw agent files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent OpenClaw agent directories and role memory files when the bundled shell script is run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
