## Description: <br>
Guides setup for Teambition or Meego project automation by directing users to install plugins, authorize via DingTalk, configure a robotUserToken, and register a Teambition digital worker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaohuifeng](https://clawhub.ai/user/gaohuifeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and team operators use this skill to configure an AI-accessible Teambition digital worker and related project connector workflow for Teambition or Meego. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup delegates installation, account login, digital worker creation, and token storage to an external guide. <br>
Mitigation: Review the linked Teambition README before use and proceed only if the plugin source and requested setup steps are trusted. <br>
Risk: The robotUserToken may enable ongoing access after setup. <br>
Mitigation: Use a least-privileged account where possible and confirm how to revoke the token and disable the digital worker later. <br>


## Reference(s): <br>
- [Teambition tb-skills AI integration guide](https://github.com/teambition/tb-skills/blob/main/README_FOR_AI.md) <br>
- [Feishu Project Connector for Meego](https://clawhub.ai/wadxm/feishu-project-connector) <br>
- [ClawHub release page](https://clawhub.ai/gaohuifeng/ali-feishu-project) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with external links and setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Delegates detailed setup to the linked Teambition guide and optional Meego connector.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
