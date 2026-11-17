## Description:

Codex Agent helps OpenClaw operate OpenAI Codex CLI through tmux sessions, notification hooks, Codex knowledge files, task workflows, and configuration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henryxiaoyang](https://clawhub.ai/user/henryxiaoyang)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to delegate Codex CLI task planning, execution monitoring, approval handling, configuration checks, and result reporting to OpenClaw while retaining visibility through terminal or messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent automation can operate long-running Codex/OpenClaw coding sessions.

Mitigation: Install from a pinned reviewed version, keep approval decisions human-controlled for risky commands, and reconsider the long session-reset setting before use.

Risk: Task output and approval details can be forwarded through external messaging channels.

Mitigation: Avoid sensitive repositories unless notifications are redacted or disabled, and configure message targets through reviewed environment variables.

## Reference(s):

- [OpenClaw project](https://github.com/openclaw/openclaw)
- [OpenAI Codex CLI](https://github.com/openai/codex)
- [OpenAI Codex overview](https://developers.openai.com/codex/overview)
- [OpenAI Codex configuration reference](https://developers.openai.com/codex/config-reference)
- [Codex CLI reference](references/codex-cli-reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and task guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger local tmux sessions, Codex CLI commands, OpenClaw messages, and notification hooks when used by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
