## Description:

Professional DeFi data aggregator that provides unified access to TVL, protocols, chains, and yields data from DefiLlama.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and DeFi users use this skill to query DefiLlama TVL, protocol, chain, and yield-pool data from an agent workflow or CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional direct-IP HTTPS configuration can weaken certificate validation.

Mitigation: Use the default DefiLlama API URLs and leave direct-IP mode disabled.

Risk: CSV exports may be unsafe to open directly in spreadsheet tools.

Mitigation: Treat exported CSV as untrusted and sanitize or inspect it before opening in spreadsheets.

Risk: Unpinned npm dependencies can change behavior between installs.

Mitigation: Use a reviewed lockfile or pinned dependency versions for production deployments.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/deanpeng-dotcom/skills/defillama-data-aggregator)
- [Repository Metadata](https://github.com/AntalphaAI/defillama-data-aggregator)
- [DefiLlama API Documentation](https://docs.llama.fi/)
- [DefiLlama API](https://api.llama.fi)
- [DefiLlama Yields API](https://yields.llama.fi)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON, tables, and CSV]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses public DefiLlama APIs, supports in-memory caching, and requires Node.js and npm.]

## Skill Version(s):

1.0.3 (source: frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
