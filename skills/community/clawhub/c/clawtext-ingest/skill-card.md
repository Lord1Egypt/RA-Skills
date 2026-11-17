## Description:

Multi-source memory ingestion with Discord support, automatic deduplication, and agent-ready patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ragesaq](https://clawhub.ai/user/ragesaq)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use Clawtext Ingest to convert Discord forums, local files, URLs, JSON, and raw text into structured ClawText memories with deduplication and metadata for RAG-enabled agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ingest Discord, web, file, and chat-export content into agent memory.

Mitigation: Limit Discord channel access, URL sources, local file paths, and memory directories to explicitly approved content before installation.

Risk: Autonomous or scheduled ingestion can repeatedly store sensitive or untrusted content.

Mitigation: Avoid autonomous schedules until URL allowlists, file path containment, privacy rules, and retention rules are in place.

Risk: Chat exports and web content may contain secrets, private data, or prompt-injection text.

Mitigation: Sanitize and review imported content before storing it in agent memory.

Risk: CLI subprocess patterns may expose secrets or execute under-scoped commands.

Mitigation: Keep tokens in environment variables, review command construction, and run ingestion with least-privilege credentials.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ragesaq/skills/clawtext-ingest)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Agent Guide](artifact/AGENT_GUIDE.md)
- [API Reference](artifact/API_REFERENCE.md)
- [CLI Guide](artifact/PHASE2_CLI_GUIDE.md)
- [Discord Bot Setup](artifact/DISCORD_BOT_SETUP.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown memory entries with YAML frontmatter, CLI commands, and JavaScript API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can persist deduplication hashes and trigger ClawText cluster rebuilds after ingestion.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
