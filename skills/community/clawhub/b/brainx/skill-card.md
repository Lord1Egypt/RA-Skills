## Description:

BrainX V5 is a vector memory engine for OpenClaw agents that stores, searches, and injects contextual memories using PostgreSQL, pgvector, and OpenAI embeddings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdx2025](https://clawhub.ai/user/mdx2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use BrainX V5 to give OpenClaw agents persistent shared memory, semantic recall, startup context injection, and operational diagnostics across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad, shared persistent memories can expose sensitive context across agents or future sessions.

Mitigation: Treat the database and generated context files as sensitive infrastructure, avoid storing personal or financial data by default, and use PII scrubbing and access controls before deployment.

Risk: Automatic startup injection can place stale, incorrect, or over-broad memories into an agent prompt.

Mitigation: Review injected context, run health and smoke tests after updates, and tune limits, tiers, minimum importance, and retention settings for each deployment.

Risk: Unattended promotion into AGENTS.md, TOOLS.md, or SOUL.md can convert unreviewed memories into persistent operating rules.

Mitigation: Disable unattended promotion unless every proposed rule is reviewed and approved before it is written into startup instruction files.

Risk: Memory and search content may be sent to OpenAI for embeddings.

Mitigation: Warn users before use, exclude secrets from memories and backups, and configure data handling policies for content submitted to the embeddings endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mdx2025/skills/brainx)
- [BrainX V5 Documentation](docs/INDEX.md)
- [CLI Reference](docs/CLI.md)
- [Configuration](docs/CONFIG.md)
- [Database Schema](docs/SCHEMA.md)
- [BrainX V5 Auto-Inject Hook](hook/HOOK.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON, shell commands, and prompt-ready text blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include retrieved memory snippets, database diagnostics, configuration changes, SQL-backed memory records, and generated workspace context files.]

## Skill Version(s):

0.3.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
