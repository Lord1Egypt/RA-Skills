## Description:

Helps an agent compress long conversations by preserving important goals, preferences, decisions, and unfinished work while summarizing useful history and discarding low-value exchanges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[c595390153-a11y](https://clawhub.ai/user/c595390153-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep long Claude Code or OpenClaw conversations usable by compacting prior context into concise summaries and structured memory. It is most relevant when context is nearly full, when a user requests compression, or when optional PreCompact hooks are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to store conversation details in long-term memory, including sensitive credentials or configuration information.

Mitigation: Require explicit review before any memory write and exclude secrets, tokens, passwords, private keys, session cookies, and sensitive account details from memory.

Risk: Optional hook configuration can make compression and post-compression memory prompts run automatically.

Mitigation: Enable hooks only after reviewing the hook configuration and confirming that automatic memory updates remain subject to user approval and redaction.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/c595390153-a11y/skills/context-compression-claude-code-custom)
- [Publisher Profile](https://clawhub.ai/user/c595390153-a11y)
- [setup-hook.md](artifact/setup-hook.md)
- [memory-template.md](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration, Shell commands]

**Output Format:** [Markdown guidance with optional JSON, YAML, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide updates to a structured memory file when the agent and user permit persistent memory writes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
