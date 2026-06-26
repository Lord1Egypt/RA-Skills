## Description: <br>
MCP server for Clude's 4-tier cognitive memory system to store, recall, search, and dream using Supabase, pgvector, type-specific decay, Hebbian association graphs, and Solana commitments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sebbsssss](https://clawhub.ai/user/sebbsssss) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this MCP server to give an agent persistent memory recall, memory storage, memory statistics, market mood lookup, and an in-character Clude response tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores long-lived memory data in an external Supabase project. <br>
Mitigation: Use a dedicated Supabase project and avoid storing secrets or sensitive personal data. <br>
Risk: The skill uses a powerful Supabase service key and depends on runtime package code. <br>
Mitigation: Use a rotateable secret and inspect and pin the clude-bot package before granting credentials. <br>
Risk: Claude calls with private context and Solana commitment behavior can expose data or create irreversible records. <br>
Mitigation: Require explicit user approval before memory writes, Claude calls with private context, or Solana commitment behavior. <br>


## Reference(s): <br>
- [Clude Memory MCP on ClawHub](https://clawhub.ai/sebbsssss/clude-memory-mcp) <br>
- [Supabase schema](artifact/supabase-schema.sql) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON] <br>
**Output Format:** [MCP tool responses with JSON payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, SUPABASE_URL, and SUPABASE_SERVICE_KEY; some tools read or write Supabase memory state, commit hashes to Solana, or call Claude with provided context.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
