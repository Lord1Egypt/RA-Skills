## Description: <br>
Guides users through creating a Feishu robot, connecting it to OpenClaw, and binding it to a dedicated Agent in a Windows OpenClaw workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[song123-wq](https://clawhub.ai/user/song123-wq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create a Feishu bot, collect its App ID and App Secret, configure an OpenClaw Agent workspace, bind bot routing, restart the gateway, and verify that messages reach the new Agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires handling a Feishu App Secret. <br>
Mitigation: Keep the App Secret in a protected secret store or secured local configuration, and do not paste it into chat or commit it to files. <br>
Risk: OpenClaw configuration changes can persist through created agent folders, memory files, and bot routing. <br>
Mitigation: Review the planned OpenClaw changes before applying them and remove or disable created folders, memory, and routing when no longer needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/song123-wq/feishu-robot-creater-for-26462-final) <br>
- [Feishu OpenClaw application creation page](https://open.feishu.cn/page/openclaw?form=multiAgent) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with PowerShell commands and configuration checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only output; users must apply Feishu and OpenClaw configuration changes in their own environment.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
