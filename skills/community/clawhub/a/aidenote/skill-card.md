## Description: <br>
智能录音笔记管理助手 - AI 自动转写和总结录音，支持知识库管理和语义搜索 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajingmiao](https://clawhub.ai/user/ajingmiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query, search, summarize, and inspect AiDeNote/SlonAide recording notes through OpenClaw. It can also help install or check a local remote bridge so the AiDeNote mobile app can connect to the user's OpenClaw instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bridge setup executes downloaded installer scripts and creates a persistent local remote bridge. <br>
Mitigation: Install only when the AiDeNote mobile app needs to connect to this computer's OpenClaw instance; review the installer source and confirm how to disable or uninstall the login-start service before enabling it. <br>
Risk: Connection-test output may expose partial credential material. <br>
Mitigation: Avoid sharing connection-test output and treat logs or screenshots from setup and testing as sensitive. <br>
Risk: The skill requires sensitive API credentials to access private recording notes. <br>
Mitigation: Use a dedicated AiDeNote/SlonAide API key, store it through OpenClaw configuration, and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ajingmiao/aidenote) <br>
- [AiDeNote web app](https://h5.aidenote.cn/) <br>
- [SlonAide web app](https://h5.slonaide.cn/) <br>
- [Skill README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-like text responses from OpenClaw tools, including note summaries, note details, status messages, setup guidance, and command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured API key for note access; bridge setup is limited to macOS and Windows in the artifact documentation.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata; artifact frontmatter and package.json report 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
