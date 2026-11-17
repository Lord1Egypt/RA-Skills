## Description:

Viking 记忆系统 provides five-level memory management, protected important memories, vector similarity retrieval, optional Feishu session capture, and cross-agent memory sharing for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyxlouspg](https://clawhub.ai/user/guyxlouspg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to persist, search, and manage long-term OpenClaw agent memories across local and global workspaces. It supports automated memory tiering, optional Feishu chat session capture, and retrieval of stored context during later agent work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically persist chats and memories across agents and chat sources.

Mitigation: Disable auto-save, Feishu session capture, and cron jobs until every agent and chat source has explicit consent and retention expectations are documented.

Risk: The skill can send content to a hard-coded plaintext network endpoint.

Mitigation: Change OLLAMA_HOST to a trusted loopback or authenticated HTTPS service before enabling embedding or memory automation.

Risk: The skill exposes unsafe file read and write paths.

Mitigation: Fix viking:// path validation and restrict memory operations to approved workspace roots before deployment.

Risk: Retention and downgrade operations can alter or compress stored memory content automatically.

Mitigation: Make downgrade and retention operations reviewable and recoverable, including backups or an approval step for protected memories.

Risk: Persisted memories may contain secrets or sensitive chat content.

Mitigation: Add secret redaction before writing memories or generating vector embeddings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guyxlouspg/skills/cat-viking-memory)
- [Detailed usage guide](artifact/references/README.md)
- [Feishu integration guide](artifact/references/飞书集成说明.md)
- [OpenViking reference](https://github.com/volcengine/OpenViking)
- [Viking memory system reference](https://github.com/TanDongTaotao/viking-memory-system.git)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and shell-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and manages local memory files, vector indexes, and configuration-driven automation.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
