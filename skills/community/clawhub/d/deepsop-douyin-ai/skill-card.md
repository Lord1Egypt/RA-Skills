## Description: <br>
抖音视频自动上传 skill。当用户需要登录抖音、校验账号或上传视频时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to prepare Douyin automation, log in through a local terminal, verify account state, and upload videos or image posts through the social-auto-upload workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automatically installs and runs external social-auto-upload automation code. <br>
Mitigation: Review the skill and the external project before installation, and use it only when that dependency chain is acceptable. <br>
Risk: The setup flow may fall back to unofficial mirrors for dependency retrieval. <br>
Mitigation: Use mirror fallback only when the mirror sources are trusted for the deployment environment. <br>
Risk: Douyin login state is stored locally and the skill can publish to a live Douyin account. <br>
Mitigation: Keep local account files protected and confirm the account, files, title, tags, and schedule before upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kukuoai/deepsop-douyin-ai) <br>
- [social-auto-upload](https://github.com/dreammis/social-auto-upload) <br>
- [CLI contract](references/cli-contract.md) <br>
- [Runtime requirements](references/runtime-requirements.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and example code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce setup commands, Douyin CLI invocations, account verification guidance, and upload parameter guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
