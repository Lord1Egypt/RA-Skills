## Description:

Manage Volcengine Supabase workspaces, branches, SQL queries, migrations, Edge Functions, Storage, and TypeScript type generation through a local CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to administer Volcengine Supabase resources, inspect workspace state, run SQL and migrations, manage branches, deploy Edge Functions, operate Storage buckets, and generate TypeScript types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform privileged Supabase administration and write operations using Volcengine credentials.

Mitigation: Install it only in an environment intended for Volcengine Supabase administration, use least-privilege credentials where possible, and review proposed changes before execution.

Risk: Read-only mode is not a complete safety boundary for write-capable workflows.

Mitigation: Treat READ_ONLY=true as a convenience guard, not an authorization control; use account permissions, isolated branches, and manual approval for destructive operations.

Risk: SQL queries and migrations can change or expose production data.

Mitigation: Prefer the documented branch-based workflow, review every SQL or migration, and validate state after changes.

Risk: API keys and service role credentials can be exposed through reveal options, logs, or chat transcripts.

Mitigation: Avoid revealing keys unless strictly necessary, keep secrets out of logs and chats, and rotate credentials if exposure is suspected.

Risk: The release depends on a personal GitHub dependency before production credentials are used.

Mitigation: Verify or replace that dependency during deployment review before using production credentials.

Risk: Endpoint defaults may not enforce HTTPS.

Mitigation: Force HTTPS before use and verify generated service URLs before sending credentials or sensitive data.

## Reference(s):

- [Volcengine](https://www.volcengine.com/)
- [ClawHub Skill Page](https://clawhub.ai/volcengine-skills/skills/byted-supabase)
- [Tool Reference](artifact/references/tool-reference.md)
- [Workflows](artifact/references/workflows.md)
- [App Integration Guide](artifact/references/app-integration-guide.md)
- [Schema Guide](artifact/references/schema-guide.md)
- [RLS Guide](artifact/references/rls-guide.md)
- [SQL Playbook](artifact/references/sql-playbook.md)
- [Edge Function Development Guide](artifact/references/edge-function-dev-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, code snippets, configuration notes, and summarized CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute real Volcengine Supabase read and write operations when configured with credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
