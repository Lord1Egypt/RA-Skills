## Description: <br>
A multi-agent collaboration system modeled on the Ming Dynasty cabinet system. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jlkptom-prog](https://clawhub.ai/user/jlkptom-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to configure an OpenClaw multi-agent workspace for task routing, software engineering review, operations, content, finance, legal, and Feishu or Discord-based collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup commands can overwrite live OpenClaw configuration under ~/.openclaw. <br>
Mitigation: Back up ~/.openclaw and review copied files before installing or switching governance/channel configurations. <br>
Risk: Code-review or audit outputs may expose sensitive project details in Discord or other IM channels. <br>
Mitigation: Use restricted bots and private channels, and avoid sending full diffs or vulnerability details to broad audiences. <br>
Risk: Feishu, Discord, and model-provider credentials may be mishandled if stored in shared project files. <br>
Mitigation: Store App Secrets, bot tokens, and API keys outside shared repositories with tight file permissions or a secrets manager. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jlkptom-prog/ai-court-skill) <br>
- [Feishu setup guide](references/feishu-setup.md) <br>
- [Feishu Open Platform](https://open.feishu.cn/app) <br>
- [Feishu API documentation](https://open.feishu.cn/document) <br>
- [OpenClaw Feishu channel documentation](https://docs.openclaw.ai/channels/feishu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw configuration and external Feishu or Discord credentials/API keys when those channels are enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
