## Description:

Connect to Supabase for database operations, vector search, and storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ecosincronia](https://clawhub.ai/user/ecosincronia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Supabase projects for SQL queries, table CRUD, stored procedure calls, storage-adjacent workflows, and pgvector similarity search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses SUPABASE_SERVICE_KEY for privileged Supabase operations that can bypass row-level security.

Mitigation: Use a dedicated project or tightly scoped credentials where possible, and install only when privileged administration is intended.

Risk: Raw SQL, update, delete, and RPC operations can change or expose production data.

Mitigation: Verify SUPABASE_URL before each run and require manual review before executing mutating or raw SQL commands.

Risk: Vector search text may be sent to OpenAI for embeddings when OPENAI_API_KEY is configured.

Mitigation: Avoid confidential vector-search queries unless external OpenAI transmission is acceptable for the use case.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ecosincronia/skills/ecosincronia-supabase)
- [Publisher profile](https://clawhub.ai/user/ecosincronia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute Supabase REST and RPC requests when the required environment variables are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
