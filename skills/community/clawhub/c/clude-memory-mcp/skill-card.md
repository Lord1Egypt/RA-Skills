## Description:

MCP server for Clude's 4-tier cognitive memory system: store, recall, search, and dream with Supabase, pgvector, type-specific decay, association graphs, and Solana commitments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebbsssss](https://clawhub.ai/user/sebbsssss)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this MCP server to add persistent memory, memory search, memory statistics, market mood lookup, and short in-character responses to Clude-backed agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Supabase service key, which can be highly privileged.

Mitigation: Use least-privilege Supabase credentials and keep deployments limited to tightly scoped personal or test environments until credential scope is reduced.

Risk: Persistent full-memory storage and retrieval can expose secrets, regulated personal data, or cross-user memories without clear tenant and retention controls.

Mitigation: Do not store secrets or regulated personal data, and add authentication, tenant isolation, retention, and deletion controls before broader deployment.

Risk: Unbounded or insufficiently controlled memory inputs can increase privacy and reliability risk.

Mitigation: Enforce input limits and review stored-memory behavior before using the skill with real users or shared datasets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sebbsssss/skills/clude-memory-mcp)
- [Skill definition](artifact/SKILL.md)
- [Supabase schema](artifact/supabase-schema.sql)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON-formatted MCP text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns memory records, storage status, memory statistics, market mood data, and in-character answers.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and server.ts)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
