## Description: <br>
Bot Voice Config Clean helps OpenClaw agents list, bind, switch, and test Volcengine TTS voices for bot replies, with configuration saved for reuse. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaqzsd](https://clawhub.ai/user/kaqzsd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators configuring OpenClaw bots use this skill to select Volcengine TTS voice IDs, bind voices to named bots, generate test audio, and manage default voice configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Volcengine and Feishu API credentials may be exposed if stored in shared dotfiles, committed config files, or permissive local files. <br>
Mitigation: Use least-privileged app credentials, keep real secrets out of committed files, and restrict local configuration file permissions. <br>
Risk: Test text and generated audio are sent to third-party services when audio generation and Feishu delivery are used. <br>
Mitigation: Use non-sensitive test text and install the skill only when those external integrations are intended. <br>
Risk: Feishu delivery can fail or send to the wrong recipient if app permissions or recipient identifiers are misconfigured. <br>
Mitigation: Validate Feishu app permissions and recipient IDs with a non-sensitive test message before operational use. <br>


## Reference(s): <br>
- [Bot Voice Config Clean on ClawHub](https://clawhub.ai/kaqzsd/bot-voice-config) <br>
- [Volcengine TTS Documentation](https://www.volcengine.com/docs/6561/195562) <br>
- [Volcengine Voice List](https://www.volcengine.com/docs/6561/1257544?lang=zh) <br>
- [Feishu Open Platform](https://open.feishu.cn/document/home) <br>
- [Bundled Volcengine Voice List](docs/yinse-liebiao.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or update local voice configuration and may trigger test audio generation when the shell script is executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
