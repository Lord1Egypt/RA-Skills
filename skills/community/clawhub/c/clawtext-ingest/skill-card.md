## Description: <br>
Multi-source memory ingestion with Discord support, automatic deduplication, and agent-ready patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ragesaq](https://clawhub.ai/user/ragesaq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to ingest files, URLs, JSON, text, and Discord content into structured, deduplicated memory for ClawText-backed agent workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected Discord channels, files, URLs, or exports may contain sensitive or unauthorized content that becomes persistent agent memory. <br>
Mitigation: Ingest only sources the user is authorized to store, and review or redact sensitive content before persistence. <br>
Risk: Discord bot tokens and other secrets can be exposed through command history or overly broad permissions. <br>
Mitigation: Use a least-privilege Discord bot token and avoid passing secrets directly in shell history. <br>
Risk: Exported JSON and memory directories can retain private or regulated data after ingestion. <br>
Mitigation: Protect exported files and memory directories, and delete them when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ragesaq/clawtext-ingest) <br>
- [README](https://github.com/ragesaq/clawtext-ingest#readme) <br>
- [Agent Guide](https://github.com/ragesaq/clawtext-ingest/blob/main/AGENT_GUIDE.md) <br>
- [API Reference](https://github.com/ragesaq/clawtext-ingest/blob/main/API_REFERENCE.md) <br>
- [CLI Reference](https://github.com/ragesaq/clawtext-ingest/blob/main/PHASE2_CLI_GUIDE.md) <br>
- [Discord Bot Setup](https://github.com/ragesaq/clawtext-ingest/blob/main/DISCORD_BOT_SETUP.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown memory entries with YAML metadata, JSON results, and CLI status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deduplicates ingested content and can rebuild ClawText clusters after ingestion.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
