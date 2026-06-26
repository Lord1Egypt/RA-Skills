## Description: <br>
Guides agents through installing, configuring, authenticating, and verifying lark-cli for Feishu/Lark, including browser-based OAuth handoff steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cosmofang](https://clawhub.ai/user/cosmofang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to set up lark-cli, configure Feishu/Lark app credentials, complete OAuth in a browser, and verify available Lark agent skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup can lead users to install global tooling and global agent skills on the host. <br>
Mitigation: Install only when Feishu/Lark CLI setup is intended, prefer non-sudo npm permission fixes, and confirm global skill installation is acceptable before proceeding. <br>
Risk: OAuth authorization can grant broad access to Feishu/Lark workspace data. <br>
Mitigation: Grant only the scopes needed for the intended workflow and use domain-specific login when broad access is unnecessary. <br>
Risk: After authentication, lark-cli commands can send messages, create documents, modify tasks, or change workspace data. <br>
Mitigation: Use dry-run before commands with side effects and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cosmofang/feishu-cli-setup) <br>
- [larksuite/cli GitHub repository](https://github.com/larksuite/cli) <br>
- [Feishu Open Platform apps](https://open.feishu.cn/app) <br>
- [Node.js](https://nodejs.org) <br>
- [npm EACCES permission guidance](https://docs.npmjs.com/resolving-eacces-permissions-errors) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown-like text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese prompt output; includes dry-run guidance for write operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
