## Description: <br>
Vector memory engine that uses PostgreSQL, pgvector, and OpenAI embeddings to store, search, and inject contextual memories into OpenClaw agent prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mdx2025](https://clawhub.ai/user/mdx2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use BrainX to give OpenClaw agents persistent shared memory, semantic search over prior context, and automatic prompt-context injection at session bootstrap. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation and workspace content may be stored persistently in PostgreSQL and sent to OpenAI for embeddings. <br>
Mitigation: Restrict contributing workspaces and agents, avoid storing secrets, review redaction settings, and set retention and backup handling before enabling shared memory. <br>
Risk: Automatically injected memories can influence future prompts and prompt-visible workspace files. <br>
Mitigation: Review active hooks and cron jobs, audit generated MEMORY.md and BRAINX_CONTEXT.md content, and disable or review automatic rule-promotion behavior. <br>
Risk: Database credentials, OpenAI API keys, and memory backups can expose sensitive agent context. <br>
Mitigation: Protect DATABASE_URL and OPENAI_API_KEY, encrypt backups, and limit database and filesystem access to trusted operators. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mdx2025/brainx) <br>
- [How It Works](docs/HOW-IT-WORKS.md) <br>
- [CLI Reference](docs/CLI.md) <br>
- [Configuration](docs/CONFIG.md) <br>
- [Database Schema](docs/SCHEMA.md) <br>
- [Auto-Inject Hook](hook/HOOK.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown and plain text context blocks, JSON CLI results, and shell commands/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DATABASE_URL, OPENAI_API_KEY, PostgreSQL with pgvector, and psql.] <br>

## Skill Version(s): <br>
0.3.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
