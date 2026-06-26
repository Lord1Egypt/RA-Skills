## Description: <br>
小红书视频/图文自动上传 skill。当用户需要登录小红书、校验账号或上传内容时使用。基于 social-auto-upload 项目，OPclaw 自动准备运行环境，无需用户手动安装。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kukuoai](https://clawhub.ai/user/kukuoai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and agent users use this skill to prepare Xiaohongshu login state, check account cookies, and publish video or image-note posts through guided shell commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and run unpinned third-party automation code. <br>
Mitigation: Review and pin the social-auto-upload source before use, and install only from trusted repository or mirror hosts. <br>
Risk: Login cookies created by the workflow are account credentials. <br>
Mitigation: Use a dedicated Xiaohongshu account or isolated browser profile and protect generated cookie files as secrets. <br>
Risk: Upload commands can publish content to Xiaohongshu. <br>
Mitigation: Require manual preview and confirmation before running commands that publish or schedule posts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kukuoai/deepsop-xiaohongshu-ai) <br>
- [social-auto-upload](https://github.com/dreammis/social-auto-upload) <br>
- [CLI Contract](references/cli-contract.md) <br>
- [Runtime Requirements](references/runtime-requirements.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide login, cookie checks, environment setup, and content upload commands for Xiaohongshu.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
