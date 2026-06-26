## Description: <br>
Codeflow streams coding agent sessions (Claude Code, Codex, Gemini CLI, etc.) to Discord or Telegram in real-time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[subjadeites](https://clawhub.ai/user/subjadeites) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use codeflow to run coding-agent CLIs while streaming structured activity, command output, file changes, and completion summaries to Discord or Telegram for session observability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review marks the release as suspicious because it can weaken agent permission controls and change OpenClaw plugin or gateway settings. <br>
Mitigation: Install only for high-privilege relay/control workflows after reviewing enforcer install, restart, and allowlist changes. <br>
Risk: Relay output may expose sensitive file previews, command output, or session details when sent to shared Discord or Telegram channels. <br>
Mitigation: Use private targets, enable CODEFLOW_SAFE_MODE, and set CODEFLOW_STREAM_LOG to redacted or off for sensitive work. <br>
Risk: Global Claude bypassPermissions or allow-all setup can reduce local safeguards on machines that hold important repositories or secrets. <br>
Mitigation: Do not apply the global bypassPermissions or allow-all setup on machines that handle important codebases or secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/subjadeites/codeflow) <br>
- [Setup guide](references/setup.md) <br>
- [Discord and Telegram output reference](references/discord-output.md) <br>
- [Advanced modes](references/advanced-modes.md) <br>
- [Issue tracker](https://github.com/subjadeites/Skills/issues) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown messages and shell commands with structured relay artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can emit Discord or Telegram session updates, stream.jsonl event logs, and delivery-summary.json delivery statistics.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
