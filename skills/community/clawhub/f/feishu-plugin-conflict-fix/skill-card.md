## Description: <br>
飞书插件工具冲突修复工具。解决 feishu_chat 命名冲突、TTS 语音配置、多 Bot 工具隔离等问题。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rfdiosuao](https://clawhub.ai/user/rfdiosuao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose and resolve Feishu/OpenClaw plugin conflicts, disable unwanted TTS behavior, and configure tool isolation for multiple bots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reset commands can remove Feishu plugin files and restart OpenClaw services if a user chooses to run them. <br>
Mitigation: Back up ~/.openclaw/openclaw.json, list matching ~/.openclaw/plugins/feishu* paths before deletion, and confirm a gateway restart window before applying reset steps. <br>
Risk: Installing or enabling @larksuite/openclaw-lark can grant Feishu permissions in the target environment. <br>
Mitigation: Verify the package source and review the requested Feishu permissions before installation or reconfiguration. <br>


## Reference(s): <br>
- [Official Plugin Usage Guide](https://my.feishu.cn/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh) <br>
- [Streaming Reply Configuration](https://www.feishu.cn/docx/Qv3fdMljgoUjYJx5cwAc3tinnfc) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose OpenClaw configuration changes and service restart commands for user review.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
