## Description: <br>
Use OpenAI Codex CLI for coding tasks, including code review, CI fixes, refactoring, feature implementation, and Clawdbot delegation to Codex CLI as a subagent or direct tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamsardo](https://clawhub.ai/user/adamsardo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering agents use this skill to route coding work to OpenAI Codex CLI for code review, bug fixes, CI repair, refactoring, feature implementation, and multi-agent coding workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delegate coding work to Codex CLI with local file editing and command execution authority. <br>
Mitigation: Use it in trusted repositories, target a specific project with `--cd`, and prefer read-only or approval-based modes for unfamiliar code. <br>
Risk: Full-access modes can remove normal sandbox and approval boundaries. <br>
Mitigation: Avoid `danger-full-access` and `--yolo` unless the operator fully accepts the risk. <br>
Risk: The integration may touch Codex authentication state and Clawdbot token sync. <br>
Mitigation: Review Codex auth/session storage and Clawdbot token sync behavior before enabling the skill. <br>


## Reference(s): <br>
- [Codex CLI Overview](https://developers.openai.com/codex/cli) <br>
- [Codex CLI Features](https://developers.openai.com/codex/cli/features) <br>
- [Codex CLI Reference](https://developers.openai.com/codex/cli/reference) <br>
- [Slash Commands Guide](https://developers.openai.com/codex/cli/slash-commands) <br>
- [AGENTS.md Spec](https://agents.md) <br>
- [Codex GitHub](https://github.com/openai/codex) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON-like configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include Codex CLI commands, Clawdbot configuration patterns, code review guidance, and implementation instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
