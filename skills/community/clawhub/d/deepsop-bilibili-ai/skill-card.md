## Description: <br>
Bilibili 视频自动上传 skill。当用户需要登录 Bilibili、校验账号或上传视频时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and operators use this skill to prepare a local social-auto-upload environment, log in to Bilibili, validate account state, and upload videos with title, description, category, tags, and optional schedule settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can clone and run the external social-auto-upload project and download dependencies. <br>
Mitigation: Install only after reviewing and trusting the external project and dependency source; avoid third-party mirror fallback unless those sources are trusted. <br>
Risk: The skill operates a Bilibili account using local login state. <br>
Mitigation: Confirm the exact account before login, account checks, or upload commands, and keep login actions in a local interactive terminal. <br>
Risk: The skill can publish or schedule videos without a clearly required final confirmation step. <br>
Mitigation: Before upload, verify the video file, title, description, tags, category, schedule, and whether the action will publish or save as a draft. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/kukuoai/deepsop-bilibili-ai) <br>
- [social-auto-upload project](https://github.com/dreammis/social-auto-upload) <br>
- [Runtime requirements](references/runtime-requirements.md) <br>
- [CLI contract](references/cli-contract.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and command parameter guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local setup, login, account check, and upload command sequences for a user-selected Bilibili account and video file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
