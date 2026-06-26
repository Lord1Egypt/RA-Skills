## Description: <br>
Codex Agent lets OpenClaw operate OpenAI Codex CLI through tmux sessions, notify hooks, and a Codex knowledge base so it can plan, launch, monitor, and report coding tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HenryXiaoYang](https://clawhub.ai/user/HenryXiaoYang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams using OpenClaw use this skill to delegate Codex CLI coding tasks, manage approvals, maintain Codex configuration knowledge, and receive task or approval notifications through messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Codex task output, paths, code snippets, or secrets may be forwarded to messaging channels. <br>
Mitigation: Use private notification channels and disable or redact raw Telegram forwarding for sensitive projects. <br>
Risk: The skill can delegate broad Codex command and approval authority to OpenClaw or Codex full-auto mode. <br>
Mitigation: Avoid full-auto for sensitive projects, keep human approval enabled, and review commands before approval. <br>
Risk: Long-running tmux and monitor processes can persist beyond the intended task window. <br>
Mitigation: Stop tmux and pane monitor processes after each task and keep OpenClaw session persistence bounded. <br>


## Reference(s): <br>
- [Codex Agent on ClawHub](https://clawhub.ai/HenryXiaoYang/codex-agent) <br>
- [Installation Guide](INSTALL.md) <br>
- [Codex CLI Reference](references/codex-cli-reference.md) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>
- [OpenAI Codex](https://github.com/openai/codex) <br>
- [OpenAI Codex Configuration Reference](https://developers.openai.com/codex/config-reference) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, Code] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and task reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke tmux, Codex CLI, OpenClaw messaging, and local hook scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
