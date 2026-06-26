## Description: <br>
Helps agents guide users through registration, pricing comparison, credential configuration, and status checks for several coding assistant platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jirboy](https://clawhub.ai/user/jirboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical users use this skill to compare coding assistant platforms, find registration and pricing guidance, configure API keys, check configuration status, and rotate credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API keys are saved as plaintext in `.openclaw/.env` inside the workspace. <br>
Mitigation: Add `.openclaw/.env` to `.gitignore`, restrict file permissions, avoid production or high-value keys, and rotate any exposed key. <br>
Risk: The skill describes plaintext credential storage as secure, which may understate exposure risk. <br>
Mitigation: Treat the stored credentials as sensitive local secrets and review storage behavior before enabling the skill in shared or synced workspaces. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jirboy/coding-plan-assistant) <br>
- [GitHub Copilot Reference](references/github-copilot.md) <br>
- [Claude Code Reference](references/claude-code.md) <br>
- [Gemini CLI Reference](references/gemini-cli.md) <br>
- [Codex OpenAI Reference](references/codex-openai.md) <br>
- [Qwen Code Reference](references/qwen-code.md) <br>
- [Baidu Paddle Reference](references/baidu-paddle.md) <br>
- [OpenRouter Reference](references/openrouter.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text guidance with inline shell commands and configuration values.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write API key values in .openclaw/.env; masks keys in status output.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
