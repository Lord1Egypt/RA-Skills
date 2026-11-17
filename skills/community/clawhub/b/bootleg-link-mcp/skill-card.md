## Description:

Bootleg Link MCP provides MCP tools for downloading and managing music from YouTube, Qobuz, and Beatport, including queue progress, account login helpers, and CDJ-2000-compatible audio output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esanle](https://clawhub.ai/user/esanle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users connect this MCP server to an agent to queue, monitor, and manage music downloads, with configurable output folders, proxy settings, quality, concurrency, and service logins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts background services and persists local task, database, cookie, and token state.

Mitigation: Run it in an isolated user account or container with a dedicated download directory, and review or clear persistent state after use.

Risk: The skill handles account credentials, cookies, and tokens for media services.

Mitigation: Avoid valuable account credentials unless necessary, use dedicated accounts where possible, and restrict access to cookie and database files.

Risk: The bundled token provider is unauthenticated and can execute remote JavaScript if reached.

Mitigation: Do not expose port 4416; constrain the provider to localhost or add authentication and network isolation before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/esanle/skills/bootleg-link-mcp)
- [Bootleg Link MCP README](artifact/README.md)
- [Bootleg Link MCP Skill Definition](artifact/SKILL.md)
- [bgutil-ytdlp-pot-provider Server README](artifact/bgutil-ytdlp-pot-provider/server/README.md)
- [yt-dlp PO Token Guide](https://github.com/yt-dlp/yt-dlp/wiki/PO-Token-Guide)

## Skill Output:

**Output Type(s):** [text, JSON, files, configuration]

**Output Format:** [MCP JSON-RPC tool responses with JSON text payloads and downloaded audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local configuration, SQLite task state, external download tools, and optional service credentials.]

## Skill Version(s):

0.9.3 (source: server release metadata; artifact frontmatter lists 0.9.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
