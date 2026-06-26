## Description: <br>
为 OpenClaw 提供中文文本处理、翻译、拼音转换、关键词提取和文本分析能力的工具包。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utopia013-droid](https://clawhub.ai/user/utopia013-droid) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to process Chinese text, convert pinyin, extract keywords, summarize text, inspect text statistics, and call translation functions from agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence marks this release as suspicious because the package includes a mismatched installer source and broad publishing, messaging, and account-authenticated instructions. <br>
Mitigation: Review installer scripts, publishing guides, and any configured remotes before running release or account-authenticated workflows. <br>
Risk: Cloud translation features may send submitted text to third-party translation services. <br>
Mitigation: Use local processing for sensitive data or obtain approval before routing text through external translation APIs. <br>
Risk: Translation API keys and cloud credentials are required for some services. <br>
Mitigation: Store credentials in environment variables or a managed secret store, avoid committing keys, and rotate exposed credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utopia013-droid/chinese-toolkit) <br>
- [Publisher profile](https://clawhub.ai/user/utopia013-droid) <br>
- [README](artifact/README.md) <br>
- [OpenClaw integration reference](artifact/openclaw_integration.py) <br>
- [Configuration](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime functions return strings, lists, or JSON-like dictionaries depending on the command.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external translation APIs when configured; local text-processing features depend on installed Python packages.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
